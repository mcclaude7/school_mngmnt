from django.shortcuts import render
from rest_framework import viewsets, serializers
from .models import Student, Teacher, Parent, Course, Enrollment, Attendance, Exam, ExamResult, FeePayment, Timetable, SalaryPayment, Homework, Test, DisciplineRecord, AreaOfImprovement

from django.contrib.auth import get_user_model
from .serializers import UserSerializer, StudentSerializer, TeacherSerializer, ParentSerializer, CourseSerializer, EnrollmentSerializer, AttendanceSerializer, ExamSerializer, ExamResultSerializer, FeePaymentSerializer, TimetableSerializer, SalaryPaymentSerializer, HomeworkSerializer, TestSerializer, DisciplineRecordSerializer, AreaOfImprovementSerializer
class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class ParentViewSet(viewsets.ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

class ExamResultViewSet(viewsets.ModelViewSet):
    queryset = ExamResult.objects.all()
    serializer_class = ExamResultSerializer

class FeePaymentViewSet(viewsets.ModelViewSet):
    queryset = FeePayment.objects.all()
    serializer_class = FeePaymentSerializer

class TimetableViewSet(viewsets.ModelViewSet):
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer

class SalaryPaymentViewSet(viewsets.ModelViewSet):
    queryset = SalaryPayment.objects.all()
    serializer_class = SalaryPaymentSerializer

class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer

class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

class DisciplineRecordViewSet(viewsets.ModelViewSet):
    queryset = DisciplineRecord.objects.all()
    serializer_class = DisciplineRecordSerializer

class AreaOfImprovementViewSet(viewsets.ModelViewSet):
    queryset = AreaOfImprovement.objects.all()
    serializer_class = AreaOfImprovementSerializer



# Create your views here.
