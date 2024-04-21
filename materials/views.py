from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lesson, Subscription, CoursePayment
from materials.paginators import CoursePaginator, LessonPaginator
from materials.serializers import CourseSerializer, LessonSerializer
from materials.services import get_session
from users.permissions import IsModerator, IsOwnerOrStaff
from users.serializers import PaymentSerializer
from materials.tasks import send_mail_for_updates


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursePaginator
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_course = self.request
        new_course.owner = self.request.user
        serializer.save()

    def get_permissions(self):
        if self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated | IsOwnerOrStaff]
        if self.action == 'delete':
            self.permission_classes = [IsAuthenticated | IsOwnerOrStaff]
        elif self.action == 'update':
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwnerOrStaff]
        return [permission() for permission in self.permission_classes]

    def update(self, request, *args, **kwargs):

        instance = self.get_object()
        # subscribed_users = instance.get_subscribed_users()

        # Отправление писем подписанным пользователям
        send_mail_for_updates.delay(instance.id)
        # for user in subscribed_users:
        #     if user.email:
        #         send_mail_for_updates.delay(instance.name, user.email)

        return super().update(request, *args, **kwargs)

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
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [AllowAny]
    pagination_class = LessonPaginator
    # permission_classes = [IsModerator | IsOwnerOrStaff]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [AllowAny]
    # permission_classes = [IsModerator, IsOwnerOrStaff]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [AllowAny]
    # permission_classes = [IsModerator, IsOwnerOrStaff]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [AllowAny]
    # permission_classes = [IsAdminUser, IsOwnerOrStaff]


class SubscriptionAPIVIEW(APIView):

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course')
        course_item = get_object_or_404(Course, pk=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.is_active = False
            message = 'Подписка удалена'
        else:
            subs_item = Subscription.objects.create(
                user=user,
                course=course_item,
            )
            subs_item.save()

            subs_item.is_active = True
            message = 'Подписка добавлена'

        return Response({"message": message})


# class PaymentAPIView(generics.CreateAPIView):
#     queryset = CoursePayment.objects.all()
#     serializer_class = PaymentSerializer
#     permission_classes = [AllowAny]
#
#     def perform_create(self, serializer):
#         course_paid = serializer.save()
#         payment_link = get_session(course_paid)
#         course_paid.link = payment_link
#         course_paid.save()
