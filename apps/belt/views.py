from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
from time import gmtime, strftime, localtime
from django.contrib import messages
from models import * # Need this in order to run queries
from django.core.urlresolvers import reverse
import bcrypt


def index(request):
    print request.session.values()
    print '*************'
    return render(request, 'belt/index.html')

def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect(reverse('index'))
        else:
            request.session['user_id'] = User.objects.get(user_name = request.POST['u_name']).id
            messages.add_message(request, messages.INFO, 'Successfully Logged In!')
            return redirect(reverse('travels'))
    else:        
        return redirect(reverse('index'))


def register(request):
        if request.method == "POST":
            errors = User.objects.reg_validator(request.POST)
            if len(errors):
                for tag, error in errors.iteritems():
                    messages.error(request, error, extra_tags=tag)
                return redirect(reverse('index'))
            else:
                messages.add_message(request, messages.INFO, 'Successfully registered!')

                new_user = User()
                new_user.first_name = request.POST["f_name"]
                new_user.user_name = request.POST["u_name"]
                # new_user.email = request.POST["user_email"]
                new_user.password = bcrypt.hashpw(request.POST["pass"].encode(), bcrypt.gensalt())
                new_user.save()

                #since INSERT returns last row id we set this equal to session to log in
                request.session['user_id'] = User.objects.get(user_name = request.POST['u_name']).id
                print User.objects.last().id
                print User.objects.get(user_name = request.POST['u_name']).id
                return redirect(reverse('travels'))
        else:        
            return redirect(reverse('index'))

    
def travels(request):
    if 'user_id' in request.session:
        context = {
            "loggedin_user" : User.objects.get(id = request.session['user_id']),
            "user_trips" : User.objects.get(id = request.session['user_id']).tripsadded.all(),
            "other_trips" : Trip.objects.all().exclude(users_trips = request.session['user_id'])
        }
        return render(request, 'belt/dashboard.html', context)
    else:
        return redirect(reverse('index'))


def addtrip(request):
    # response = "Hello, I am your first request!"
    # return HttpResponse(response)
    
    print '!!!!!!!!!!!!!!!!!!!!!!'
    if 'user_id' in request.session:
        print "------------", request.session
        return render(request, 'belt/create.html')
    else:
        print "-----*********-------", request.session
        return redirect(reverse('index')) 

def createtrip(request):
    if request.method == "POST":
        errors = Trip.objects.trip_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect(reverse('addtrip'))
        else:
            Trip.objects.create(destination = request.POST["dest_name"], desc = request.POST["desc_name"], date_from = request.POST["travel_from"], date_to = request.POST["travel_to"], added_by = User.objects.get(id = request.session['user_id']))

            Trip.objects.last().users_trips.add(User.objects.get(id = request.session['user_id']))

            return redirect(reverse('travels'))
    else:
        return redirect(reverse('addtrip'))

def jointrip(request, id):
    # response = "Hello, I am your first request!"
    # return HttpResponse(response)

    Trip.objects.get(id = id).users_trips.add(User.objects.get(id = request.session['user_id']))
    return redirect(reverse('travels'))

def travelinfo(request, id):
    context = {
        "trip" : Trip.objects.get(id = id),
        "users" : User.objects.filter(tripsadded = id).exclude(added_trip = id)
    }
    return render(request, 'belt/trip_info.html', context)

def logout(request):
    try:
        request.session.clear()
        return redirect(reverse('index'))
    except:
        return redirect(reverse('index'))