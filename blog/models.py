from django.db import models

# Create your models here.
class Add_Presciption(models.Model): 
    Username = models.CharField(max_length=750)
    Doctor_name = models.CharField(max_length=750)
    Patient_name = models.CharField(max_length=750)
    age = models.IntegerField()
    gender = models.CharField(max_length=70)
    symptoms  = models.CharField(max_length=750)
    medicines = models.CharField(max_length=750)
    preventions = models.CharField(max_length=750)
    date = models.DateField()

    def __str__(self):
        return self.Patient_name+"taken prescription from"+self.Doctor_name
    

class Patient_Info(models.Model):
    Username = models.CharField(max_length=750)
    First_name = models.CharField(max_length=750)
    Last_name  = models.CharField(max_length=750)
    Email = models.EmailField(max_length=750)
    
       
class Add_Doctor(models.Model):
    name = models.CharField(max_length=750)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=16)
    gender = models.CharField(max_length=10)
    phonenumber = models.IntegerField()
    address = models.CharField(max_length=100)   
    