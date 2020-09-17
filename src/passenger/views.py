from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from .forms import PassengerCreationForm, PassengerLoginForm
from django.contrib import messages
from .models import Passenger
from tickets.forms import TicketForm
from route.models import Route
from tickets.models import Ticket
from django.http import HttpResponseRedirect
from leg.models import Leg
from tickets.views import generate_ticket,calc_journey_amount,calc_total_amount,update_ticket
from leg.views import get_leg

def login(request):
	if request.method == "POST":
		form = PassengerLoginForm(request.POST)        
		if form.is_valid():        	
			username = form.cleaned_data.get('username')        	
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)            
			if user is not None:            	
				return redirect('/admin/')           
			else:            	
				if Passenger.objects.filter(username=username,password=password).exists():            		
					messages.success(request, f'The passenger {username} was logged in successfully.')
					passenger_id = Passenger.objects.get(username=username).id
					request.session['passenger_id']=passenger_id
					return redirect('select_route')
					# return render(request,'select_route.html', {})

				else:
					messages.warning(request,'Please enter a valid username and password.')

	else:
		form = PassengerLoginForm()


	return render(request,'login.html',{'form': form })


def register(request):
	if request.method == "POST":
		form = PassengerCreationForm(request.POST)

		if form.is_valid():
			username = form.cleaned_data.get('username')
			if Passenger.objects.filter(username=form.cleaned_data['username']).exists():
				# print('Already exists')
				messages.warning(request, f'The username {username} already exists.')

			else:
				form.save()			
				print(form.cleaned_data)
				messages.success(request, f'The passenger {username} was registered successfully.')
				return redirect('login')			    
			
	else:
	    form = PassengerCreationForm()		

	return render(request,'register.html',{'form': form })


# def generate_ticket(obj,passenger_id,form,ticket_no):
# 	#ticket_no =1 for single way ticket
# 	#ticket_no=2 for return way ticket
# 	# print(form.cleaned_data['journey_type'])
# 	ticket = Ticket.objects.create(
# 			passenger_id = passenger_id,
# 			no_of_adults = form.cleaned_data['no_of_adults'],
# 			no_of_children = form.cleaned_data['no_of_children'],
# 			journey_type = form.cleaned_data['journey_type']
# 		)
# 	#For Single Way Ticket, source and destination will be same as passenger's route choice
# 	if ticket_no==1: 
# 		ticket.source = obj.source
# 		ticket.destination = obj.destination
# 	#For Return Way Ticket, source and destination will be opposite of passenger's route choice
# 	elif ticket_no==2:
# 		ticket.source = obj.destination
# 		ticket.destination = obj.source
# 	ticket.save()
# 	return ticket

def select_route(request):	
	passenger_id = request.session['passenger_id']

	form = TicketForm(request.POST or None)
	routes = Route.objects.all()
	
	context = {}
	context.update({'routes': routes, 'passenger_id': passenger_id})
	
	if form.is_valid():
		id = request.POST['route']
		journey_type= request.POST['journey_type']
		request.session['passenger_id']=passenger_id
		obj = Route.objects.get(id=id)
		out_ticket = generate_ticket(obj,passenger_id,form,1)
		if journey_type == 'R':
			in_ticket = generate_ticket(obj,passenger_id,form,2)
		form = TicketForm()
		context['ticket'] = out_ticket #why did i do this?
		if Ticket.objects.latest('id').journey_type == 'R':
			return HttpResponseRedirect('/return',request)
		else:
			return HttpResponseRedirect('/single',request)

	context.update({'form': form})
	print(context)
	return render(request,'select_route.html',context)


