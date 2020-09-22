from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.contrib import messages
from .models import *
import bcrypt
from datetime import *
from django.db.models import Count

def index(request):
    if "user_id" in request.session:
        return redirect('/thoughts')
    return render(request,"index.html")

def register(request):
    errors = User.objects.validator(request.POST)
    if len(errors)>0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/')

    pw = request.POST['password']
    pw_hash = bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()

    new_user = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = pw_hash,
    )

    request.session['user_id'] = new_user.id

    return redirect('/thoughts')

def login(request):

    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            return redirect('/thoughts')
        
        messages.error(request, "That password does not match that email.")
        return redirect('/')

    messages.error(request, "Please check your email and password.")
    return redirect('/')

def show_thoughts_page(request):
    if "user_id" not in request.session:
        messages.error(request, "You must be logged in to view that page.")
        return redirect('/')

    current_user = User.objects.get(id = request.session['user_id'])
    context={
        "user":User.objects.get(id = request.session['user_id']),
        # "all_thoughts":Thought.objects.all().order_by('users_who_like')
        "all_thoughts":Thought.objects.annotate(num_items=Count('users_who_like')).order_by('-num_items')
        # "my_wishes" : current_user.creator.filter(date_granted= None),
        # "granted_wishes" : Wish.objects.exclude(date_granted = None)
        # # 'granted_wishes' : Wish.objects.filter(granted_status=['granted']),
        # # 'granted_wishes' : Wish.objects.filter(granted_status=User.objects.get(id = request.session['user_id'])),
        # # "allwishes": Wish.objects.all()
    }
    return render(request,'thoughts.html',context)

def logout(request):
    request.session.pop("user_id")
    return redirect('/')

def process_new_thought(request):
    errors = Thought.objects.validator(request.POST)
    if len(errors)>0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/thoughts')

    Thought.objects.create(
        thoughtName = request.POST['thoughtName'],
        creator = User.objects.get(id=request.session['user_id'])
    )
    return redirect('/thoughts')

def delete(request, thought_id):
    thought = Thought.objects.get(id=thought_id)
    thought.delete()
    return redirect ('/thoughts')

def details_page(request, thought_id):
    if "user_id" not in request.session:
        messages.error(request, "You must be logged in to view that page.")
        return redirect('/')

    current_user = User.objects.get(id = request.session['user_id'])
    main_thought = Thought.objects.get(id=thought_id)
    context={
        "user":User.objects.get(id = request.session['user_id']),
        "users_liked_this":main_thought.users_who_like.all(),
        "thought": Thought.objects.get(id=thought_id),
    }
    return render(request, "details.html", context)

def process_like(request, thought_id):
    post = request.POST
    this_thought = Thought.objects.get(id = thought_id)
    current_user = User.objects.get(id=request.session['user_id'])

    this_thought.users_who_like.add(current_user)
    # return redirect('/thoughts')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def process_unlike(request, thought_id):
    post = request.POST
    this_thought = Thought.objects.get(id = thought_id)
    current_user = User.objects.get(id=request.session['user_id'])

    this_thought.users_who_like.remove(current_user)
    # return redirect('/thoughts')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
