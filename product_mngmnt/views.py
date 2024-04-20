from django.shortcuts import render,redirect
from product_mngmnt.models import *
from django.http import HttpResponse
from django.http import JsonResponse
from .urls import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from product_mngmnt.forms import UserForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def view_index(request):
    return render(request, 'product_mngmnt/index.html')


def view_signup(request):
    if request.method=='GET':
        frm_unbound=UserForm()
        d1={'form':frm_unbound}
        resp=render(request,'product_mngmnt/signup.html',context=d1)
        return resp
    elif request.method=='POST':
        frm_bound=UserForm(request.POST)
        if frm_bound.is_valid():  # Server Side Validation
            u=frm_bound.save()
            # u.set_password(u.password)
            u.save()
            user=UserDetail()
            user.mobile_number=request.POST.get('mobileno','NA')
            user.email=request.POST.get('email','NA')
            user.name= request.POST.get('name','NA')
            user.user=u
            user.save()
            messages.success(request, "Congrats , Account created !")
            return redirect('login')
        else:
            d1={'form':frm_bound}
            resp=render(request,'product_mngmnt/signup.html',context=d1)
            return resp  
  


def view_login(request):
    if request.method=='GET':
        resp=render(request,'product_mngmnt/login.html')
        return resp
    elif request.method=='POST':
        u_name=request.POST.get('username','NA')
        u_paswd=request.POST.get('password','NA')
        user=authenticate(request,username=u_name,password=u_paswd)
        if user is not None:
            login(request,user)
            return render(request,'product_mngmnt/home.html')
            # return HttpResponse("<h1>Login SuccessFully!!</h1>")
        else:
            # return HttpResponse("<h1>Login Failed!!</h1>")
            messages.success(request, " Please enter valid details ")
            return render(request,'product_mngmnt/login.html')
        
def view_logout(request):
    logout(request=request)
    resp=render(request,'product_mngmnt/home.html')
    return resp

def view_forget(request):
    if request.method == 'GET':
        return render(request,'product_mngmnt/forget.html')
    elif request.method == 'POST':
        u_name= request.POST.get('username','NA')
        u=User.objects.get(username=u_name)
        print(u)
        if u is not None:
            u_passwd = request.POST.get('password','NA')
            u.set_password(u_passwd)
            u.save()
            messages.success(request, "Congrats , Password changed !")
            return redirect('login')
        else :
            return render(request,'product_mngmnt/forget.html')


        



def view_home(request):
    if request.method == 'GET':
        return render(request,'product_mngmnt/home.html')
    elif request.method == 'POST':
        tofind = request.POST.get('search','NA')
        if "btnsubmit" in request.POST:
                p=Product()
                prod=Product.objects.filter(detail__contains=tofind)    
                # if  request.user.is_authenticated:
                return render(request,'product_mngmnt/request.html',context={"prod":prod})
                # else:
                #     return redirect('login')
        elif "btnVisitor" in request.POST:
            v=Visitor()
            v.name=request.POST.get('txtname','NA')
            v.mobile_number=int(request.POST.get('txtmobile',0))
            v.save()
            return render(request,'product_mngmnt/home.html')


    
def view_desc(request,pk):
    prod=Product.objects.filter(id=pk).first()
    if prod:
        return render(request,"product_mngmnt/desc.html",context={"prod":prod})
    else:
        return redirect('/')
    
# @login_required(login_url='login')
def view_thermo(request):
    if request.method == 'GET':
        section = "Thermopatch"
        prod=Product.objects.filter(detail__contains="thermopatch parts")   
        return render(request,'product_mngmnt/request.html',context={"prod":prod,"section":section})

# @login_required(login_url='login')
def view_marking(request):
    if request.method == 'GET':
        section = "Marking"
        prod=Product.objects.filter(detail__contains="marking consumable")   
        return render(request,'product_mngmnt/request.html',context={"prod":prod ,"section":section})
    
# @login_required(login_url='login')    
def view_flatwork(request):
    if request.method == 'GET':
        section = "Flat Work Ironer"
        prod=Product.objects.filter(detail__contains="flat")   
        return render(request,'product_mngmnt/request.html',context={"prod":prod,"section":section})

# @login_required(login_url='login')    
def view_padscovers(request):
    if request.method == 'GET':
        section = "Pads and covers"
        prod=Product.objects.filter(detail__contains="pads")   
        return render(request,'product_mngmnt/request.html',context={"prod":prod ,"section":section})

# @login_required(login_url='login')
def view_drainvalve(request):
    if request.method == 'GET':
        section = "Drain Valve"
        prod=Product.objects.filter(detail__contains=" drain valve")   
        return render(request,'product_mngmnt/request.html',context={"prod":prod ,"section":section})

