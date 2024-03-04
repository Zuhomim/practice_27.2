from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lesson, Subscription
from materials.paginators import CoursePaginator, LessonPaginator
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwnerOrStaff


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursePaginator

    def perform_create(self, serializer):
        new_course = self.request
        new_course.owner = self.request.user
        serializer.save()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action == 'delete':
            self.permission_classes = [IsOwnerOrStaff]
        elif self.action == 'list' or self.action == 'update':
            self.permission_classes = [IsModerator | IsOwnerOrStaff]
        return [permission() for permission in self.permission_classes]


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
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwnerOrStaff]
    pagination_class = LessonPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator, IsOwnerOrStaff]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator, IsOwnerOrStaff]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAdminUser, IsOwnerOrStaff]


class SubscriptionAPIVIEW(APIView):
    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.create(
            user=user,
            course=course_item,

        )
        subs_item.save()

        if subs_item.exists():
            subs_item.is_active = False
            message = 'Подписка удалена'
        else:
            subs_item.is_active = True
            message = 'Подписка добавлена'

        return Response({"message": message})
