from django.shortcuts import render
from registrationsystem.models import Course, Advisor, Student, Professor, AddRequest, DropRequest, GradeReport, EnrollmentSummary
from registrationsystem.serializers import CourseSerializer, AdvisorSerializer, ProfessorSerializer, AddRequestSerializer, DropRequestSerializer, StudentSerializer, GradeReportSerializer, EnrollmentSummarySerializer
from rest_framework import viewsets

# ViewSets define the view behavior.
class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

# Read Only View of Professors because they will be created / updated through Admin
class ProfessorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer

# ModelViewSet for AddRequest because they may be created through POST request
class AddRequestViewSet(viewsets.ModelViewSet):
    queryset = AddRequest.objects.all()
    serializer_class = AddRequestSerializer

# ModelViewSet for DropRequest because they may be created through POST request
class DropRequestViewSet(viewsets.ModelViewSet):
    queryset = DropRequest.objects.all()
    serializer_class = DropRequestSerializer

# Read Only View of Students because they will be created / updated through Admin
class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

# Read Only View of Grade Reports because they will be created / updated through Admin
class GradeReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GradeReport.objects.all()
    serializer_class = GradeReportSerializer

# Read Only View of Enrollment Summaries because they will be created / updated through Admin
class EnrollmentSummaryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EnrollmentSummary.objects.all()
    serializer_class = EnrollmentSummarySerializer

# Read Only View of Advisors because they will be created / updated through Admin
class AdvisorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Advisor.objects.all()
    serializer_class = AdvisorSerializer