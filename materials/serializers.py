from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Course, Lesson, Subscription
from .validators import validate_links


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.CharField(validators=[validate_links])

    class Meta:
        model = Lesson
        fields = ["id", "title", "course", "owner", "video_url"]

class LessonListSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        # Только то, что ждёт тест
        fields = ["id", "title", "course", "owner", "video_url"]

class LessonDetailSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "title", "course", "owner", "video_url", "description", "picture"]
        read_only_fields = ["owner"]  # ВАЖНО: здесь нет "title"


    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        update_fields = list(validated_data.keys())
        if update_fields:
            instance.save(update_fields=update_fields)
        else:
            instance.save()
        return instance



class CourseSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(many=True, source="lesson_set")

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):
    count_of_lessons = serializers.SerializerMethodField()
    lesson = LessonSerializer(many=True, source="lesson_set")
    info_lessons = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    def get_count_of_lessons(self, objects):
        return objects.lesson_set.count()

    def get_info_lessons(self, obj):
        lessons = obj.lesson_set.all()
        return LessonSerializer(lessons, many=True).data

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        if not user.is_authenticated:
            return False
        return Subscription.objects.filter(user=user, course=obj).exists()

    class Meta:
        model = Course
        fields = (
            "title",
            "description",
            "preview",
            "count_of_lessons",
            "lesson",
            "info_lessons",
            "is_subscribed",
        )
