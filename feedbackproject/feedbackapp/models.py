from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
import datetime

class Customer(models.Model):
    custid = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)  # Increased max length for hashed password
    email = models.EmailField(unique=True)
    mobileno = models.CharField(max_length=15)
    regdate = models.DateTimeField(auto_now_add=True)

    # def save(self, *args, **kwargs):
    #     if self.password:
    #         self.password = make_password(self.password)  # Hash the password before saving
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.custid


class Manager(models.Model):
    managerid = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)  # Increased max length for hashed password
    deptname = models.CharField(max_length=50)
    fullname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    regdate = models.DateTimeField(auto_now_add=True)

    # def save(self, *args, **kwargs):
    #     if self.password:
    #         self.password = make_password(self.password)  # Hash the password before saving
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.fullname


class Feedback(models.Model):
    custid = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Link to Customer
    feeddesc = models.TextField()
    feedrate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])  # Rating system (1-5)
    feeddate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.custid} on {self.feeddate}"


# class Admin(AbstractUser):
#     adminid = models.CharField(max_length=50, unique=True)

#     def __str__(self):
#         return self.adminid

class Admin(models.Model):
    adminid = models.CharField(max_length=50, unique=True)
    fullname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=128)

    # def save(self, *args, **kwargs):
    #     if self.password:
    #         self.password = make_password(self.password)  # Hash the password before saving
    #     super().save(*args, **kwargs)
        
    def __str__(self):
        return self.fullname


class Reply(models.Model):
    custid = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Link to Customer
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)  # Link to Feedback
    managerid = models.ForeignKey(Manager, on_delete=models.CASCADE)  # Link to Manager
    replymessage = models.TextField()
    replydate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply to Feedback {self.feedback.custid} by {self.managerid.fullname}"

