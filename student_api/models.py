from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Course(models.Model):
    title=models.CharField(max_length=100)
    duration=models.CharField(max_length=50, default="3 months")
    about_course=models.TextField()
    price=models.DecimalField(max_digits=10, decimal_places=2)
    start_date=models.DateField()
    end_date=models.DateField()


    def __str__(self):
        return self.title
    

class Student(models.Model):
    class GenderChoice(models.TextChoices):
        Female="F", _("female"),
        Male="M", _("Male")
    names=models.CharField(max_length=100)
    age=models.PositiveIntegerField()
    gender=models.CharField(max_length=5, choices=GenderChoice.choices)
    email=models.EmailField(max_length=100)

    def __str__(self):
        return self.names


class Admission(models.Model):
    student=models.ForeignKey(Student, on_delete=models.CASCADE)
    course=models.ForeignKey(Course, on_delete=models.CASCADE)
    is_paid=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.names} registered"



class Instructor(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    course=models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
