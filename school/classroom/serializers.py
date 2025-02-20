from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Student, Teacher, Parent, Course, Enrollment, Attendance, Exam, ExamResult, FeePayment, Timetable, SalaryPayment, Homework, Test, DisciplineRecord, AreaOfImprovement

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model() # type: ignore
        fields = ['id','username','email','role','date_of_birth','profile_photo']

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = '__all__'

class ParentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Parent
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = get_user_model().objects.create(**user_data)
        parent = Parent.objects.create(user=user, **validated_data)
        return parent
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Teacher
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = get_user_model().objects.create(**user_data)
        parent = Parent.objects.create(user=user, **validated_data)
        return parent
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__' 

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

# Exam, ExamResult, FeePayment, Timetable, SalaryPayment
class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'

class ExamResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamResult
        fields = '__all__'

class FeePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeePayment

class TimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timetable
        fields = '__all__'

class SalaryPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryPayment
        fields = '__all__'

class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = '__all__'


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'


class DisciplineRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisciplineRecord
        fields = '__all__'


class AreaOfImprovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaOfImprovement
        fields = '__all__'