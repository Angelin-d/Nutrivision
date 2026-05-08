from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class User_table(models.Model):
    LOGIN = models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    age=models.IntegerField()
    gender=models.CharField(max_length=100)
    image=models.FileField()
    # phone=models.BigIntegerField()
    # pin=models.IntegerField()
    # # post=models.CharField(max_length=100)
    # place=models.CharField(max_length=100)
    # district=models.CharField(max_length=100)



class dataset(models.Model):

    question=models.TextField()
    answer=models.TextField()


class tips_table(models.Model):
    title=models.CharField(max_length=100)
    tip=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    date=models.DateField()

class Feedback_table(models.Model):
    USER=models.ForeignKey(User_table,on_delete=models.CASCADE)
    feedback=models.CharField(max_length=100)
    rating=models.CharField(max_length=100)
    date=models.DateField()

class PredictionHistory(models.Model):
    USER=models.ForeignKey(User_table,on_delete=models.CASCADE)
    precondition=models.CharField(max_length=100)
    result=models.CharField(max_length=100)
    suggestion =models.TextField()
    confidence =models.FloatField()
    image=models.FileField()
    date=models.DateField()

class personaldetails(models.Model):
    USER = models.ForeignKey(User_table, on_delete=models.CASCADE)
    healthconditions=models.CharField(max_length=100)
    dietry_prefer=models.CharField(max_length=100)
    # bmi=models.CharField(max_length=100)
    allergies=models.CharField(max_length=100)
    supplements_taken=models.CharField(max_length=100)
    smoking_habit=models.CharField(max_length=100)
    alcohol_consumption =models.CharField(max_length=100)
    physical_conditions=models.CharField(max_length=100)
    # medical_history=models.CharField(max_length=100)
    height =models.IntegerField()
    weight =models.IntegerField()
    image=models.FileField()



