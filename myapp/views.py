from django.shortcuts import render
from .models import UserComments,Booking,Menu
from .forms import CommentForm,BookingForm
from django.http import JsonResponse
from django.core import serializers
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

import json
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'book.html', context)

# Add your code here to create new views

def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data})

def display_menu_item(request, pk=None): 
    if pk: 
        menu_item = Menu.objects.get(pk=pk) 
    else: 
        menu_item = "" 
    return render(request, 'menu_item.html', {"menu_item": menu_item}) 


def reservations(request):
    date=request.GET.get("date",datetime.today().date())
    bookings=Booking.objects.all()
    booking_json=serializers.serialize('json',bookings)
    return render(request,'bookings.html',{'bookings':booking_json})

@csrf_exempt
def bookings(request):
    
    if request.method =="POST":
        data=json.load(request)
        exist=Booking.objects.filter(reservation_date=data['resercation_date']).filter(
            reservation_slot=data["reservation_slot"]).exists()
        
        if exist ==False:
            booking=Booking(
                first_name=data["first_name"],
                reservation_date=data["reservation_date"],
                reservation_slot=data["reservation_slot"],
            )
            booking.save()
        
        else:
            return  HttpResponse("{'error:1'}",content_type="application/json")
    
    date=request.GET.get('date',datetime.today().date())   
    bookings=Booking.objects.all().filter(reservation_date=date)
    booking_json=serializers.serialize('json',bookings) 
    
    return HttpResponse(booking_json,content_type='application/json')

def form_view(request):
    form = CommentForm()
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            # clean_data is a method that helps in data normalization
            cd = form.cleaned_data
            
            uc = UserComments(
                first_name=cd["first_name"],
                last_name=cd["last_name"],
                comment=cd["comment"],
            )
            
            uc.save()
            return JsonResponse({
                'message':'success'
                    })
            
    return render(request,'blog.html',{'form':form})        

      
      
        