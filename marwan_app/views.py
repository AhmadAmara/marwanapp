from django.shortcuts import render
from marwan_app.form import LoginForm, SignUpForm
from marwan_app.models import User
from django.contrib import messages
from django.shortcuts import redirect
from marwan_app.models import ActiveOrder, Order
import datetime

def home(request):
    if request.session.get('logged_in'):
        user = User.objects.get(pk=request.session['phone_number'])
        if user.have_booked:
            active_order = ActiveOrder.objects.get(user=user)
            #check if time passed
            if(active_order.order.time <  str(datetime.datetime.today())[11:16]):
                active_order.order.booked = False
                active_order.order.save()
                active_order.user.have_booked = False
                active_order.user.save()
                request.session['have_booked'] = False
                active_order.delete()
                return render(request, 'home.html')
            return render(request,'home.html', {'user':user, 'active_order':active_order})
        else:
            return render(request, 'home.html')

    return render(request, 'home.html')


def login(request):
 
    if request.method == 'POST':
        #Get the posted form
        MyLoginForm = LoginForm(request.POST)
        if MyLoginForm.is_valid():
            phone_number = MyLoginForm.cleaned_data['phone_number']
            password = MyLoginForm.cleaned_data['password']

            user_value = User.objects.filter(phone_number = phone_number).values()

            if(not user_value):
                messages.info(request, ('هذا الرقم غير مسجل'))
                return render(request, 'login.html', {"phone_number" : "bad phone number"})        
            
            elif(user_value[0]['password'] != password):
                messages.info(request, ('كلمة المرور غير صحيحة'))
                return render(request, 'login.html', {"phone_number" : "bad phone number"})        

            else:
                d = dict(user_value[0])
                request.session['logged_in'] = True
                request.session['phone_number'] = d['phone_number']
                request.session['user_type'] = d['user_type']
                request.session['name'] = d['first_name']
                request.session['have_booked'] = d['have_booked']
                print(d['have_booked'])
                if( d['have_booked']):
                    user = User.objects.get(pk=request.session['phone_number'])
                    active_order = ActiveOrder.objects.get(user=user)
                    return render(request,'home.html', {'user':user, 'active_order':active_order})
                else:

                    return render(request,'home.html', user_value[0])
            
        else:
            
            messages.info(request, ('التفاصيل غير صحيحة'))
            return render(request, 'login.html', {"phone_number" : "bad phone number"})        
       
    else:
        if request.session.get('logged_in'):
                return render(request,'home.html')

        return render(request, 'login.html')

def signout(request):
    try:
        del request.session['logged_in']
        del request.session['phone_number']
        del request.session['user_type']
        del request.session['name']
        del request.session['have_booked']
    except KeyError:
        pass
    return render(request, "home.html")

def signup(request):
    if request.method == 'POST':
        #Get the posted form
        MySignupForm = SignUpForm(request.POST)
        if MySignupForm.is_valid():
            phone_number = MySignupForm.cleaned_data['phone_number']
            first_name  = MySignupForm.cleaned_data['first_name']
            last_name  = MySignupForm.cleaned_data['last_name']
            password = MySignupForm.cleaned_data['password']
            
            user_value = User.objects.filter(pk = phone_number)

            if(user_value):
                messages.error(request, ('המספר הזה כבר רשום'))
                return redirect('.')

            new_user = User()
            new_user.phone_number = phone_number
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.password = password
            new_user.save()
           
            return render(request, "login.html")
        else:
            messages.error(request, ('أحد التفاصيل التي ادخلتها غير صحيحة'))
            return render(request, "signup.html",{'message': 'somthing wrong, please fill the form again'})        
    else:

        return render(request, "signup.html",{})


def order(request):
    if Order.objects.count() == 0:
        init_orders_db()
    if request.session.get('logged_in'):
        updateOrders() 
        day_1 = Order.objects.filter(day_index = 0)
        day_2 = Order.objects.filter(day_index = 1)
        print(str(datetime.datetime.today())[11:16])
        print("10:00" > str(datetime.datetime.today())[11:16])
        return render(request, "bookTimes.html", {'day1': day_1,'day2': day_2, 'now_hour': str(datetime.datetime.today())[11:16]})
    else:
        return render(request, "login.html")

def bookTimes(request):
    if request.method == 'POST':
        pass
    else:
        day_1 = Order.objects.filter(day_index = 0)
        day_2 = Order.objects.filter(day_index = 1)
        return render(request, "bookTimes.html", {'day1': day_1,'day2': day_2}) 

def init_orders_db():
    times = ["10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00",
     "13:30","14:00", "14:30","15:00", "15:30","16:00", "16:30","17:00", "17:30"
     ,"18:00", "18:30","19:00", "19:30","20:00", "20:30", "22:30"]

    for i in range(0,2):
        for time in times:
            order = Order()
            order.day_index = i
            order.time = time
            order.dt = datetime.datetime.today() + datetime.timedelta(days=i)
            order.save()

def updateOrders():
    day_1 = Order.objects.filter(day_index = 0)
    # print(day_1[0].dt)
    if datetime.datetime.today().date() > day_1[0].dt:
        print("faaaaaaaaaaaaaat")
        day_1.update(day_index=3)
        day_1 = Order.objects.filter(day_index = 3)
        day_1.update(dt = datetime.datetime.today() + datetime.timedelta(days=1))
        day_1.update(booked=False)
        day_2 = Order.objects.filter(day_index = 1)
        day_2.update(day_index=0)
        day_1 = Order.objects.filter(day_index = 3)
        day_1.update(day_index=1)

def book(request, time_id):
    if request.session.get('logged_in'):
        updateOrders()
        user = User.objects.get(pk=request.session['phone_number'])
        if  user.have_booked:
            messages.error(request, ('لديك دور محجوز'))
            active_order = ActiveOrder.objects.get(user=user)
            return render(request,'home.html', {'user':user, 'active_order':active_order})

        order = Order.objects.get(pk=time_id)

        if order.booked:
            messages.success(request, ("هذا الدور لم يعد متوفرا"))
            return render(request, 'bookTimes.html')

        order.booked = True
        order.save()
        user.have_booked = True
        user.save()
        active_order = ActiveOrder()
        active_order.user = user
        active_order.order = order
        active_order.save()
        request.session['have_booked'] = True
        messages.success(request, ("تم حجز الدور بنجاح"))
        return render(request,'home.html', {'active_order':active_order})
    else:
        return render(request, 'login.html')

def cancel_booked(request, booked_id):
    if request.session.get('logged_in'):
        ao = ActiveOrder.objects.get(pk=booked_id)
        ao.user.have_booked = False
        ao.user.save()
        ao.order.booked = False
        ao.order.save()
        request.session['have_booked'] = False
        ao.delete()
        messages.error(request, ('لقد تم الغاء الدور'))
        return render(request, 'home.html')
    else:
        return render(request, 'loggedin.html')

######################################## admin #################################

def control_panel(request):
    if request.session.get('user_type') == 'admin':
        return render(request, 'adminTemplates/controlPanel.html')
    else:
        return redirect('login')

def today_orders(request):
    today_orders = ActiveOrder.objects.filter(order__day_index=0)
    return render(request, 'adminTemplates/todayOrders.html', {'today_active_orders': today_orders})

def tomorrow_orders(request):
    tomorrow_orders = ActiveOrder.objects.filter(order__day_index=1)
    return render(request, 'adminTemplates/tomorrowOrders.html', {'tomorrow_active_orders': tomorrow_orders})
