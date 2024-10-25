from django.utils import timezone
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView  # type: ignore
from rest_framework.generics import (DestroyAPIView, ListAPIView,
                                     RetrieveAPIView, UpdateAPIView,
                                     get_object_or_404)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet  # type: ignore

from materials.models import Course, Lesson
from materials.pagination import CustomPagination
from materials.serializers import (CourseDetailSerializer, CourseSerializer,
                                   LessonSerializer)
from materials.tasks import update_mailing
from users.permissions import IsModer, IsOwner


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="эндпоинт вывода списка курсов"
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="эндпоинт вывода детальной информации о курсе"
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_description="эндпоинт обновление информации о курсе"
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_description="эндпоинт создания нового курсa"
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(operation_description="эндпоинт удаления курса"),
)
class CourseViewSet(ModelViewSet):
    """
    контроллер CRUD курса
    """

    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        serializer.validated_data["owner"] = self.request.user
        serializer.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModer, IsOwner)
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        course = self.get_object()
        serializer = self.get_serializer(course, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        course = serializer.save()
        course.update_at = timezone.now()
        course.save()
        update_mailing.delay(course.id)
        return Response(serializer.data)


class LessonCreateApiView(CreateAPIView):
    """
    контроллер создания урока
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [~IsModer]

    def perform_create(self, serializer):
        serializer.validated_data["owner"] = self.request.user
        lesson = serializer.save()
        if lesson.course:
            delta = timezone.now() - lesson.course.update_at
            if delta.seconds // 3600 >= 4:
                lesson.course.update_at = timezone.now()
                update_mailing.delay(lesson.course.id)


class LessonUpdateApiView(UpdateAPIView):
    """
    контроллер редактирования урока
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModer | IsOwner]

    def perform_update(self, serializer):
        lesson = serializer.save()
        if lesson.course:
            delta = timezone.now() - lesson.course.update_at
            if delta.seconds // 3600 >= 4:
                lesson.course.update_at = timezone.now()
                update_mailing.delay(lesson.course.id)


class LessonRetrieveApiView(RetrieveAPIView):
    """
    контроллер детального отображения урока
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModer | IsOwner]


class LessonListApiView(ListAPIView):
    """
    контроллер отображения списка уроков
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination


class LessonDestroyApiView(DestroyAPIView):
    """
    контроллер удаления урока
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [~IsModer, IsOwner]
