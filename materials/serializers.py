from rest_framework import serializers

from materials.models import Course, Lesson, Subscription, CoursePayment
from materials.validators import ScamLinkValidator


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [ScamLinkValidator(field='video_link')]


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)
    lesson_count = serializers.SerializerMethodField()
    subscription = serializers.SerializerMethodField()

    def get_lesson_count(self, instance):
        if instance.lesson_set.all().first():
            return instance.lesson_set.all().count()
        return 0

    def get_subscription(self, instance):
        user = self.context["request"].user

        subscription = Subscription.objects.filter(user=user, course=instance).first()
        if subscription:
            return subscription.is_active
        return 0

    class Meta:
        model = Course
        fields = "__all__"
        # fields = ('id', 'name', 'description', 'lesson_count', 'lessons')


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = "__all__"


class CoursePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursePayment
        fields = '__all__'
