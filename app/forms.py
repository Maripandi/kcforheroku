#from fileinput import FileInput

from dataclasses import field
from statistics import quantiles
from django import forms

from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import *


class CustomUserForm(UserCreationForm):
    username=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter username'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'your@email.com','autocomplete':'off'}))
    first_name=forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the first Name of user'}))
    last_name=forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the last Name of user'}))
    password1=forms.Field(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter the New password'}))
    password2=forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter the password again'}))


class EmployeeProfileForm(CustomUserForm):
    emp_phon=forms.CharField(label='Employee Phone Number',max_length=13,widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter the Emplyee Phone Number'}))
    emp_address=forms.CharField(label='Employee Address', max_length=500,widget=forms.Textarea(attrs={'class':'form-control','rows':3}))
    profile_pic=forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control'}))
    add_to_about=forms.BooleanField(required= False)
    class Meta:
        model=Employee
        fields=(
                'username',
                'email',
                'first_name',
                'last_name',
                'password1',
                'password2',
                'emp_phon',
                'emp_address',
                'profile_pic',
                'add_to_about',
                )



class AdminProfileForm(CustomUserForm):          
    admin_phon=forms.CharField(label='Admin Phone Number',max_length=13,widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter the Admin Phone Number',}))
    admin_address=forms.CharField(label='Admin Address', max_length=500,widget=forms.Textarea(attrs={'class':'form-control','rows':3}))
    profile_pic=forms.FileField(widget=forms.FileInput(attrs={'class':'form-control'}))
    add_to_home=forms.BooleanField(required= False)
    add_to_about=forms.BooleanField(required= False)
    class Meta:
        model=Admin
        fields=(
                'username',
                'email',
                'first_name',
                'last_name',
                'password1',
                'password2',
                'admin_phon',
                'admin_address',
                'profile_pic',
                'add_to_home',
                'add_to_about',

                )


class BlogPostForm(forms.Form): #working
    title=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the title','name':'title'}))
    project=forms.ModelChoiceField(ProjectLocations.objects.filter(is_completed=False), label='Select Project and Location',widget=forms.Select(attrs={'class':'form-control'}))
    site_pic=forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control'}))
    updates=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','rows':3,'placeholder':'Enter the Points'}))

    class Meta:
        model=Blog
        fields=['title',
                'site_pic',
                'updates'
                ]
class ProjectCategoryForm(forms.Form):
    pname=forms.CharField(label='Project Name',max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the new project Name',}))
    ppic=forms.ImageField(label='Project Picture',widget=forms.FileInput(attrs={'class':'form-control'}))
    pdescription=forms.CharField(label='Project Descriptions', max_length=500,widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Enter the short definition of your project','rows':'3'}))
    icon=forms.CharField(label='Paste icon code',max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'copy the from ICONs Code table which blow the Projects',}))
    add_home=forms.BooleanField(
                            label='Are you want to show this project on home page?',
                            widget=forms.RadioSelect(
                                choices=[
                                    (True, 'yes'),
                                    (False, 'No')
                                    ]
                                )
                            )

    class Meta:
        model=ProjectCategory
        fields=[
            'pname',
            'ppic',
            'pdescription',
            'icon',
            'add_home'

        ]

class EditProjectCategoryForm(forms.ModelForm):
    pname=forms.CharField(label='Project Name',max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the new project Name',}))
    ppic=forms.ImageField(label='Project Picture',widget=forms.FileInput(attrs={'class':'form-control'}))
    pdescription=forms.CharField(label='Project Descriptions', max_length=500,widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Enter the short definition of your project','rows':'3'}))


    class Meta:
        model=ProjectCategory
        fields=[
            'pname',
            'ppic',
            'pdescription'

        ]


class ProjectLocationForm(forms.Form): #projectlocations
    # BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
    location=forms.CharField(label='Project Location', max_length=150,widget=forms.TextInput(attrs={'class':'form-control','placeholer':'Enter the project Location'}))
    project=forms.ModelChoiceField(ProjectCategory.objects.all(),label='Select Project Type',widget=forms.Select(attrs={'class':'form-control'}))
    engineer=forms.ModelChoiceField(User.objects.filter(role="EMPLOYEE"),label='Assign Engineer',widget=forms.Select(attrs={'class':'form-control','rows':'3'}))
    site_pic=forms.ImageField(label='Project Picture',widget=forms.FileInput(attrs={'class':'form-control'}))
    is_completed=forms.BooleanField(
        required=False,
        label='This project is completed ?',
        widget=forms.RadioSelect(
            choices=[
                (True, 'Completed'),
                (False, 'Not yet')
                ]
            )
        )
    class Meta:
        model=ProjectLocations
        fields=(
            'location',
            'project',
            'engineer',
            'site_pic',
            'is_completed'
        )

# class QuotationForm(forms.Form):
#     name=forms.CharField(max_length=100, required=False)
#     email=forms.EmailField(required=False)
#     phone=forms.CharField(max_length=13, required=False)
#     service=forms.ModelChoiceField(ProjectCategory.objects.all(),required=False,widget=forms.Select(attrs={'class':'form-control'}))
#     note=forms.CharField(required=False,widget=forms.Textarea(attrs={'class':'form-control','rows':3,'placeholder':'Enter the Points'}))
#     class Meta:
#         model=Quotation
#         fields=(
#             'name',
#             'email',
#             'phone',
#             'service',
#             'note',

#         )

class CustomUserChangeForm(UserChangeForm):
    username=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control border-0','style':'height: 55px;'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','autocomplete':'off'}))
    first_name=forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name=forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))


    class Meta:
        model=User
        fields=(
            'username',
            'email',
            'first_name',
            'last_name',
        )