# @login_required(login_url='login')
def view_drycleaning(request):
    if request.method == 'GET':
        section = "Dry Cleaning Parts"
        prod=Product.objects.filter(detail__contains="dry cleaning part")   
        return render(request,'product_mngmnt/request.html',context={"prod":prod ,"section":section})

# @login_required(login_url='login')    
def view_speedqueen(request):
    if request.method == 'GET':
        section = "Speed queen"
        prod=Product.objects.filter(detail__contains="speed queen")   
        return render(request,'product_mngmnt/request.html',context={"prod":prod ,"section":section})

# @login_required(login_url='login')    
def view_thermopatch(request):
    if request.method == 'GET':
        section = "Thermopatch"
        prod=Product.objects.filter(detail__contains="thermopatch")   
        return render(request,'product_mngmnt/request.html',context={"prod":prod ,"section":section})
    
def view_image(request):
    if request.method == 'GET':
        section = "IMAGE"
        prod=Product.objects.filter(detail__contains="image")   
        return render(request,'product_mngmnt/request.html',context={"prod":prod ,"section":section})

# @login_required(login_url='login')    
def view_forenta_parts(request):
    if request.method == 'GET':
        section = "Forenta Parts"
        prod=Product.objects.filter(detail__contains="forenta parts")   
        return render(request,'product_mngmnt/request.html',context={"prod":prod ,"section":section})

# @login_required(login_url='login')    
def view_hoffman_parts(request):
    if request.method == 'GET':
        section = "Hoffman Parts"
        prod=Product.objects.filter(detail__contains="hoffman parts")   
        return render(request,'product_mngmnt/request.html',context={"prod":prod ,"section":section})

# @login_required(login_url='login')    
def view_milnor_parts(request):
    if request.method == 'GET':
        section = "Milnor Parts"
        prod=Product.objects.filter(detail__contains="milnor parts")   
        return render(request,'product_mngmnt/request.html',context={"prod":prod ,"section":section})

# Equipment dropdown view 

# @login_required(login_url='login')
def view_washer_extractor(request):
    if request.method == 'GET':
        section = "Washer Extractor"
        prod=Product.objects.filter(detail__contains="washer extractor")   
        return render(request,'product_mngmnt/request.html',context={"prod":prod ,"section":section})

# @login_required(login_url='login')
def view_dryer(request):
    if request.method == 'GET':
        section = "Dryer"
        prod=Product.objects.filter(detail__contains="tumbler dryer")   
        return render(request,'product_mngmnt/request.html',context={"prod":prod ,"section":section})

# @login_required(login_url='login')
def view_roll_heated_flat_work_ironer(request):
    if request.method == 'GET':
        section = "Roll Heated Ironer"
        prod=Product.objects.filter(detail__contains="roll heated")   
        return render(request,'product_mngmnt/request.html',context={"prod":prod ,"section":section})

# @login_required(login_url='login')
def view_chest_heated_flat_work_ironer(request):
    if request.method == 'GET':
        section = "Chest Heated Ironer"
        prod=Product.objects.filter(detail__contains="Chest Heated")   
        return render(request,'product_mngmnt/request.html',context={"prod":prod ,"section":section})

# @login_required(login_url='login')    
def view_marking_machine(request):
    if request.method == 'GET':
        section = "Marking Machine"
        prod=Product.objects.filter(detail__contains="marking machine")   
        return render(request,'product_mngmnt/request.html',context={"prod":prod,"section":section})

# @login_required(login_url='login')
def view_dry_cleaning_machines(request):
    if request.method == 'GET':
        section = "Dry Cleaning Machine"
        prod=Product.objects.filter(detail__contains="dry cleaning machine")   
        return render(request,'product_mngmnt/request.html',context={"prod":prod,"section":section})

# @login_required(login_url='login')
def view_finishing_machines(request):
    if request.method == 'GET':
        section = "Finishing Machine"
        prod=Product.objects.filter(detail__contains="Finishing equipment")   
        return render(request,'product_mngmnt/request.html',context={"prod":prod,"section":section})
    





# new
# kitchen appliances

def view_kitchen_appliances(request):
    if request.method == 'GET':
        section = "Kitchen accessories"
        prod=Product.objects.filter(detail__contains="kitchen")   
        return render(request,'product_mngmnt/request.html',context={"prod":prod ,"section":section})













def view_disclaimer(request):
    if request.method=='GET':
        return render(request,'product_mngmnt/disclaimer.html')        

def view_about(request):
    if request.method == 'GET':
        return render(request,'product_mngmnt/aboutus.html')

def view_service(request):
    if request.method == 'GET':
        return render(request,'product_mngmnt/services.html')

def view_sitemap(request):
    if request.method == 'GET':
        return render(request,'product_mngmnt/sitemap_index.xml')
    
def view_robots(request):
    if request.method == 'GET':
        return render(request,'product_mngmnt/Robots.txt')