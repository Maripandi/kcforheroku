from django.shortcuts import render, redirect
from app.forms import BlogPostForm,AdminProfileForm,EmployeeProfileForm,ProjectCategoryForm,ProjectLocationForm,EditProjectCategoryForm
from app.models import *
from django.contrib import messages
from http.client import HTTPResponse
from django.contrib.auth import authenticate, login, logout
import os
# Create your views here.


projects=ProjectLocations.objects.all()
pcategory=ProjectCategory.objects.all()
def home(request):
    # projects=ProjectLocations.objects.all()
    # pcategory=ProjectCategory.objects.all()
    context={
        'data1':projects,
        'data3':pcategory
    }
    return render(request, "index.html",context)
# def login_page(request):
#     return render(request,'login.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if (request.method=='POST'):
            user = authenticate(
                                request,
                                username=request.POST.get('username'),
                                password=request.POST.get('password')
                                )
            if user is not None:
                login(request, user)
                if user.role=="ADMIN":
                    messages.success(request,'Admin logged in successfully')
                    return redirect('adminhome')
                elif user.role=="EMPLOYEE":
                    messages.success(request,'Employee logged in successfully')
                    return redirect('emphome')
                elif user.role=="CUSTOMER":
                    messages.success(request,'Customer logged in successfully')
                    return redirect('cushome')
                else:
                    messages.success(request,'invalid user')
            else:
                messages.error(request,'invalid Login credentials')
        return render(request,'registration/login.html')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,'user has been logged out')
    return redirect('login')

def admin_home(request):
    admins=AdminProfile.objects.all().order_by('-user_id')
    context={
        'data':admins
    }
    return render(request,'users/admin/admin_home.html',context)

def admins(request):
    admins=AdminProfile.objects.all().order_by('-user_id')
    if request.method == 'POST':
        form3=AdminProfileForm(request.POST, request.FILES)
        # form=ProfilePicUploadForm(request.POST, request.FILES)
        if form3.is_valid():
            # username=form3.cleaned_data.get('username')
            # password=form3.cleaned_data.get('password1')
            # email=form3.cleaned_data.get('email')
            # e1=Admin.objects.create_user(username=username,password=password,email=email)
            a1=form3.save()
            # print(e1,'form3 saved')
            user=AdminProfile.objects.get(pk=a1.id)
            user.admin_phon=form3.cleaned_data.get('admin_phon')
            user.admin_address=form3.cleaned_data.get('admin_address')
            user.profile_pic=request.FILES.get('profile_pic')
            user.save()
            # print(user,'form saved')
            messages.success(request,'Successfully added Admin')
            return redirect('admins')
        else:
            # print('Form error : ',form.errors)
            # print("Form 3 error : ",form3.errors)
            messages.error(request,'Failed to add admin')
    else:
        form3 = AdminProfileForm()
        # form=ProfilePicUploadForm()
    context={
        'data3':form3,
        'data':admins
         }
    return render(request,'users/admin/admins.html',context)

def editadmin(request, id):
    return render(request,'editadmin.html')

def deladmins(request,id):
    delusr=User.objects.get(id=id)
    delpic=AdminProfile.objects.get(pk=id)
    os.remove(delpic.profile_pic.path)
    delusr.delete()
    messages.success(request,'User Deleted')
    return redirect('admins')

def employees(request):
    employeesdetails=EmployeeProfile.objects.all().order_by('-user_id')
    if request.method == 'POST':
        form2=EmployeeProfileForm(request.POST, request.FILES)
        if form2.is_valid():
            # e1=Employee.objects.create_user(
            #     username=form2.cleaned_data.get('username'),
            #     email=form2.cleaned_data.get('email'),
            #     first_name=form2.cleaned_data.get('first_name'),
            #     last_name=form2.cleaned_data.get('last_name'),
            #     password=form2.cleaned_data.get('password1')
            # )
            e1=form2.save()
            # print(e1,'form2 saved')
            user=EmployeeProfile.objects.get(pk=e1.id)
            user.emp_phon=form2.cleaned_data.get('emp_phon')
            user.emp_address=form2.cleaned_data.get('emp_address')
            user.profile_pic=request.FILES.get('profile_pic')
            user.save()
            messages.success(request,'Successfully added Employee')
            return redirect('employees')
        else:
            # print('Form error : ',form.errors)
            # print("Form 2 error : ",form2.errors)
            messages.error(request,'somthing went wrong') 
    else:
        # form = CustomUserForm()
        form2 = EmployeeProfileForm()
        # form3 = AdminProfileForm()
    context={
            # 'data':form,
            'data2':form2,
            'data3':employeesdetails
              } #'data3':form3
    return render(request,'users/admin/employees.html',context)

def delemployees(request,id):
    delusr=User.objects.get(id=id)
    delpic=EmployeeProfile.objects.get(pk=id)
    os.remove(delpic.profile_pic.path)
    delusr.delete()
    messages.success(request,'User Deleted')
    return redirect('employees')

