from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Student, Teacher, Parent, Course, Enrollment, Attendance, Exam, ExamResult, FeePayment, Timetable, SalaryPayment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model() # type: ignore
        fields = ['id','username','email','role','date_of_birth','profile_photo']

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = '__all__'
