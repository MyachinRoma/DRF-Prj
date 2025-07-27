from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Course, Lesson


class LessonSerializer(ModelSerializer):
    lessons = SerializerMethodField()

    def get_lessons(self, lesson):
        return [lesson.title for lesson in Lesson.objects.filter(lesson=lesson)]

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer()

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):
    count_of_lessons = serializers.SerializerMethodField()
    lesson = LessonSerializer()

    def get_count_of_lessons(self, objects):
        return objects.lesson_set.count()

    class Meta:
        model = Course
        fields = ("title", "description", "preview", "count_of_lessons", "lesson")
