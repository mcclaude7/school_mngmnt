from django.contrib import admin
from .models import Student, Teacher, Parent, Course, Enrollment, Attendance, Exam, ExamResult, FeePayment, Timetable, SalaryPayment, Homework, Test, DisciplineRecord, AreaOfImprovement
# Register your models here.

admin.site.register(Student),
admin.site.register(Teacher),
admin.site.register(Parent),
admin.site.register(Course),
admin.site.register(Enrollment),
admin.site.register(Attendance),
admin.site.register(Exam),
admin.site.register(ExamResult),
admin.site.register(FeePayment),
admin.site.register(Timetable),
admin.site.register(SalaryPayment),
admin.site.register(Homework),
admin.site.register(Test),
admin.site.register(DisciplineRecord),
admin.site.register(AreaOfImprovement)
