"""
URL configuration for school project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from classroom.views import (
    UserViewSet, StudentViewSet, TeacherViewSet, ParentViewSet, CourseViewSet,
    EnrollmentViewSet, AttendanceViewSet, ExamViewSet, ExamResultViewSet,
    FeePaymentViewSet, TimetableViewSet, SalaryPaymentViewSet, HomeworkViewSet,
    TestViewSet, DisciplineRecordViewSet, AreaOfImprovementViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'students', StudentViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'parents', ParentViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'attendance', AttendanceViewSet)
router.register(r'exams', ExamViewSet)
router.register(r'exam-results', ExamResultViewSet)
router.register(r'fee-payments', FeePaymentViewSet)
router.register(r'timetable', TimetableViewSet)
router.register(r'salary-payments', SalaryPaymentViewSet)
router.register(r'homework', HomeworkViewSet)
router.register(r'tests', TestViewSet)
router.register(r'discipline-records', DisciplineRecordViewSet)
router.register(r'area-of-improvement', AreaOfImprovementViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]
