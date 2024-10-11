from rest_framework import filters, status
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet  # type: ignore

from materials.models import Course
from materials.serializers import SubscriptionSerializer
from users.models import Payment, Subscription, User
from users.permissions import IsModer, IsOwner, IsSelfUser
from users.serializers import (OtherUserSerializer, PaymentSerializer,
                               UserSerializer)
from users.services import (convert_rub_to_usd, create_stripe_price,
                            create_stripe_session)


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [filters.OrderingFilter]
    filterset_fields = ["course", "lesson", "payment"]
    ordering_fields = [
        "payment_date",
    ]

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        amount_in_usd = convert_rub_to_usd(payment.payment_amount)
        price = create_stripe_price(amount_in_usd)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsAuthenticated,)
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        elif self.action in ["update", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsSelfUser]

        return super().get_permissions()

    def get_serializer_class(self):
        if (
            self.action in ["create", "update", "partial_update"]
            or self.action == "retrieve"
            and self.request.user == super().get_object()
        ):
            self.serializer_class = UserSerializer
        else:
            self.serializer_class = OtherUserSerializer
        return self.serializer_class


class SubscriptionAPIView(APIView):
    """
    контроллер создания/удаления подписки
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course")
        if not course_id:
            return Response({"message": "курс не передан"}, status=400)
        course_item = get_object_or_404(Course, id=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
            # Если подписки у пользователя на этот курс нет - создаем ее
            return Response({"message": message}, status=204)
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "подписка добавлена"
            # Возвращаем ответ в API
            return Response({"message": message}, status=201)
