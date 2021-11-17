from django.contrib import admin
from registrationsystem.models import Course, DropRequest, AddRequest, Professor, Student, GradeReport, EnrollmentSummary, Advisor, StudentClass

# Mass accept requests
@admin.action(description="Accept Request")
def accept_request(modeladmin, request, queryset):
    for request in queryset:
        request.accept_request()  

# Mass deny requests
@admin.action(description="Deny Request")
def deny_request(modeladmin, request, queryset):
    for request in queryset:
        request.deny_request()

# Calculate Bill for Students
@admin.action(description="Calculate Bill")
def calculate_bill(modeladmin, request, queryset):
    for request in queryset:
        request.calculate_bill()

# Generate Enrollment Report
@admin.action(description="Generate Enrollment Report")
def generate_enrollment_report(modeladmin, request, queryset):
    for course in queryset:
        summary = EnrollmentSummary.objects.get_or_create(course=course)[0]
        summary.generate_report()

# Generate Grade Report
@admin.action(description="Generate Grade Report")
def generate_grade_report(modeladmin, request, queryset):
    for course in queryset:
        summary = GradeReport.objects.get_or_create(course=course)[0]
        summary.generate_report()

# Set actions and fields to display in action
class RequestAdmin(admin.ModelAdmin):
    list_display = ['course', 'student']
    actions = [deny_request, accept_request]

# Set Fields for Admin Display for Course
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'crn', 'professor', 'price']
    search_fields = ['name', 'crn']
    actions = [generate_enrollment_report, generate_grade_report]

class BasicAccountAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    search_fields = ['name']

class StudentAdmin(admin.ModelAdmin):
    list_display=['name',]
    actions = [calculate_bill]

class StudentClassAdmin(admin.ModelAdmin):
    list_display=['name', 'grade']

# Register your models to admin site, then you can add, edit, delete and search your models in Django admin site.
admin.site.register(Course, CourseAdmin)
admin.site.register(DropRequest, RequestAdmin)
admin.site.register(AddRequest, RequestAdmin)
admin.site.register(Professor, BasicAccountAdmin)
admin.site.register(Advisor, BasicAccountAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(GradeReport)
admin.site.register(EnrollmentSummary)
admin.site.register(StudentClass, StudentClassAdmin)