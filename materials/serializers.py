from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson
from materials.validators import YouTubeLinkValidator
from users.models import Subscription


class LessonSerializer(ModelSerializer):
    """
    сериализатор модели урока
    """

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [YouTubeLinkValidator()]


class CourseSerializer(ModelSerializer):
    """
    сериализатор модели курса
    """

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    """
    сериализатор модели курса c доп. полями
    """

    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(source="lesson_set", many=True, read_only=True)
    subscribed = SerializerMethodField()

    def get_lessons_count(self, course):
        return course.lesson_set.count()

    def get_subscribed(self, instance):
        user = self.context["request"].user
        return Subscription.objects.filter(user=user, course=instance).exists()

    class Meta:
        model = Course
        fields = [
            "title",
            "preview",
            "description",
            "lessons_count",
            "lessons",
            "subscribed",
        ]


class SubscriptionSerializer(ModelSerializer):

    class Meta:
        model = Subscription
        fields = "__all__"
