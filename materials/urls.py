from django.urls import path
from rest_framework.routers import SimpleRouter  # type: ignore

from materials.apps import MaterialsConfig
from materials.views import (CourseViewSet, LessonCreateApiView,
                             LessonDestroyApiView, LessonListApiView,
                             LessonRetrieveApiView, LessonUpdateApiView)

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register("", CourseViewSet, basename="course")


urlpatterns = [
    path("lessons/", LessonListApiView.as_view(), name="lesson_list"),
    path("lessons/create/", LessonCreateApiView.as_view(), name="lesson_create"),
    path("lessons/<int:pk>/", LessonRetrieveApiView.as_view(), name="lesson_detail"),
    path(
        "lessons/update/<int:pk>/", LessonUpdateApiView.as_view(), name="lesson_update"
    ),
    path(
        "lessons/delete/<int:pk>/", LessonDestroyApiView.as_view(), name="lesson_delete"
    ),
] + router.urls
