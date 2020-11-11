from django.shortcuts import render,redirect
import datetime
from run.models import Run
from leg.models import Leg
from leg.forms import LegForm
from vessel.models import Vessel
from django.contrib import messages
from django.http import HttpResponseRedirect
from tickets.models import Ticket
from django.db.models.functions import Now

def get_leg(request):
    all_legs = Leg.objects.all()
    return render(request,"leg_dashboard.html",{'all_legs':all_legs}) 


def add_leg(request):
    vessels=Vessel.objects.all()
    if request.method == "POST":  
        form = LegForm(request.POST)  
        
        if form.is_valid():  
            form.save()  
            return redirect('leg_dashboard') 
    else:  
        form = LegForm() 
    return render(request,"add_leg.html",{'form':form, 'vessels': vessels}) 


def edit_leg(request,id):
    leg = Leg.objects.get(id=id)
    vessels=Vessel.objects.all()
    if request.method == "POST": 
        form = LegForm(request.POST, instance = leg) 
        print(form)
        if form.is_valid():  
            form.save()  
            return redirect("leg_dashboard") 
    
    else:
        print(leg.date)
        print(leg.arrival_time)
    
    return render(request,"edit_leg.html",{'leg':leg, 'vessels': vessels}) 
    print(form.errors)

def delete_leg(request, id):  
    leg = Leg.objects.get(id=id)
    leg.delete()  
    print(leg.id)
    messages.success(request, f'The leg having id {id} was deleted successfully.')
    return redirect("leg_dashboard")



