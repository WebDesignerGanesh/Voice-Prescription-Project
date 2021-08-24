"""voice2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blog import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('doctordashboard/',views.doctordashboard,name='doctordashboard'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('addpost/',views.add_post,name='addpost'),
    path('ddashboard/',views.ddashboard,name='ddashboard'),
    path('cust_dashboard/',views.cust_dashboard,name='cust_dashboard'),
    path('updatedata/<int:id>/',views.update_data,name='updatedata'),
    #path('pdf/',views.render_pdf_view,name='test_view'),
    path('pdf/',views.generate_pdf,name='test_view'),
    path('send_mail_plain_with_file/' , views.send_mail_plain_with_file , name='send_mail_plain_with_file')

]
