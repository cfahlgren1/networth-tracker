from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, DO_NOTHING

# Professor Model
class Professor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrollmentSummaries = models.ManyToManyField('EnrollmentSummary', blank=True)
    gradeReports = models.ManyToManyField('GradeReport', blank=True)

    def __str__(self):
        return self.name

# Course Model
class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    professor = models.ForeignKey(Professor, related_name="courses", on_delete=DO_NOTHING)
    crn = models.IntegerField()
    description = models.TextField(blank=True)
    price = models.FloatField(default=0, blank=False)

    def __str__(self):
        return self.name

# Student Model
class Student(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE) # delete this student account, if user deletes account
    courses = models.ManyToManyField(Course, blank=True)
    bill = models.FloatField(default=0)

    # Calculate bill for student based on classes enrolled in
    def calculate_bill(self):
        amt = 0
        for course in self.courses.all():
            amt += course.price
        self.bill = amt
        self.save()

    def __str__(self):
        return self.name

# Enrollment Summary
class EnrollmentSummary(models.Model):
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    report = models.TextField(blank=True) # list of student names in course

    # Find students that are registered for course and build report
    def generate_report(self):
        course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
        summary = ""
        for student in Student.objects.all():
            for course in student.courses.all():
                if course == self.course:
                    summary += student.name + "\n"
                    break
        self.report = summary
        self.save()

    def __str__(self):
        return self.course.name

# Student Class Model
class StudentClass(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=DO_NOTHING)
    student = models.ForeignKey(Student, related_name="classes", on_delete=DO_NOTHING)
    grade = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.student.name + " - " + self.course.name

# Grade Report
class GradeReport(models.Model):
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    description = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    report = models.TextField(blank=True) # student grades
    
    def generate_report(self):
        summary = ""
        for student in Student.objects.all():
            for course in student.courses.all():
                if course == self.course:
                    # student class
                    summary += student.name + " - " + str(StudentClass.objects.get(student=student, course=self.course).grade) + "\n"
                    break
        self.report = summary
        self.save()
    
    def __str__(self):
        return self.course.name

# Advisor
class Advisor(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE) # delete this student account, if user deletes account

    def __str__(self):
        return self.name

# Drop Request
class DropRequest(models.Model):
    course = models.OneToOneField(Course, on_delete=DO_NOTHING)
    student = models.ForeignKey(Student, on_delete=DO_NOTHING)
    
    # Drop student from course
    def accept_request(self):
        # remove student from course
        self.student.courses.remove(self.course)
        self.student.calculate_bill()

        # delete student class
        student_class = StudentClass.objects.get_or_create(name=self.course.name,course=self.course, student=self.student)[0]
        student_class.delete()

        #remove request when done
        super().delete()
    
    # Deny Request
    def deny_request(self):
        super().delete()
    
    def __str__(self):
        return self.course.name

# Add Request
class AddRequest(models.Model):
    course = models.OneToOneField(Course, on_delete=DO_NOTHING)
    student = models.ForeignKey(Student, on_delete=DO_NOTHING)

    # Add student to course
    def accept_request(self):
        # add student to course
        self.student.courses.add(self.course)
        self.student.calculate_bill()

        # create student class
        student_class = StudentClass.objects.get_or_create(name=self.course.name,course=self.course, student=self.student)[0]
        student_class.save()

        # delete request when done
        super().delete()

    # Delete Request 
    def deny_request(self):
        super().delete()

    def __str__(self):
        return self.course.name