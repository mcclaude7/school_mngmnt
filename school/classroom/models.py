from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    ROLE_CHOICES =[
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Administration'),
        ('staff', 'Staff'),
        ('parent', 'Parent'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profiles/', null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)

class EnrollmentYear(models.Model):  
   # year = models.IntegerField(unique=True)
    year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.year)
    
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrollment_year = models.ForeignKey('EnrollmentYear', on_delete=models.CASCADE, related_name='students', null=True, blank=True)  
    grade = models.CharField(max_length=10)
    student_id = models.CharField(max_length=10, unique=True, blank=True)  # Auto-generated

    def save(self, *args, **kwargs):
        if not self.student_id:
            last_student = Student.objects.filter(enrollment_year=self.enrollment_year).order_by('id').last()
            last_id = int(last_student.student_id[-4:]) + 1 if last_student else 1
            self.student_id = f"{self.enrollment_year.year}{last_id:04d}"  
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student_id} - {self.user.username}"

# Parent Model
class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, related_name='parents')
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()

# Teacher Model
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    subject_specialization = models.CharField(max_length=100)
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.user.get_full_name()

# Staff Model (for non-teaching staff)
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=50)
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.user.get_full_name()

# Course Model
class Course(models.Model):
    course_code = models.CharField(max_length=10, unique=True)
    course_name = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    schedule = models.CharField(max_length=100)

    def __str__(self):
        return self.course_name


# Enrollment Model
class Enrollment(models.Model):
    # Make the year field nullable or provide a default value
    year = models.IntegerField(unique=True, null=True, blank=True)  
    # Option 1: Make it nullable
    # OR
    # year = models.IntegerField(unique=True, default=2025)  # Option 2: Provide a default value
    
    student = models.ManyToManyField('Student', related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(auto_now_add=True)
    grade = models.CharField(max_length=5, null=True, blank=True)

    class Meta:
        permissions = [
            ('can_enroll_students', 'Can enroll students in courses'),
        ]
        constraints = [
            models.UniqueConstraint(fields=['year', 'course'], name='unique_year_course')
        ]

    def __str__(self):
        return f"{self.year} - {self.course.course_name}"

# Attendance Model
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.course.course_name} - {self.date}"

# Class Model
class ClassRoom(models.Model):
    name = models.CharField(max_length=50, unique=True)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

# Exam Model
class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    exam_date = models.DateField()
    total_marks = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.course.course_name} - {self.exam_date}"

# Exam Result Model
class ExamResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    marks_obtained = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.exam.course.course_name} - {self.marks_obtained} Marks"

# Fee Payment Model
class FeePayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    receipt_number = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.amount_paid} on {self.payment_date}"

# Timetable Model
class Timetable(models.Model):
    day_of_week = models.CharField(max_length=10, choices=[
        ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'), ('Friday', 'Friday')
    ])
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    classroom = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.course.course_name} - {self.day_of_week} {self.start_time} - {self.end_time}"

# Salary Payment Model
class SalaryPayment(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)  # Can be a teacher or staff
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=50, choices=[('Bank Transfer', 'Bank Transfer'), ('Cash', 'Cash')])

    def __str__(self):
        return f"{self.employee.get_full_name()} - {self.amount} on {self.payment_date}"
    
class Homework(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="homeworks")
    subject = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()

    def __str__(self):
        return f"Homework: {self.subject} for {self.student}"


class Test(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="tests")
    subject = models.CharField(max_length=100)
    score = models.FloatField()
    total_marks = models.FloatField()
    date_taken = models.DateField()

    def __str__(self):
        return f"Test: {self.subject} - {self.score}/{self.total_marks}"


class DisciplineRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="discipline_records")
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    action_taken = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Discipline: {self.student} - {self.date}"


class AreaOfImprovement(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="improvement_areas")
    subject = models.CharField(max_length=100)
    feedback = models.TextField()

    def __str__(self):
        return f"Improvement: {self.subject} for {self.student}"
   
