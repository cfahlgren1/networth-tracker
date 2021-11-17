"""rsb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from registrationsystem.views import CourseViewSet,AdvisorViewSet, EnrollmentSummaryViewSet, GradeReportViewSet, StudentViewSet, AddRequestViewSet, DropRequestViewSet, ProfessorViewSet
from rest_framework import routers

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

# urls for API endpoints
router.register(r'courses', CourseViewSet)
router.register(r'addRequests', AddRequestViewSet)
router.register(r'dropRequests', DropRequestViewSet)
router.register(r'professors', ProfessorViewSet)
router.register(r'students', StudentViewSet)
router.register(r'enrollmentSummaries', EnrollmentSummaryViewSet)
router.register(r'gradeReports', GradeReportViewSet)
router.register(r'advisors', AdvisorViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
