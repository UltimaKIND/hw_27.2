from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    """
    сериализатор модели урока
    """

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    """
    сериализатор модели курса
    """

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    """
    сериализатор модели курса
    """

    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(source="lesson_set", many=True, read_only=True)

    def get_lessons_count(self, course):
        return course.lesson_set.count()

    class Meta:
        model = Course
        fields = ["title", "preview", "description", "lessons_count", "lessons"]
