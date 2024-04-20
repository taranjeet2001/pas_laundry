from django.urls import path
from product_mngmnt.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # path('',view_index ,name='index'),
    path('',view_home ,name='home'),
    path('disclaimer/',view_disclaimer ,name='disclaimer'),
    path('aboutus/',view_about , name='about'),
    path('services/',view_service , name='services'),
    path('signup/',view_signup , name='signup'),
    path('login/',view_login , name='login'),
    path('logout/',view_logout , name='logout'),
    path('forget/',view_forget , name='forget'),    
    path('sitemap.xml/',view_sitemap , name='forget'),    
    path('robots.txt/',view_robots , name='forget'),    
    # path('visitor-form/', visitor_form_view, name='visitor_form'),


    # urls for consumables dropdown 
    path('marking/' , view_marking , name='marking'),
    path('image/' , view_image , name='image'),
    path('flat_work_ironer/' , view_flatwork , name='flat_work_ironer'),
    path('pads_and_covers/' , view_padscovers , name='pads_and_covers'),

    # urls for parts dropdown 
    path('dependo_drain_valve/' , view_drainvalve , name='drainvalve'),
    path('dry_cleaning/' , view_drycleaning , name='drycleaning'),
    path('speed_queen/' , view_speedqueen , name='speedqueen'),
    path('thermopatch/' , view_thermopatch , name='thermopatch'),
    path('forenta_parts/',view_forenta_parts , name='forenta'),
    path('hoffman_parts/',view_hoffman_parts , name='hoffman'),
    path('milnor_parts/',view_milnor_parts , name='milnor'),

    # urls for equipment dropdown  
    path('washer_extractor/',view_washer_extractor , name='washerextractor'),
    path('dryer/',view_dryer , name='dryer'),
    path('roll_heated_flat_work_ironer/',view_roll_heated_flat_work_ironer , name='rollheatedironer'),
    path('chest_heated_flat_work_ironer/',view_chest_heated_flat_work_ironer , name='chestheatedironer'),
    path('dry_cleaningmachines/',view_dry_cleaning_machines , name='drycleanmachines'),
    path('marking_machine/',view_marking_machine , name='markingmachines'),
    path('finishing_machines/',view_finishing_machines , name='finishingequipment'),
    path('desc/<int:pk>' , view_desc ),


    # urls for kitchen appliances dropdown 
    path('kitchen-accessories/' , view_kitchen_appliances , name='kitchenapp'),
]
