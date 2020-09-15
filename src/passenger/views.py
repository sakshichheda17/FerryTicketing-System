from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from .forms import PassengerCreationForm, PassengerLoginForm
from django.contrib import messages
from .models import Passenger
from tickets.forms import TicketForm
from route.models import Route
from tickets.models import Ticket
from django.http import HttpResponseRedirect

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


def generate_ticket(obj,passenger_id,form):
	print(form.cleaned_data['journey_type'])
	ticket = Ticket.objects.create(
			passenger_id = passenger_id,
			source = obj.source,
			destination = obj.destination,
			no_of_adults = form.cleaned_data['no_of_adults'],
			no_of_children = form.cleaned_data['no_of_children'],
			journey_type = form.cleaned_data['journey_type']
		)
	ticket.save()
	return ticket

def select_route(request):	
	passenger_id = request.session['passenger_id']

	form = TicketForm(request.POST or None)
	routes = Route.objects.all()
	
	context = {}
	context.update({'routes': routes, 'passenger_id': passenger_id})
	
	if form.is_valid():
		id = request.POST['route']
		journey_type= request.POST['journey_type']
		obj = Route.objects.get(id=id)
		out_ticket = generate_ticket(obj,passenger_id,form)
		if journey_type == 'R':
			in_ticket = generate_ticket(obj,passenger_id,form)
		form = TicketForm()
		context['ticket'] = out_ticket
		if Ticket.objects.latest('id').journey_type == 'R':
			return HttpResponseRedirect('/return',request)
		else:
			return HttpResponseRedirect('/single',request)

	context.update({'form': form})
	print(context)
	return render(request,'select_route.html',context)
	