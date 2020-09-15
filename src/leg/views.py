from django.shortcuts import render
import datetime
from run.models import Run
from leg.models import Leg
from django.http import HttpResponseRedirect
from tickets.models import Ticket

def update_ticket(ticket,leg_id):
    leg = Leg.objects.get(id=leg_id)
    ticket.leg_id = leg_id
    ticket.booking_time = datetime.datetime.now()
    ticket.vessel_name = leg.vessel_name
    ticket.arrival_time = leg.arrival_time,
    ticket.departure_time = leg.departure_time,
    ticket.save()
    
def get_leg(date):
    date_int = (list(map(int,date.split('-')))) #convert to list of integers [year,month,date]
    d = datetime.date(date_int[0],date_int[1],date_int[2]) #pass integers to create datetime instance
    day = d.strftime("%a") #get day of that date

    # check if date records in leg table
    existing_dates = [e['date'] for e in Leg.objects.values('date')]
    available = []
    schedule = Run.objects.all()
    if d in existing_dates:
        #check available legs based on seats 
        available_legs = Leg.objects.filter(date=d)
        print([e.run_id for e in available_legs])
        existing_legs = Leg.objects.all()
        for leg in existing_legs:
            if d == leg.date:
                available.append(leg)
        #return legs
    else:
        #get legs from run table based on day
        for i in range(len(schedule)):
            run = schedule[i]
            if getattr(run, day): #if there is run on the requested date's day, add new leg
                Leg.objects.create(
                    date=d,
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
                    max_seats = run.max_seats)
                available.append(Leg.objects.latest('id'))
    return available


def get_return_view(request):
    
    context = {}
    passenger_id = request.session['passenger_id']
    if request.method == 'POST' and request.POST['Submit']=='Find Ferry':
        formtype = request.POST['Submit']
        print(request.POST)
        context.update({'formtype': formtype})
        # date = request.POST['date'] #get date as string
        out_date = request.POST['date1']
        in_date = request.POST['date2']
        out_available = get_leg(out_date)
        in_available = get_leg(in_date)
                
        context.update({
            # 'day' : day,
            'out_available': out_available,
            'in_available': in_available
        }) 
    # ferry is selected
    if request.method == 'POST' and request.POST['Submit']=='Ok':
        print(request.POST)
        request.session['out_ferry_id'] = request.POST['out_ferry_id']
        request.session['in_ferry_id'] = request.POST['in_ferry_id']
        in_ticket = list(Ticket.objects.filter(passenger_id=passenger_id))[-1]
        update_ticket(in_ticket,request.POST['in_ferry_id'])
        out_ticket = list(Ticket.objects.filter(passenger_id=passenger_id))[-2]
        update_ticket(out_ticket,request.POST['out_ferry_id'])
        return HttpResponseRedirect('/checkout',request)

    return render(request, "return.html", context)

def get_single_view(request):
    
    context = {}
    passenger_id = request.session['passenger_id']
    if request.method == 'POST' and request.POST['Submit']=='Find Ferry':
        formtype = request.POST['Submit']
        # print(request.POST)
        context.update({'formtype': formtype})
        # date = request.POST['date'] #get date as string
        out_date = request.POST['date']
        out_available = get_leg(out_date)       
                
        context.update({
            'out_available': out_available
        }) 
    # ferry is selected
    if request.method == 'POST' and request.POST['Submit']=='Ok':
        request.session['out_ferry_id'] = request.POST['out_ferry_id']
        request.session['in_ferry_id'] = None
        leg = Leg.objects.get(id=request.POST['out_ferry_id'])
        
        # update ticket
        out_ticket = list(Ticket.objects.filter(passenger_id=passenger_id))[-1]
        update_ticket(out_ticket,request.POST['out_ferry_id'])
        
        return HttpResponseRedirect('/checkout',request)

    return render(request, "single.html", context)