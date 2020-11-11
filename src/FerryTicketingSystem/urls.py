"""FerryTicketingSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,include
from passenger.views import register,login,select_route,checkout,home
from passenger.views import choose_ferry_return,choose_ferry_single
# from tickets.views import checkout_view
from run.views import get_run,add_run,edit_run,delete_run
from manager.views import view_dashboard
from django.contrib.auth import views as auth_views
from leg.views import get_leg,add_leg, edit_leg, delete_leg

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home ,name='home'),
    path('login/', login ,name='login'),

    path('select_route/', select_route ,name='select_route'),
    path('register/', register,name='register'), 

    path('return/', choose_ferry_return),
    path('single/', choose_ferry_single),

    path('checkout/', checkout),

    #manager
    path('manager/',view_dashboard,name='manager_home'),
    path('runs/',get_run,name='runs'),
    path('addrun/',add_run),
    path('editrun/<int:id>',edit_run),
    # path('updaterun/<int:id>',update_run),
    path('deleterun/<int:id>',delete_run),

    #Leg
    path('leg_dashboard/',get_leg,name='leg_dashboard'),
    path('add_leg/',add_leg,name='add_leg'),
    path('edit_leg/<int:id>',edit_leg),
    path('delete_leg/<int:id>',delete_leg),

]
