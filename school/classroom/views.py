

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import (
    Student, Teacher, Parent, Course, Enrollment, 
    Attendance, Exam, ExamResult, FeePayment, Timetable,
    EnrollmentYear, ClassRoom, Staff, Homework,
    Test, DisciplineRecord, AreaOfImprovement
)
from .serializers import (
    UserSerializer, StudentSerializer, TeacherSerializer, 
    ParentSerializer, CourseSerializer, EnrollmentSerializer,
    AttendanceSerializer, ExamSerializer, ExamResultSerializer,
    FeePaymentSerializer, TimetableSerializer, EnrollmentYearSerializer,
    ClassRoomSerializer, StaffSerializer, HomeworkSerializer,
    TestSerializer, DisciplineRecordSerializer, AreaOfImprovementSerializer
)

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class EnrollmentYearViewSet(viewsets.ModelViewSet):
    queryset = EnrollmentYear.objects.all()
    serializer_class = EnrollmentYearSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=True, methods=['get'])
    def homework(self, request, pk=None):
        student = self.get_object()
        homeworks = Homework.objects.filter(student=student)
        serializer = HomeworkSerializer(homeworks, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def tests(self, request, pk=None):
        student = self.get_object()
        tests = Test.objects.filter(student=student)
        serializer = TestSerializer(tests, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def discipline_records(self, request, pk=None):
        student = self.get_object()
        records = DisciplineRecord.objects.filter(student=student)
        serializer = DisciplineRecordSerializer(records, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def improvement_areas(self, request, pk=None):
        student = self.get_object()
        areas = AreaOfImprovement.objects.filter(student=student)
        serializer = AreaOfImprovementSerializer(areas, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def enrollments(self, request, pk=None):
        student = self.get_object()
        enrollments = Enrollment.objects.filter(student=student)
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def attendance(self, request, pk=None):
        student = self.get_object()
        attendances = Attendance.objects.filter(student=student)
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def fees(self, request, pk=None):
        student = self.get_object()
        fees = FeePayment.objects.filter(student=student)
        serializer = FeePaymentSerializer(fees, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def exam_results(self, request, pk=None):
        student = self.get_object()
        results = ExamResult.objects.filter(student=student)
        serializer = ExamResultSerializer(results, many=True)
        return Response(serializer.data)

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    
    @action(detail=True, methods=['get'])
    def courses(self, request, pk=None):
        teacher = self.get_object()
        courses = Course.objects.filter(teacher=teacher)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

class ParentViewSet(viewsets.ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    
    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        parent = self.get_object()
        students = parent.students.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
    @action(detail=True, methods=['get'])
    def enrollments(self, request, pk=None):
        course = self.get_object()
        enrollments = Enrollment.objects.filter(course=course)
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def attendance(self, request, pk=None):
        course = self.get_object()
        attendances = Attendance.objects.filter(course=course)
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def exams(self, request, pk=None):
        course = self.get_object()
        exams = Exam.objects.filter(course=course)
        serializer = ExamSerializer(exams, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def timetable(self, request, pk=None):
        course = self.get_object()
        timetable_entries = Timetable.objects.filter(course=course)
        serializer = TimetableSerializer(timetable_entries, many=True)
        return Response(serializer.data)

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    
    @action(detail=False, methods=['get'])
    def by_year(self, request):
        year = request.query_params.get('year', None)
        if year is not None:
            enrollments = Enrollment.objects.filter(year=year)
            serializer = self.get_serializer(enrollments, many=True)
            return Response(serializer.data)
        return Response({"error": "Year parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    
    @action(detail=False, methods=['get'])
    def by_date(self, request):
        date = request.query_params.get('date', None)
        if date is not None:
            attendances = Attendance.objects.filter(date=date)
            serializer = self.get_serializer(attendances, many=True)
            return Response(serializer.data)
        return Response({"error": "Date parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

class ClassRoomViewSet(viewsets.ModelViewSet):
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer
    
    @action(detail=True, methods=['get'])
    def timetable(self, request, pk=None):
        classroom = self.get_object()
        timetable_entries = Timetable.objects.filter(classroom=classroom)
        serializer = TimetableSerializer(timetable_entries, many=True)
        return Response(serializer.data)

class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    
    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        exam = self.get_object()
        results = ExamResult.objects.filter(exam=exam)
        serializer = ExamResultSerializer(results, many=True)
        return Response(serializer.data)

class ExamResultViewSet(viewsets.ModelViewSet):
    queryset = ExamResult.objects.all()
    serializer_class = ExamResultSerializer

class FeePaymentViewSet(viewsets.ModelViewSet):
    queryset = FeePayment.objects.all()
    serializer_class = FeePaymentSerializer
    
    @action(detail=False, methods=['get'])
    def by_date_range(self, request):
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        
        if start_date and end_date:
            payments = FeePayment.objects.filter(payment_date__range=[start_date, end_date])
            serializer = self.get_serializer(payments, many=True)
            return Response(serializer.data)
        return Response({"error": "Both start_date and end_date parameters are required"}, 
                       status=status.HTTP_400_BAD_REQUEST)

class TimetableViewSet(viewsets.ModelViewSet):
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer
    
    @action(detail=False, methods=['get'])
    def by_day(self, request):
        day = request.query_params.get('day', None)
        if day is not None:
            timetable_entries = Timetable.objects.filter(day_of_week=day)
            serializer = self.get_serializer(timetable_entries, many=True)
            return Response(serializer.data)
        return Response({"error": "Day parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        from datetime import date
        homeworks = Homework.objects.filter(due_date__gte=date.today()).order_by('due_date')
        serializer = self.get_serializer(homeworks, many=True)
        return Response(serializer.data)

class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    
    @action(detail=False, methods=['get'])
    def by_subject(self, request):
        subject = request.query_params.get('subject', None)
        if subject is not None:
            tests = Test.objects.filter(subject=subject)
            serializer = self.get_serializer(tests, many=True)
            return Response(serializer.data)
        return Response({"error": "Subject parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

class DisciplineRecordViewSet(viewsets.ModelViewSet):
    queryset = DisciplineRecord.objects.all()
    serializer_class = DisciplineRecordSerializer

class AreaOfImprovementViewSet(viewsets.ModelViewSet):
    queryset = AreaOfImprovement.objects.all()
    serializer_class = AreaOfImprovementSerializer

"""
==============================================================================


from django.shortcuts import render
from rest_framework import viewsets
from .models import (Student, Teacher, Parent, Course, Enrollment, Attendance, Exam, ExamResult, FeePayment, Timetable, 
                    SalaryPayment, Homework, Test, DisciplineRecord, AreaOfImprovement, EnrollmentYear)

from .models import (
    Student, Teacher, Parent, Course, Enrollment, 
    Attendance, Exam, ExamResult, FeePayment, Timetable,
    EnrollmentYear, ClassRoom, Staff, User, Homework,
    Test, DisciplineRecord, AreaOfImprovement
)

from django.contrib.auth import get_user_model
from .serializers import (UserSerializer, StudentSerializer, TeacherSerializer, ParentSerializer, CourseSerializer, 
                          EnrollmentSerializer, AttendanceSerializer, ExamSerializer, ExamResultSerializer, FeePaymentSerializer, 
                          TimetableSerializer, SalaryPaymentSerializer, HomeworkSerializer, TestSerializer, DisciplineRecordSerializer, 
                          AreaOfImprovementSerializer)
class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

#class StudentViewSet(viewsets.ModelViewSet):
 #   queryset = Student.objects.all()
  #  serializer_class = StudentSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    def create(self, request, *args, **kwargs):
        # Extract enrollment year data if it's a dictionary
        enrollment_year_data = request.data.get('enrollment_year')
        
        # If enrollment_year is sent as a dictionary
        if isinstance(enrollment_year_data, dict):
            year_value = enrollment_year_data.get('year')
            
            # Try to find an existing EnrollmentYear or create a new one
            enrollment_year, created = EnrollmentYear.objects.get_or_create(year=year_value)
            
            # Modify the data to include the actual EnrollmentYear instance id
            mutable_data = request.data.copy()
            mutable_data['enrollment_year'] = enrollment_year.id
            request.data = mutable_data
            
        # Continue with the normal create process
        return super().create(request, *args, **kwargs)
        
    def update(self, request, *args, **kwargs):
        # Similar handling for update operations
        enrollment_year_data = request.data.get('enrollment_year')
        
        if isinstance(enrollment_year_data, dict):
            year_value = enrollment_year_data.get('year')
            enrollment_year, created = EnrollmentYear.objects.get_or_create(year=year_value)
            
            mutable_data = request.data.copy()
            mutable_data['enrollment_year'] = enrollment_year.id
            request.data = mutable_data
            
        return super().update(request, *args, **kwargs)

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
"""