from django.urls import path

from app import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),


    path("blog", views.blog, name="blog"),
    path('blog/<int:id>',views.blogview,name='blogview'),
    path('delblog/<int:id>',views.delblog,name='delblog'),
    # path("createpost", views.blog, name="blog"),
    path('blog_post/',views.blog_post, name='blog_post'),


    path('django',views.login_admin,name='django'),

    path('admin_home',views.admin_home,name='adminhome'),
    
    path('admins',views.admins,name='admins'),
    path('deladmins/<str:id>',views.deladmins,name='deladmins'),
    path('edit-admin/<str:pk>',views.editadmin,name='editadmin'),

    path('employees',views.employees,name='employees'),
    path('delemployees/<str:id>',views.delemployees,name='delemployees'),
    # path('manageemployees',views.manage_emp,name='manage_emp'),



    path('emp_home',views.employee_home,name='emphome'),
    path('cus_home',views.customer_home,name='cushome'),

    
    path('projectcategories',views.projectcategories,name='projectcategories'),
    path('editprojectcategories/<str:pk>',views.editprojectcategories,name='editprojectcategories'),
    path('deleteprojectcategory/<int:id>',views.deleteprojectcategory,name='deleteprojectcategory'),


    path('locations',views.projectlocations,name='locations'),
    path('dellocations/<int:id>',views.delprojectlocations,name='dellocations'),


    path("about", views.about, name="about"),
    path("services", views.services, name="services"),
    path("contact_us", views.contact_us, name="contactus"),
    # path('quotation',views.quotation, name='quotation'),
    
]