def projectcategories(request):
    # projects=ProjectCategory.objects.all()
    if request.method == 'POST':
        form=ProjectCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            s1=ProjectCategory.objects.create(
                pname=form.cleaned_data.get('pname'),
                ppic=request.FILES.get('ppic'),
                pdescription=form.cleaned_data.get('pdescription'),
                icon=form.cleaned_data.get('icon'),
                add_home=form.cleaned_data.get('add_home'),
            )
            s1.save()
            messages.success(request,'success')
        else:
            # print('Form error : ',form.errors)
            messages.error(request,'error')
    else:
        form=ProjectCategoryForm()
    context={
        
        'd2':form,
        'd1':pcategory
    }
    return render(request,'users/admin/projects.html',context)

def editprojectcategories(request,id):
    projects=ProjectCategory.objects.get(id=id)
    # initial={
    #     'pname':projects.pname,
    #     'ppic':projects.ppic,
    #     'pdescription':projects.pdescription
    # }
    if request.method == 'POST':
        form=ProjectCategoryForm(
            request.POST or None, 
            request.FILES, 
            # initial=initial
            instance=projects
            )
        if form.is_valid():
            # form.save()
            s1=ProjectCategory.objects.get(id=id)
            s1.pname=form.cleaned_data.get('pname'),
            s1.ppic=request.FILES.get('ppic'),
            s1.pdescription=form.cleaned_data.get('pdescription')
            
            s1.save()
            messages.success(request,'success')
        else:
            # print('Form error : ',form.errors)
            messages.error(request,'error')
    else:
        form=EditProjectCategoryForm()
    context={
        
        'd2':form,
        'd1':projects
    }
    return render(request,'users/admin/editprojects.html',context)

def deleteprojectcategory(request,id):
    projects=ProjectCategory.objects.get(id=id)
    os.remove(projects.ppic.path)
    projects.delete()
    messages.success(request,'deleted')
    return redirect('projectcategories')

def projectlocations(request): #projectlocations
    # cproject=ProjectLocations.objects.all()
    if request.method == 'POST':
        form=ProjectLocationForm(request.POST, request.FILES)
        if form.is_valid():
            l1=ProjectLocations.objects.create(
                location=form.cleaned_data.get('location'),
                project=form.cleaned_data.get('project'),
                engineer=form.cleaned_data.get('engineer'),
                is_completed=form.cleaned_data.get('is_completed'),
                site_pic=request.FILES.get('site_pic')
            )
            l1.save()
            messages.success(request,"success")
        else:
            messages.error(request,'Error')
    else:
        form=ProjectLocationForm()

    context={
        'd1':projects,
        'd2':form
    }
    return render(request,'users/admin/locations.html',context)

def delprojectlocations(request, id):
    projects=ProjectLocations.objects.get(id=id)
    os.remove(projects.site_pic.path)
    projects.delete()
    messages.success(request,'deleted')
    return redirect('locations')

def employee_home(request):
    return render(request,'users/emp/emp_home.html')

def customer_home(request):
    return render(request,'users/custmr/cus_home.html')


def blog_post(request):
    if request.method=='POST':
        myform=BlogPostForm(request.POST,request.FILES)
        if myform.is_valid():

            b1=Blog.objects.create(
                                    title=myform.cleaned_data.get('title'),
                                    category=myform.cleaned_data.get('project'),
                                    site_pic=request.FILES.get('site_pic'),
                                    updates=myform.cleaned_data.get('updates'),
                                    posted_by=request.user
                                    )
            b1.save()
            s1=ProjectLocations.objects.get(pk=b1.category.id)
            os.remove(s1.site_pic.path)
            s1.site_pic=request.FILES.get('site_pic')
            s1.save()
            messages.success(request,'Your blog posted successfully')
            return redirect ('blog')
        else:
            print(myform.errors)
            print("error")
            messages.error(request,'Somthing went wrong!')
            return redirect('blog')

def blog(request):
    myform=BlogPostForm()
    if request.method=='GET':
        post=Blog.objects.all().order_by('-id')
        # projects=ProjectCategory.objects.all()
        context={
            'data':post,
            'data2':myform,
            'data3':pcategory
        }
        return render(request, "blog.html",context)
def delblog(request,id):
    post=Blog.objects.get(id=id)
    os.remove(post.site_pic.path)
    post.delete()
    messages.success(request,'deleted')
    return redirect('blog')

def blogview(request,id):
    projects=ProjectLocations.objects.get(pk=id)
    post=Blog.objects.filter(category_id=id)
    context={
        'data':post,
        'data2':projects
    }
    return render(request,'blogview.html',context)



def contact_us(request):

    return render(request, "contactus.html")


def about(request):
    return render(request, "about.html")


def services(request):
    # services=ProjectCategory.objects.all()
    context={
        'data1':pcategory
    }
    return render(request, "services.html",context)


def login_admin(request): #django admin
    return redirect("/admin/")
