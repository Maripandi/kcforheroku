


from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
import os
from django.utils.translation import gettext_lazy as _

def getFileName(request,filename):
    now_time=datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    new_filename="%s%s"%(now_time,filename)
    return os.path.join('uploads/',new_filename)

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN='ADMIN','Admin'
        EMPLOYEE='EMPLOYEE','Employee'
        CUSTOMER='CUSTOMER','Customer'

    base_role=Role.ADMIN

    role=models.CharField(max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role=self.base_role
            return super().save(*args, **kwargs)

class AdminManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results=super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.ADMIN)

class EmployeeManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.EMPLOYEE)

class CustomerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.CUSTOMER)

class Admin(User):
    base_role=User.Role.ADMIN
    admin=AdminManager()
    class Meta:
        proxy=True
    
    def welcome(self):
        return 'Here only for Admin'

class Employee(User):
    base_role=User.Role.EMPLOYEE
    employee=EmployeeManager()
    class Meta:
        proxy=True
    
    def welcome(self):
        return 'here only for employee'


class Customer(User):
    base_role=User.Role.CUSTOMER
    customer=CustomerManager()
    class Meta:
        proxy=True

    def welcome(self):
        return 'here only for Customer'
    

class AdminProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    admin_phon=models.CharField(max_length=13,null=True,blank=False)
    profile_pic=models.ImageField(upload_to=getFileName,null=True,blank=True)
    admin_address= models.TextField(max_length=300,null=True,blank=False)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=Admin)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "ADMIN":
        AdminProfile.objects.create(user=instance)

class EmployeeProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    emp_phon=models.CharField(max_length=13,null=True,blank=False)
    profile_pic=models.ImageField(upload_to=getFileName,null=True,blank=True)
    emp_address= models.TextField(max_length=300,null=True,blank=False)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=Employee)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "EMPLOYEE":
        EmployeeProfile.objects.create(user=instance)

class CustomerProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    emp_phon=models.CharField(max_length=13,null=True,blank=False)
    # profile_pic=models.ImageField(upload_to=getFileName,null=True,blank=True)
    emp_address= models.TextField(max_length=300,null=True,blank=False)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=Customer)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "CUSTOMER":
        CustomerProfile.objects.create(user=instance)

class ProjectCategory(models.Model):
    pname=models.CharField('Project Name', max_length=50,null=False,blank=False)
    ppic=models.ImageField(upload_to=getFileName,null=True,blank=True)
    pdescription=models.TextField(max_length=500)
    icon=models.CharField('Icon', max_length=50,null=True,blank=False)
    add_home=models.BooleanField(null=True,blank=False)

    class Meta:
        verbose_name = _("Project Category")
        verbose_name_plural = _("Project Categories")

    def __str__(self):
        return self.pname

class ProjectLocations(models.Model):
    location=models.CharField(max_length=50,null=True,blank=False)
    project=models.ForeignKey(ProjectCategory, on_delete=models.CASCADE)
    site_pic=models.ImageField(upload_to=getFileName,null=True,blank=False)
    engineer=models.ForeignKey(Employee, on_delete=models.CASCADE)
    is_completed=models.BooleanField(null=True,blank=False)

    def __str__(self):
        # return f'{self.project.pname}'+ ' at '+ f'{self.location}'
        return self.project.pname + ' work at '+ self.location



class Blog(models.Model):
    title=models.CharField(max_length=100)
    category=models.ForeignKey(ProjectLocations, on_delete=models.CASCADE) 
    site_pic=models.ImageField(upload_to=getFileName,null=True,blank=False)
    updates= models.TextField(max_length=500,null=True,blank=False)
    posted_by=models.ForeignKey(User, on_delete=models.CASCADE,related_name='posted_by_user',null=True,blank=True) #for same type of foreign key we should use 'related_name'
    updated_by=models.ForeignKey(User, on_delete=models.CASCADE,related_name='updated_by_user',null=True,blank=True) #for same type of foreign key we should use 'related_name'
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

##ORM##
# (Kalam-Venv) PS C:\Kalam Construction\KalamConstruction\Project\Kalamconst> python manage.py shell
# >>> from app.models import *
# >>> Customer.objects.create_user(username='cus1',password='ssk67')
# <Customer: cus1>
# >>> Employee.objects.create_user(username='emp1',password='ou88700',email='emp1@gm.com')
# <Employee: emp1>


#admin
#Ad@pass1




