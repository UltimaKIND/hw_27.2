from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    """
    сериализатор модели курса
    """
    lessons = SerializerMethodField()

    def get_lessons(self, course):
        return Lesson.objects.all().filter(course=course).count()

    class Meta:
        model = Course
        fields = "__all__"





class LessonSerializer(ModelSerializer):
    """
    сериализатор модели урока
    """

    class Meta:
        model = Lesson
        fields = "__all__"
