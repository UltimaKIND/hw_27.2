from rest_framework import serializers  # type: ignore

from materials.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    """
    сериализатор модели курса
    """

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    """
    сериализатор модели урока
    """

    class Meta:
        model = Lesson
        fields = "__all__"
