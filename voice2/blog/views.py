from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from .forms import SignUpForm,LoginForm,User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Add_Presciption,Patient_Info
from django.contrib.auth.models import Group
from django.views.generic import ListView
from xhtml2pdf import pisa
from django.template import Context
from django.template.loader import get_template


# Create your views here.
# Home
def home(request):
    return render(request,'blog/home.html')

# About
def about(request):
    return render(request,'blog/about.html')    

# Contact
def contact(request):
    return render(request,'blog/contact.html')    

def cust_dashboard(request):
    if request.user.is_authenticated:
        if request.method == "POST":
          form = SignUpForm(request.POST)
          if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']

            pst = Patient_Info(username=username,first_name=first_name,last_name=last_name,email=email)
            pst.save()
            form = SignUpForm()
        else:
            form = SignUpForm()    
        return render(request,'blog/cust_dashboard.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')   
    

# Dashboard
def dashboard(request):
    if request.user.is_authenticated:
        presciption = Add_Presciption.objects.filter(Username=request.user).order_by("-id")
        user = request.user
        full_name = user.get_full_name()
        gps =user.groups.all()
        return render(request,'blog/dashboard.html',{'presciption':presciption,'full_name':full_name,'groups':gps}) 
    else:
        return HttpResponseRedirect('/login/')

def ddashboard(request):
    if request.user.is_authenticated:
        presciption = Add_Presciption.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request,'blog/ddashboard.html',{'presciption':presciption,'full_name':full_name,'groups':gps})
    else:
        return HttpResponseRedirect('/login/')    

def doctordashboard(request):
    if request.user.is_authenticated:
        presciption = Add_Presciption.objects.filter(Doctor_name=request.user).order_by("-id")
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request,'blog/doctordashboard.html',{'presciption':presciption,'full_name':full_name,'groups':gps})
    else:
        return HttpResponseRedirect('/login/')         



#Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')          

#SignUp
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congralutions!!You have successfully signed in..')
            user = form.save()
            group = Group.objects.get(name='Patients')
            user.groups.add(group)
    else:        
     form = SignUpForm()
    return render(request,'blog/signup.html',{'form':form}) 

#Login
def user_login(request):
  if not request.user.is_authenticated:
    if request.method == "POST":
        form =  LoginForm(request=request, data=request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            upass = form.cleaned_data['password']
            user = authenticate(username=uname,password=upass)
            if user is not None:
                login(request,user)
                messages.success(request,'Logged in Successfully!!')
                if user.is_superuser:
                 return HttpResponseRedirect('/ddashboard/')
                elif user.is_staff:
                    return HttpResponseRedirect('/doctordashboard/') 
                else:
                 return HttpResponseRedirect('/dashboard/')
 
    else:
     form = LoginForm()
    return render(request,'blog/login.html',{'form':form}) 
  else:
    return HttpResponseRedirect('/ddashboard/')  

# Add new post 
def add_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
         Username = request.POST["Username"]   
         Doctor_name = request.POST["Doctor_name"]
         Patient_name = request.POST["Patient_name"]
         age = request.POST["age"]
         gender = request.POST["gender"]
         symptoms = request.POST["symptoms"]
         medicines = request.POST["medicines"]
         preventions = request.POST["preventions"]
         date  = request.POST["date"]

         data = Add_Presciption(Username=Username,Doctor_name=Doctor_name,Patient_name=Patient_name,age=age,gender=gender,symptoms=symptoms,medicines=medicines,preventions=preventions,date=date)
         data.save()
        return render(request,'blog/index.html')
    else:
        return HttpResponseRedirect('/login/')

# def render_pdf_view(request):
#     template_path = 'blog/test_view.html'
#     presciption = Add_Presciption.objects.filter(Username=request.user).order_by("-id")
#     context = {'myvar': presciption}
#     response = HttpResponse(content_type='application/pdf')
#   #return render(request,'blog/test_view.html',context)
#     #if download :
#     #response['Content-Disposition']='attachment; filename="report.pdf"'
#     #if only display:
#     response['Content-Disposition']='filename="report.pdf"'
#     template = get_template(template_path)
#     html = template.render(context)

#     pisa_status = pisa.CreatePDF(
#         html, dest=response)
#     if pisa_status.err:
#         return HttpResponse('We had some errors<pre>'+ html + '</pre>')
#     return response
#     #presciption = Add_Presciption.objects.filter(Username=request.user).order_by("-id")

def generate_pdf(request):
    presciption = Add_Presciption.objects.filter(Doctor_name=request.user).order_by('-id')[:1]
    user = request.user
    data={'var':presciption}
    template = get_template('blog/test_view.html')
    html = template.render(data)
    file = open('report.pdf',"w+b")
    pisaStatus = pisa.CreatePDF(html.encode('utf-8'),dest=file,encoding='utf-8')
    file.seek(0)
    pdf = file.read()
    file.close()
    return HttpResponse(pdf,'application/pdf')

def update_data(request,id):
  if request.user.is_authenticated:  
    if request.method == 'POST':
        pi = User.objects.get(pk=id)
        fm = SignUpForm(request.POST, instance=pi)
        if fm.is_valid():
            fm.save()
    else:
         pi = User.objects.get(pk=id)
         fm = SignUpForm(instance=pi)
    return render(request,'blog/updatedata.html',{'form':fm}) 
  else:
       return HttpResponseRedirect('/login/')


from voice2 import settings
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail, EmailMessage
from voice2.settings import EMAIL_HOST_USER

def send_mail_plain_with_file(request):
    if request.method == 'POST' :
        message = request.POST.get('message', '')
        subject = request.POST.get('subject', '')
        mail_id = request.POST.get('email', '')
        email = EmailMessage(subject, message, EMAIL_HOST_USER, [mail_id])
        email.content_subtype = 'html'

        file = request.FILES['pdf']
        email.attach(file.name, file.read(), file.content_type)

        email.send()
        return HttpResponseRedirect('/')
    return render(request , 'blog/emailattchment.html')

    