def choose_ferry_return(request):
    
    context = {}
    passenger_id = request.session['passenger_id']
    if request.method == 'POST' and request.POST['Submit']=='Find Ferry':
        formtype = request.POST['Submit']
        print(request.POST)
        context.update({'formtype': formtype})
        in_ticket = list(Ticket.objects.filter(passenger_id=passenger_id))[-1]
        out_ticket = list(Ticket.objects.filter(passenger_id=passenger_id))[-2]
        in_source = in_ticket.source
        in_destination = in_ticket.destination
        out_source = out_ticket.source
        out_destination = out_ticket.destination
        # date = request.POST['date'] #get date as string
        out_date = request.POST['date1']
        in_date = request.POST['date2']
        out_available = get_leg(out_date,out_ticket)
        in_available = get_leg(in_date,in_ticket)
        print(out_available, in_available)
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
        out_ticket = list(Ticket.objects.filter(passenger_id=passenger_id))[-2]
        out_ticket = update_ticket(out_ticket,request.POST['out_ferry_id'])
        request.session['booking_time'] = out_ticket.booking_time
        in_ticket = update_ticket(in_ticket,request.POST['in_ferry_id'])
        print(in_ticket.booking_time)
        request.session['in_booking_time'] = in_ticket.booking_time
        return HttpResponseRedirect('/checkout',request)

    return render(request, "return.html", context)

def choose_ferry_single(request):
    
    context = {}
    passenger_id = request.session['passenger_id']
    if request.method == 'POST' and request.POST['Submit']=='Find Ferry':
        formtype = request.POST['Submit']
        # print(request.POST)
        context.update({'formtype': formtype})
        # date = request.POST['date'] #get date as string
        out_ticket = list(Ticket.objects.filter(passenger_id=passenger_id))[-1]
        out_source = out_ticket.source
        out_destination = out_ticket.destination
        out_date = request.POST['date']
        out_available = get_leg(out_date,out_ticket)       
        print(out_available)
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
        print(out_ticket)
        out_ticket = update_ticket(out_ticket,request.POST['out_ferry_id'])
        print('hello')
        request.session['out_booking_time'] = out_ticket.booking_time
        request.session['in_booking_time'] = None
        return HttpResponseRedirect('/checkout',request)

    return render(request, "single.html", context)

# def calc_journey_amount(ticket):
# 	leg = Leg.objects.get(id=ticket.leg_id)
# 	adults = ticket.no_of_adults
# 	children = ticket.no_of_children
# 	journey_type = ticket.journey_type

# 	if journey_type == 'S':
# 		journey_amount = leg.PASS*adults + leg.PCSS*children
# 	else:
# 		journey_amount = leg.PARS*adults + leg.PCRS*children
# 	ticket.journey_amount = journey_amount
# 	ticket.save()

# def calc_total_amount(out_ticket,in_ticket):
# 	total_amount = out_ticket.journey_amount + in_ticket.journey_amount
# 	out_ticket.total_amount = total_amount
# 	in_ticket.total_amount = total_amount
# 	out_ticket.save()
# 	in_ticket.save()

	
def checkout_view(request):
	passenger_id = request.session['passenger_id']
	out_booking_time = request.session['out_booking_time']
	
	context = {'passenger_id': request.session['passenger_id'],
		'out_booking_time': out_booking_time
	}
	
	last_ticket = list(Ticket.objects.filter(passenger_id=passenger_id))[-1]
	if last_ticket.journey_type == 'R':
		out_ticket = list(Ticket.objects.filter(passenger_id=passenger_id))[-2]
		calc_journey_amount(out_ticket)
		out_leg= Leg.objects.get(id=out_ticket.leg_id)
		context.update({'out_ticket': out_ticket,'out_leg':out_leg})
		in_booking_time = request.session['in_booking_time']
		in_ticket = list(Ticket.objects.filter(passenger_id=passenger_id))[-1]
		in_leg= Leg.objects.get(id=in_ticket.leg_id)
		context.update({'in_ticket': in_ticket, 'in_leg': in_leg})
		context.update({'in_booking_time': in_booking_time})
		calc_journey_amount(in_ticket)
		calc_total_amount(out_ticket,in_ticket)
		
	else:
		out_ticket = list(Ticket.objects.filter(passenger_id=passenger_id))[-1]
		calc_journey_amount(out_ticket)
		out_leg= Leg.objects.get(id=out_ticket.leg_id)
		context.update({'out_ticket': out_ticket,'out_leg':out_leg})
		out_ticket.total_amount = out_ticket.journey_amount
		out_ticket.save()
	
	
	
	return render(request,'checkout.html',context)