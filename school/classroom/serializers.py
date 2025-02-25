from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Student, Teacher, Parent, Course, Enrollment, 
    Attendance, Exam, ExamResult, FeePayment, Timetable,
    EnrollmentYear, ClassRoom, Staff, User, Homework,
    Test, DisciplineRecord, AreaOfImprovement
)

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'role', 'date_of_birth', 'profile_photo', 'contact_number']
        extra_kwargs = {
            'password': {'write_only': True}
        }

class EnrollmentYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrollmentYear
        fields = ['id', 'year']

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    enrollment_year = EnrollmentYearSerializer()
    
    class Meta:
        model = Student
        fields = ['id', 'user', 'enrollment_year', 'grade', 'student_id']
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        enrollment_year_data = validated_data.pop('enrollment_year')
        
        # Create or get the user
        password = user_data.pop('password', User.objects.make_random_password())
        user = User.objects.create_user(**user_data)
        user.set_password(password)
        user.save()
        
        # Create or get the enrollment year
        enrollment_year, created = EnrollmentYear.objects.get_or_create(**enrollment_year_data)
        
        # Create the student
        student = Student.objects.create(
            user=user,
            enrollment_year=enrollment_year,
            **validated_data
        )
        return student
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        enrollment_year_data = validated_data.pop('enrollment_year', None)
        
        # Update user if provided
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                if attr == 'password':
                    user.set_password(value)
                else:
                    setattr(user, attr, value)
            user.save()
        
        # Update enrollment year if provided
        if enrollment_year_data:
            enrollment_year, created = EnrollmentYear.objects.get_or_create(**enrollment_year_data)
            instance.enrollment_year = enrollment_year
        
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Teacher
        fields = ['id', 'user', 'employee_id', 'subject_specialization', 'hire_date', 'salary']
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password', User.objects.make_random_password())
        user = User.objects.create_user(**user_data)
        user.set_password(password)
        user.save()
        
        teacher = Teacher.objects.create(user=user, **validated_data)
        return teacher
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                if attr == 'password':
                    user.set_password(value)
                else:
                    setattr(user, attr, value)
            user.save()
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

class ParentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    students = serializers.PrimaryKeyRelatedField(many=True, queryset=Student.objects.all())
    
    class Meta:
        model = Parent
        fields = ['id', 'user', 'students', 'address']
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        students_data = validated_data.pop('students', [])
        
        password = user_data.pop('password', User.objects.make_random_password())
        user = User.objects.create_user(**user_data)
        user.set_password(password)
        user.save()
        
        parent = Parent.objects.create(user=user, **validated_data)
        parent.students.set(students_data)
        
        return parent
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        students_data = validated_data.pop('students', None)
        
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                if attr == 'password':
                    user.set_password(value)
                else:
                    setattr(user, attr, value)
            user.save()
        
        if students_data is not None:
            instance.students.set(students_data)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

class CourseSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(read_only=True)
    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(),
        source='teacher',
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Course
        fields = ['id', 'course_code', 'course_name', 'description', 'teacher', 'teacher_id', 'schedule']

class EnrollmentSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(many=True, queryset=Student.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    
    class Meta:
        model = Enrollment
        fields = ['id', 'year', 'student', 'course', 'date_enrolled', 'grade']

class AttendanceSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    
    class Meta:
        model = Attendance
        fields = ['id', 'student', 'course', 'date', 'status']

class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = ['id', 'name', 'capacity']

class ExamSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    
    class Meta:
        model = Exam
        fields = ['id', 'course', 'exam_date', 'total_marks']

class ExamResultSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    exam = serializers.PrimaryKeyRelatedField(queryset=Exam.objects.all())
    
    class Meta:
        model = ExamResult
        fields = ['id', 'student', 'exam', 'marks_obtained']

class FeePaymentSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    
    class Meta:
        model = FeePayment
        fields = ['id', 'student', 'amount_paid', 'payment_date', 'receipt_number']

class TimetableSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    classroom = serializers.PrimaryKeyRelatedField(queryset=ClassRoom.objects.all(), required=False, allow_null=True)
    
    class Meta:
        model = Timetable
        fields = ['id', 'day_of_week', 'course', 'start_time', 'end_time', 'classroom']

class StaffSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Staff
        fields = ['id', 'user', 'position', 'hire_date', 'salary']
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password', User.objects.make_random_password())
        user = User.objects.create_user(**user_data)
        user.set_password(password)
        user.save()
        
        staff = Staff.objects.create(user=user, **validated_data)
        return staff
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                if attr == 'password':
                    user.set_password(value)
                else:
                    setattr(user, attr, value)
            user.save()
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

class HomeworkSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    
    class Meta:
        model = Homework
        fields = ['id', 'student', 'subject', 'description', 'due_date']

class TestSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    
    class Meta:
        model = Test
        fields = ['id', 'student', 'subject', 'score', 'total_marks', 'date_taken']

class DisciplineRecordSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    
    class Meta:
        model = DisciplineRecord
        fields = ['id', 'student', 'description', 'date', 'action_taken']

class AreaOfImprovementSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    
    class Meta:
        model = AreaOfImprovement
        fields = ['id', 'student', 'subject', 'feedback']