from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    lesson = LessonSerializer(read_only=True, many=True, source="lesson_set")


    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    count_of_lessons = SerializerMethodField()
    lesson = LessonSerializer(read_only=True, many=True, source="lesson_set")


    def get_count_of_lessons(self, objects):
        return objects.lesson_set.count()


    class Meta:
        model = Course
        fields = ("title", "description", "preview", "count_of_lessons", "lesson")
