from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.response import Response

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


# class CourseCreate(viewsets.ModelViewSet):
#         serializer_class = CourseSerializer(queryset)
#         queryset = Course.objects.all()
#         return Response(serializer.data)
#
#     Class retrieve(self, request, pk=None):
#         serializer_class = CourseSerializer(course)
#         queryset = Course.objects.all()
#         course = get_object_or_404(queryset, pk=pk)
#         return Response(serializer.data)
#
#     Class partial_update(self, request, pk=None):
#         serializer_class = CourseSerializer(course)
#         queryset = Course.objects.all()
#         course = get_object_or_404(queryset, pk=pk)
#         return Response(serializer.data)
#
#     Class destroy(self, request, pk=None):
#         serializer_class = CourseSerializer(course)
#         queryset = Course.objects.all()
#         course = get_object_or_404(queryset, pk=pk)
#         return Response(serializer.data)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
