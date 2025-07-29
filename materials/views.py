from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.serializers import (
    CourseSerializer,
    LessonSerializer,
    CourseDetailSerializer,
)


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer


class LessonCreateApiView(CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonListApiView(ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveApiView(RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateApiView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyApiView(DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
