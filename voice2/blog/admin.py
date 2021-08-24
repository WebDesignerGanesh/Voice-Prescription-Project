from django.contrib import admin
from blog.models import Add_Presciption,Patient_Info,Add_Doctor
# Register your models here.
@admin.register(Add_Presciption)
class PresciptionModelAdmin(admin.ModelAdmin):
    list_display = ['id','Username','Doctor_name','Patient_name','age','gender','symptoms','medicines','preventions','date']

@admin.register(Patient_Info)
class PatientModelAdmin(admin.ModelAdmin):
    list_display = ['id','Username','First_name','Last_name','Email']    

admin.site.register(Add_Doctor)