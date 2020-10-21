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

def get_leg(date,ticket):
    date_int = (list(map(int,date.split('-')))) #convert to list of integers [year,month,date]
    d = datetime.date(date_int[0],date_int[1],date_int[2]) #pass integers to create datetime instance
    day = d.strftime("%a") #get day of that date

    # check if date records in leg table
    existing_dates = [e['date'] for e in Leg.objects.values('date')]
    available = []
    schedule = Run.objects.all()
    if d in existing_dates:
        #check available legs based on seats 
        available_legs = list(Leg.objects.filter(date=d))
        print(available_legs)
        # print([e.run_id for e in available_legs])
        # existing_legs = Leg.objects.all()
        for leg in available_legs:
            if d == leg.date and leg.source == ticket.source and leg.destination == ticket.destination and leg.available_seats >= (ticket.no_of_adults+ticket.no_of_children):
                available.append(leg)
        #return legs
    # if len(available):
        #get legs from run table based on day and passenger's route choice!
    if len(available) == 0:
        for i in range(len(schedule)):
            run = schedule[i]
            if getattr(run, day) == True : #if there is run on the requested date's day, add new leg
                if run.source == ticket.source and run.destination == ticket.destination:
                    Leg.objects.create(
                        date=d,
                        day=day,
                        run_id=run.id,
                        source = run.source,
                        destination = run.destination,
                        vessel_name = run.vessel_name,
                        arrival_time = run.arrival_time,
                        departure_time = run.departure_time,
                        PASS = run.PASS,
                        PARS = run.PARS,
                        PCSS = run.PCSS,
                        PCRS = run.PCRS,
                        max_seats = run.max_seats,
                        sold_seats=0,
                        available_seats=run.max_seats)
                    available.append(Leg.objects.latest('id'))
    print(available)
    return available


def view_leg(request):
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


def update_leg_seats(ticket):
    leg = Leg.objects.get(id=ticket.leg_id)
    total_tickets_sold = ticket.no_of_adults + ticket.no_of_children
    leg.sold_seats = leg.sold_seats + total_tickets_sold
    leg.available_seats = leg.available_seats - total_tickets_sold
    leg.save()
