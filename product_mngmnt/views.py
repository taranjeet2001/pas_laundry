from django.shortcuts import render,redirect
from product_mngmnt.models import *
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from product_mngmnt.forms import UserForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.


class ProductCatalog:
    """
    Domain service implementing Single Responsibility Principle (SRP)
    for querying, filtering, and ordering products cleanly.
    """

    @staticmethod
    def normalize_name(value):
        """Clean and normalize whitespace in names and brand strings."""
        return " ".join((value or "").split())

    @classmethod
    def get_brand_parts(cls, brand_name):
        """Fetch parts specific to a brand."""
        brand = cls.normalize_name(brand_name)
        return (
            Product.objects.filter(brand__iexact=brand, detail__icontains="part")
            .order_by("name")
        )

    @classmethod
    def get_brand_consumables(cls, brand_name):
        """Fetch consumables specific to a brand."""
        brand = cls.normalize_name(brand_name)
        return (
            Product.objects.filter(brand__iexact=brand)
            .filter(
                Q(detail__icontains="consumable")
                | Q(detail__icontains="marking")
                | Q(detail__icontains="pads")
                | Q(detail__icontains="flat")
            )
            .order_by("name")
        )

    @classmethod
    def get_brand_washer_controllers(cls, brand_name):
        """Fetch washer controller products specific to a brand."""
        brand = cls.normalize_name(brand_name)
        return (
            Product.objects.filter(
                brand__iexact=brand,
                detail__icontains="washer controller",
            )
            .order_by("name")
        )

    @classmethod
    def get_washer_controllers(cls, brand=None):
        """Fetch washer controller products, optionally filtered by brand."""
        qs = Product.objects.filter(detail__icontains="washer controller")
        if brand:
            clean_brand = cls.normalize_name(brand)
            if clean_brand:
                qs = qs.filter(brand__iexact=clean_brand)
        return qs.order_by("name")

    @classmethod
    def filter_by_keywords(cls, *keywords, brand=None):
        """
        Query products matching one or more detail keywords (case-insensitive OR).
        Optionally filters by brand.
        """
        if not keywords:
            qs = Product.objects.all()
        else:
            query = Q()
            for kw in keywords:
                cleaned = (kw or "").strip()
                if cleaned:
                    query |= Q(detail__icontains=cleaned)
            qs = Product.objects.filter(query)

        if brand:
            clean_brand = cls.normalize_name(brand)
            if clean_brand:
                qs = qs.filter(brand__iexact=clean_brand)

        return qs.order_by("name")


def _render_catalog_response(request, section, queryset):
    """Render standard catalog response to adhere to DRY."""
    return render(
        request,
        "product_mngmnt/request.html",
        context={"prod": queryset, "section": section},
    )


def _normalize_brand_name(brand_name):
    return ProductCatalog.normalize_name(brand_name)


def _render_brand_products(request, brand_name, section_label=None):
    brand = ProductCatalog.normalize_name(brand_name)
    section = section_label or f"{brand} Parts"
    prod = ProductCatalog.get_brand_parts(brand)
    return _render_catalog_response(request, section, prod)


def _render_consumable_products(request, brand_name, section_label=None):
    brand = ProductCatalog.normalize_name(brand_name)
    section = section_label or f"{brand} Consumables"
    prod = ProductCatalog.get_brand_consumables(brand)
    return _render_catalog_response(request, section, prod)


def _render_washer_controller_products(request, brand_name, section_label=None):
    brand = ProductCatalog.normalize_name(brand_name)
    section = section_label or f"{brand} Washer Controller"
    prod = ProductCatalog.get_brand_washer_controllers(brand)
    return _render_catalog_response(request, section, prod)

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
        consumable_name = _normalize_brand_name(request.GET.get("consumable", ""))
        if consumable_name:
            return _render_consumable_products(request, consumable_name, f"{consumable_name} Consumables")
        washer_controller_name = _normalize_brand_name(
            request.GET.get("washer_controller") or request.GET.get("controller", "")
        )
        if washer_controller_name:
            return _render_washer_controller_products(
                request, washer_controller_name, f"{washer_controller_name} Washer Controller"
            )
        brand_name = _normalize_brand_name(request.GET.get("brand", ""))
        if brand_name:
            return _render_brand_products(request, brand_name, f"{brand_name} Parts")
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
        return _render_brand_products(request, "Thermopatch", "Thermopatch Parts")

def view_pony_sidi_parts(request):
    if request.method == 'GET':
        return _render_brand_products(request, "Pony/Sidi", "Pony/Sidi Parts")

def view_miscellaneous(request):
    if request.method == 'GET':
        return _render_brand_products(request, "Miscellaneous", "Miscellaneous Parts")

def view_adc_parts(request):
    if request.method == 'GET':
        return _render_brand_products(request, "ADC", "ADC Parts")
    
def view_image(request):
    if request.method == 'GET':
        section = "IMAGE"
        prod=Product.objects.filter(detail__contains="image")   
        return render(request,'product_mngmnt/request.html',context={"prod":prod ,"section":section})
    
def view_LGparts(request):
    if request.method == 'GET':
        return _render_brand_products(request, "LG", "LG Spare Parts")

# @login_required(login_url='login')    
def view_forenta_parts(request):
    if request.method == 'GET':
        return _render_brand_products(request, "Forenta", "Forenta Parts")

# @login_required(login_url='login')    
def view_hoffman_parts(request):
    if request.method == 'GET':
        return _render_brand_products(request, "Hoffman", "Hoffman Parts")

# @login_required(login_url='login')    
def view_milnor_parts(request):
    if request.method == 'GET':
        return _render_brand_products(request, "Milnor", "Milnor Parts")

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
        prod=Product.objects.filter(detail__contains="equipments : dryer")   
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
    





# Washer Controller views
def view_washer_controller(request):
    if request.method == "GET":
        brand = ProductCatalog.normalize_name(
            request.GET.get("brand") or request.GET.get("washer_controller", "")
        )
        section = f"{brand} Washer Controller" if brand else "Washer Controller"
        prod = (
            ProductCatalog.get_brand_washer_controllers(brand)
            if brand
            else ProductCatalog.get_washer_controllers()
        )
        return _render_catalog_response(request, section, prod)


# Kitchen appliances (backward compatibility)
def view_kitchen_appliances(request):
    if request.method == "GET":
        brand = request.GET.get("brand")
        prod = ProductCatalog.filter_by_keywords(
            "kitchen acc", "kitchen appliance", "kitchen accessories", brand=brand
        )
        section = f"{brand} Kitchen Accessories" if brand else "Kitchen accessories"
        return _render_catalog_response(request, section, prod)


def view_kitchen_parts(request):
    if request.method == "GET":
        brand = request.GET.get("brand")
        prod = ProductCatalog.filter_by_keywords("kitchen part", "kitchen parts", brand=brand)
        section = f"{brand} Kitchen Parts" if brand else "Kitchen Parts"
        return _render_catalog_response(request, section, prod)













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
