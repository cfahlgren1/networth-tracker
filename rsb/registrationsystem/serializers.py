from rest_framework import serializers, viewsets
from registrationsystem.models import Course, Advisor, StudentClass, EnrollmentSummary, GradeReport, Professor, Student, DropRequest, AddRequest

# Serializers define the API representation.
class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'professor', 'crn', 'description', 'price']

    professor = serializers.CharField(source='professor.name')

class ProfessorSerializer(serializers.HyperlinkedModelSerializer):
    courses = serializers.StringRelatedField(many=True)

    class Meta:
        model = Professor
        fields = ['id','name', 'courses']
    

class DropRequestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DropRequest
        fields = ['course', 'student']
    
    course = serializers.CharField(source='course.name')
    student = serializers.StringRelatedField()

class AddRequestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AddRequest
        fields = ['course', 'student']
    
    course = serializers.CharField(source='course.name')
    student = serializers.StringRelatedField()

class StudentClassSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StudentClass
        fields = ['name', 'grade']

class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'classes']
    
    classes = StudentClassSerializer(many=True, read_only=True)

class EnrollmentSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EnrollmentSummary
        fields = ["course", "description", "date_created", "report"]

class GradeReportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GradeReport
        fields = ["course", "description", "date", "report"]

class AdvisorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Advisor
        fields = ["name"]