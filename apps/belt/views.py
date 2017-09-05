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
            request.session['user_id'] = User.objects.get(email = request.POST['user_email']).id
            messages.add_message(request, messages.INFO, 'Successfully Logged In!')
            return redirect(reverse('quotes'))
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
                new_user.alias = request.POST["u_name"]
                new_user.email = request.POST["user_email"]
                new_user.password = bcrypt.hashpw(request.POST["pass"].encode(), bcrypt.gensalt())
                new_user.save()

                #since INSERT returns last row id we set this equal to session to log in
                request.session['user_id'] = User.objects.get(email = request.POST['user_email']).id
                # print User.objects.last().id
                # print User.objects.get(user_name = request.POST['u_name']).id
                return redirect(reverse('quotes'))
        else:        
            return redirect(reverse('index'))

    
def quotes(request):
    if 'user_id' in request.session:
        context = {
            "loggedin_user" : User.objects.get(id = request.session['user_id']),
            "quotes" : Quote.objects.all().exclude(fav_quotes = request.session['user_id']),
            "favs" : User.objects.get(id = request.session['user_id']).quotesadded.all(),
        }
        return render(request, 'belt/dashboard.html', context)
    else:
        return redirect(reverse('index'))

def addquote(request):
    # response = "Hello, I am your first request!"
    # return HttpResponse(response)

    if request.method == "POST":
        errors = Quote.objects.quote_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect(reverse('quotes'))
        else:

            Quote.objects.create(quoted_by = request.POST["quoted_by"], message = request.POST["message"], added_by = User.objects.get(id = request.session['user_id']))

            Quote.objects.last().fav_quotes.add(User.objects.get(id = request.session['user_id']))

            return redirect(reverse('quotes'))
    # else:
    #     return redirect(reverse('addtrip'))

def addtolist(request, id):
    # response = "Hello, I am your first request!"
    # return HttpResponse(response)

    Quote.objects.get(id = id).fav_quotes.add(User.objects.get(id = request.session['user_id']))
    return redirect(reverse('quotes'))

def removefromlist(request, id):
    Quote.objects.get(id = id).fav_quotes.remove(User.objects.get(id = request.session['user_id']))
    return redirect(reverse('quotes'))

def userinfo(request, id):
    if 'user_id' in request.session:
        context = {
            "user" : User.objects.get(id = id),
            "quotes" : Quote.objects.filter(added_by__id = id),
            "count" : Quote.objects.filter(added_by__id = id).count()
        }
        return render(request, 'belt/user_info.html', context)
    else:
        return redirect(reverse('index')) 

def logout(request):
    try:
        request.session.clear()
        return redirect(reverse('index'))
    except:
        return redirect(reverse('index'))