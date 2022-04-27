import pdb

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as log, logout
import time
from django.contrib import messages
import random
# from .models import UserOTP
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

from societyapp.form import NewsForm
from societyapp.models import News, Guest, Visitors, Complain
from .tasks import send_email_task

User = get_user_model()


def index(request):
    # return render(request, "Hello, You're at the Society Management Application.")
    return render(request, 'societyapp/index.html')


def signup(request):
    try:
        print(request.method == "POST")
        if request.method == "POST":
            name = request.POST['name']
            email = request.POST['email']
            phone = request.POST['phone']
            flat = request.POST['flat']
            tower = request.POST['tower']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if password1 != password2:
                messages.error(request, "Passwords do not match.")
                return render(request, 'societyapp/signup.html', {'error': "Password does not match"})

            user = User.objects.create_user(email=email, password=password1)
            print('user_created')
            user.name = name
            user.flat = flat
            user.tower = tower
            user.phone = phone
            user.email = email
            user_otp = random.randint(1000, 9999)
            request.session['email'] = email
            request.session['otp'] = user_otp
            user.is_active = False
            user.save()
            send_email_task.delay(email, user_otp)
            # print(email, user_otp)
            # UserOTP.objects.create(user=user,otp=user_otp)

            # mess = f"Hello {user.email}, \n Your OTP is {user_otp} \n Thank You"
            # send_mail(
            #     "Welcome",
            #     mess,
            #     settings.EMAIL_HOST_USER,
            #     [user.email],
            #     fail_silently=False
            # )
            return redirect('verify')
    except IntegrityError:
        q = email + ' already exist'
        messages.error(request, q)
    return render(request, "societyapp/signup.html")


def otp(request):
    OTP = request.session['otp']
    if request.method == "POST":

        if OTP == int(request.POST['otp']):
            user = User.objects.get(email=request.session['email'])
            user.is_verified = True
            user.is_active = True
            user.save()
            return redirect('login')
        else:
            messages.error(request, "OTP does not match. recheck or click to resend otp")
            return render(request, 'societyapp/verify.html', {'error': "OTP does not match. Please Enter Correct OTP"})
    return render(request, 'societyapp/verify.html')


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
            log(request, user)
            # messages.success(request, "Successfully Logged In")
            return redirect("/societyapp/user_dashboard")
        else:
            return render(request, 'societyapp/login.html', {'error': "Invalid Credentials"})
    return render(request, "societyapp/login.html")


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/societyapp/login')
def user_dashboard(request):
    obj = News.objects.filter().order_by('-dateTime')
    vis = Visitors.objects.filter().order_by('-dateTime')
    return render(request, "societyapp/user_dashboard.html", {'news': obj, 'visitor': vis})


def guest_dashboard(request):
    obj = News.objects.filter().order_by('-dateTime')
    return render(request, "societyapp/guest_dashboard.html", {'news': obj})


@login_required(login_url='/societyapp/login')
def add_news(request):
    form = NewsForm()
    if request.method == "POST":
        form = NewsForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            return redirect("/societyapp/user_dashboard")
    return render(request, "societyapp/add_news.html", {'form': form})


def rent(request):
    if request.method == "POST":
        rnt = Guest.objects.create()
        rnt.name = request.POST['name']
        rnt.email = request.POST['email']
        rnt.mobile = request.POST['mobile']
        rnt.flat_size = request.POST['flat_size']
        rnt.flat_type = request.POST['flat_type']
        rnt.member = request.POST['member']
        rnt.pool = request.POST.get('pool')
        rnt.gym = request.POST.get('gym')
        rnt.creche = request.POST.get('creche')
        rnt.flat_rent = True
        rnt.save()
        return redirect('message')

    return render(request, "societyapp/rent.html")


def buy(request):
    if request.method == "POST":
        rnt = Guest.objects.create()
        rnt.name = request.POST.get('name')
        rnt.email = request.POST.get('email')
        rnt.mobile = request.POST.get('mobile')
        rnt.furnished = request.POST.get('furnished')
        rnt.flat_size = request.POST.get('flat_size')
        rnt.flat_buy = True
        rnt.save()
        return redirect('message')
    return render(request, "societyapp/buy.html")


def message(request):
    return render(request, 'societyapp/message.html')


def resident(request):
    usr = User.objects.filter().order_by('name')
    return render(request, 'societyapp/resident.html', {'user': usr})


def visitors(request):
    if request.method == "POST":
        vis = Visitors.objects.create()

        vis.name = request.POST['name']
        vis.gender = request.POST['gender']
        vis.mobile = request.POST['mobile']
        vis.place = request.POST['place']
        vis.save()
        return redirect('user_dashboard')
    return render(request, "societyapp/visitors.html")


def complain_user(request):
    if request.method == "POST":
        vis = Complain.objects.create()

        vis.name = request.POST['name']
        vis.email = request.POST['email']
        vis.value = request.POST['value']
        vis.message = request.POST['message']
        vis.save()
        return redirect('user_dashboard')
    return render(request, "societyapp/user_dashboard.html")


def complain(request):
    if request.method == "POST":
        vis = Complain.objects.create()

        vis.name = request.POST['name']
        vis.email = request.POST['email']
        vis.value = request.POST['value']
        vis.message = request.POST['message']
        vis.save()
        return redirect('guest_dashboard')
    return render(request, "societyapp/guest_dashboard.html")
