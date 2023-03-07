from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
# data = [
#     {'id':1, 'name': 'Page1'},
#     {'id':2, 'name': 'Page2'},
#     {'id':3, 'name': 'Page3'},
# ]

def loginPage(request):
    
    if request.user.is_authenticated: 
        return redirect('home')
        
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try: user = User.objects.get(username=username)
            
        except: 
            messages.error(request, 'User does not exist!')
            return redirect('home')

        user = authenticate(request, username=username, password=password)
        if user is not None: 
            login(request, user)
            return redirect('home')
        else : messages.error(request, 'Username or password does not exist!')
    context = {'message': 'login'}
    return render(request, 'base/login_register.html', context)



def logoutPage(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) #customizing user submission before saving
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else : 
            messages.error(request, 'An error occured during registration!')
    context = {'form':form}
    return render(request, 'base/signup.html', context)

def profilePage(request, pk):
    user = User.objects.get(id=pk)
    room = user.room_set.all()
    messages_recent = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user, 'topics':topics, 'room':room, 'messages_recent':messages_recent}
    return render(request, 'base/profile.html', context)

def home(request):
    # return HttpResponse("HomePage")

    q = request.GET.get('q')
    if request.GET.get('q') != None: q = request.GET.get('q')
    else: q = ''
    # room = Room.objects.filter(topic__name__icontains=q)
    room = Room.objects.filter(
            Q(topic__name__icontains=q)
            # Q(name__icontains=q)|
            # Q(description__icontains=q)
        )
    # room = Room.objects.all()
    topic = Topic.objects.all()
    topic_count = topic.count
    topic = topic[0:5]
    room_count = room.count()
    # message_recent = Message.objects.all() # all messages
    message_recent = Message.objects.filter(Q(room__topic__name__icontains=q)) # of_particular Room
    context = {'room' : room, 'topics':topic, 'room_count':room_count, 'messages_recent':message_recent, 'topic_count':topic_count}
    return render(request, 'base/home.html', context)
    # return render(request, 'home.html', {'room' : room})

def room(request, pk):
    # return HttpResponse("You are in Room")
    room = {}
    room = Room.objects.get(id=pk)
    
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room = room,
            body=request.POST.get('body') #name of input
        )
        room.participant.add(request.user) #to add user into room
        return redirect('room', pk=room.id)
    
    #cant name messages cuz we have flash messages of django of same name
    # messages = room.message_set.all() # GET all messages from room
    room_messages = room.message_set.all().order_by('-created') # GET all messages from room
    participants = room.participant.all()
    # for i in data:
    #     if i['id'] == int(pk): 
    #         room = i 
    context = {'room':room, 'room_messages':room_messages, 'participants':participants}
    return render(request, 'base/room.html', context)


@login_required(login_url='/login')
def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        # print(request.post)
        form = RoomForm(request.POST)
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            topic=topic,
            host=request.user
        )

        # if form.is_valid():
        #     form = form.save(commit=False)  
        #     form.host = request.user
        #     form.save()
        return redirect('home')
    topics = Topic.objects.all()
    context = {'form' : form, 'topics':topics}
    return render(request, 'base/room_form.html', context)
 
@login_required(login_url='/login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    # get initial form(specifications) of this Room
    form = RoomForm(instance=room)
    # creating new form and filling entering of old one, to update on that

    if request.user != room.host:
        # messages(request, 'Forbidden')
        return HttpResponse("You are not allowed")

    if request.method == "POST":
        # print(request.post)
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        room.name = request.POST.get('name') 
        room.description = request.POST.get('description') 
        room.topic = topic
        room.save()
        return redirect('home')
        # form = RoomForm(request.POST, instance=room) #Update "room" instance
        # if form.is_valid():
        #     form.save()
        #     return redirect('home')
    
    topics = Topic.objects.all()
    context = {'form':form, 'topics':topics, 'room':room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        # messages(request, 'Forbidden')
        return HttpResponse("You are not allowed")
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})

@login_required(login_url='/login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    # if request.user != message.user:
    #     # messages(request, 'Forbidden')
    #     return HttpResponse("You are not allowed")
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})


@login_required(login_url='/login')
def settingsPage(request, pk):
    user = User.objects.get(id=pk)

    if request.method == "POST":
        user.username = request.POST.get('username')
        user.save()
        return redirect('home')
        # user.name = request.POST.get('name')
        # user.name = request.POST.get('name')
        # user.name = request.POST.get('name')
    
    context = {'user':user}
    return render(request,'base/settings.html', context)
    
@login_required(login_url='/login')
def updatePage(request, pk):
    user = User.objects.get(id=pk)
    user = request.user
    form = UserForm(instance=user)
    
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', user.id)
            
    context = {'user':user, 'form':form}
    return render(request,'base/update-user.html', context)
    
def topicsPage(request):
    if request.GET.get('q') != None: q = request.GET.get('q')
    else: q = ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {'topics': topics}
    return render(request, 'base/topics.html', context) 

def activityPage(request):
    messages_recent = Message.objects.all()
    context = {"messages_recent":messages_recent}
    return render(request, 'base/activity.html', context) 