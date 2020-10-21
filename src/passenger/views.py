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

from django.conf import settings 
# from django.core.mail import send_mail 

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

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

	
def checkout(request):
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
	
	
	if request.method == 'POST':
		passenger_list = request.POST.getlist('passenger')
		passenger_details = ",".join(passenger_list)
		out_ticket.passenger_details = passenger_details
		if out_ticket.journey_type == "R":
			in_ticket.passenger_details = passenger_details
			in_ticket.save()

		out_ticket.save()
		passenger = Passenger.objects.get(id=passenger_id)

		html_content = render_to_string("email_template.html",context)
		text_content = strip_tags(html_content)
		subject = 'Booking Confirmed'
		message = text_content
		email_from = settings.EMAIL_HOST_USER
		recipient_list = [passenger.email]
		email = EmailMultiAlternatives(subject, message, email_from, recipient_list)
		email.attach_alternative(html_content,"text/html")
		email.send()
				
		messages.success(request, f'Congratulations! Booking Confirmed.')
		return redirect('home')

	return render(request,'checkout.html',context)


def home(request):
	return render(request,'home.html')