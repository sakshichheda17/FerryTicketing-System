from django.shortcuts import render
from .models import Ticket
from leg.models import Leg
import datetime
from run.models import Run
from django.db.models.functions import Now
from django.contrib import messages

# Create your views here.
def update_leg_seats(ticket):
    leg = Leg.objects.get(id=ticket.leg_id)
    total_tickets_sold = ticket.no_of_adults + ticket.no_of_children
    leg.sold_seats = leg.sold_seats + total_tickets_sold
    leg.available_seats = leg.available_seats - total_tickets_sold
    leg.save()


# After Select Route 
def generate_ticket(obj,passenger_id,form,ticket_no):
	#ticket_no =1 for single way ticket
	#ticket_no=2 for return way ticket
	# print(form.cleaned_data['journey_type'])
	ticket = Ticket.objects.create(
			passenger_id = passenger_id,
			no_of_adults = form.cleaned_data['no_of_adults'],
			no_of_children = form.cleaned_data['no_of_children'],
			journey_type = form.cleaned_data['journey_type']
		)
	#For Single Way Ticket, source and destination will be same as passenger's route choice
	if ticket_no==1: 
		ticket.source = obj.source
		ticket.destination = obj.destination
	#For Return Way Ticket, source and destination will be opposite of passenger's route choice
	elif ticket_no==2:
		ticket.source = obj.destination
		ticket.destination = obj.source
	ticket.save()
	return ticket

#After choosing ferry
def update_ticket(ticket,leg_id):
    leg = Leg.objects.get(id=leg_id)
    ticket.leg_id = leg_id
    ticket.booking_time = str(datetime.datetime.now())
    ticket.vessel_name = leg.vessel_name
    ticket.arrival_time = leg.arrival_time
    ticket.departure_time = leg.departure_time
    ticket.save()
    update_leg_seats(ticket)
    return ticket

#On checkout page
def calc_journey_amount(ticket):
	leg = Leg.objects.get(id=ticket.leg_id)
	adults = ticket.no_of_adults
	children = ticket.no_of_children
	journey_type = ticket.journey_type

	if journey_type == 'S':
		journey_amount = leg.PASS*adults + leg.PCSS*children
	else:
		journey_amount = leg.PARS*adults + leg.PCRS*children
	ticket.journey_amount = journey_amount
	ticket.save()

#On checkout page
def calc_total_amount(out_ticket,in_ticket):
	total_amount = out_ticket.journey_amount + in_ticket.journey_amount
	out_ticket.total_amount = total_amount
	in_ticket.total_amount = total_amount
	out_ticket.save()
	in_ticket.save()
