from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from random import randrange
from django.conf import settings
from django.contrib.auth import get_user_model

from testapp.models import MyUser

from datetime import datetime
from time import localtime

#############################################################################################

passlist = []
passlist2 = []
check_limit = [('host', 0, 0, 0)]
blacklist = []
u_s_e_r = ['amir', 'amir', 'amir', 'amir', 'amir']

# username is phone number

def del_pass(r):
    try:
        l = localtime()
        global passlist2, passlist
        m = l.tm_min
        counter = 0
        for i in passlist2:
            if i[0] + 4 < m:
                passlist2.remove(i)
                passlist.remove((r.headers['host'], i[1]))
                counter += 1
        if counter > 0:
            counter = 0
            return redirect('/user/register/')
    except Exception as error:
        print("\n im for del_pass function: {}\n".format(error))

#############################################################################################

def sendmail(name, mail):
    try:
        ran = randrange(10000000, 10000000000)
        subject = 'ساخت حساب:'
        message = "برای تایید ایمیل کد را قرار دهید {}".format(ran)
        send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=[mail])
        return ran
    except:
        return HttpResponse('error 500, please try later')

#############################################################################################

def check(request):
    try:
        del_pass(request)
        global passlist2, passlist, check_limit, blacklist
        if request.user.is_authenticated is True:
            return redirect('/home/')

        if len(passlist2) == 0:
            return redirect('/user/register/')


        if request.method == 'POST':

            get_pass = request.POST.get('__pass__')
            get_pass = int(get_pass)

            for i in passlist:
                if get_pass != i[1]:
                    l = localtime()
                    host = request.headers['host']
                    error = {"error": "رمزی که وارد کرده اید اشتباه است دوباره وارد کنید"}
                    for ii in check_limit:
                        if host != ii[0]:
                            check_limit.append([host, 0, l.tm_min, l.tm_mday])
                        elif host == ii[0]:
                            check_limit[check_limit.index(ii)][1] = check_limit[check_limit.index(ii)][1] + 1

                            if check_limit[check_limit.index(ii)][1] >=3:
                                check_limit.remove(ii)
                                passlist.remove(i)
                                for i in passlist2:
                                    if i[1] == get_pass:
                                        passlist2.remove(i)
                                blacklist.append((host, l.tm_min))
                                return redirect('/user/register/')

                            return render(request, 'check.html', error)
                elif get_pass == i[1]:
                    global u_s_e_r
                    
                    user = MyUser.objects.create_user(email = u_s_e_r[0], name=u_s_e_r[3], lastname=u_s_e_r[4], phone=u_s_e_r[2], password=u_s_e_r[1])
                    user.save()

                    passlist.remove(i)
                    
                    for i in passlist2:
                        if i[1] == get_pass:
                            passlist2.remove(i)

                    return redirect('/home/')
        return render(request, 'check.html')
    except Exception as error:
        print(error)
        return redirect('/user/check/')

#############################################################################################

def sing_up(request):
    try:

        del_pass(request)
        l = localtime()

        global passlist, u_s_e_r, blacklist

        print(blacklist)

        for ii in blacklist:
            if request.headers['host'] in ii[0] and ii[1] + 4 >  l.tm_min:
                return HttpResponse("تلاش های شما برای ورود بیشتر از حد مجاز بوده است تا {} دقیقه دگیر نمیتوانید تلاش کنید".format(ii[1]+4- l.tm_min))
            else:
                blacklist.remove(ii)

        if request.user.is_authenticated is True:
            return redirect('/home/')
        else:
            if request.method == 'POST':
                _fullname_ = request.POST.get('_name_')
                _lastname_ = request.POST.get('_lastname_')
                _email_ = request.POST.get('_email_')
                _phone_ = request.POST.get('_phone_')
                _pass1_ = request.POST.get('_pass1_')
                _pass2_ = request.POST.get('_pass2_')

                if _phone_ == "" or _lastname_ == "" or _fullname_ == "" or _email_ == "" or _pass1_ == "" or _pass2_ == "":
                    error = {"error": "فیلد ها نباید خالی باشند"}
                    return render(request, 'register.html', error)
                else:
                    use = get_user_model()
                    username = use.objects.filter(email=_email_)
                    phone = use.objects.filter(phone=_phone_)
                    if username.exists():
                        _error = {
                            "error": " ایمیلی که انتخاب کرداید موجود است لطفا ایمیل دیگری وارد کنید یاوارد شوید",
                            "name":_fullname_,
                            "lastname":_lastname_,
                            "phone":_phone_,
                        }
                        return render(request, 'register.html', _error)
                    elif phone.exists():
                        _error_ = {
                            "error": "شماره که وارد کرده اید قبلا انتخاب شده است یا وارد شودید یا از شماره دیگری استفاده کنید ",
                            "name":_fullname_,
                            "lastname":_lastname_,
                            "email":_email_,
                        }
                        return render(request, 'register.html', _error_)
                    elif _pass1_ != _pass2_:
                        _error_ = {
                            "error": "پسوردهای شما یکسان نیست دوباره وارد کنید",
                            "name":_fullname_,
                            "lastname":_lastname_,
                            "phone":_phone_,
                            "email":_email_,
                        }
                        return render(request, 'register.html', _error_)
                    elif len(_phone_) !=11:
                        _error_ = {
                            "error": "شماره خود را درست وارد کنید",
                            "name":_fullname_,
                            "lastname":_lastname_,
                            "email":_email_,    
                        }
                        return render(request, 'register.html', _error_)
                    else:
                        
                        pa = sendmail(_fullname_, _email_)
                        
                        passlist.append((request.headers['host'], pa))
                        passlist2.append((l.tm_min, pa))
                        u_s_e_r[0] = _email_
                        u_s_e_r[1] = _pass1_
                        u_s_e_r[2] = _phone_
                        u_s_e_r[3] = _fullname_
                        u_s_e_r[4] = _lastname_
                        return redirect('/user/check/')

            return render(request, 'register.html')
    except Exception as error:
        print(error)

#############################################################################################

def log_in(request):
    try:

        del_pass(request)

        if request.user.is_authenticated is True:
            return redirect('/home/')
        if request.method == 'POST':

            u = request.POST.get('_phone_')
            p = request.POST.get('_pass1_')

            if '@' in u:
                user_check = authenticate(request, email=u, password=p)
            else:
                a = MyUser.objects.get(phone= u)
                user_check = authenticate(request, email=a.email, password=p)


            #print(user_check, type(user_check))

            if user_check is not None:

                user_check.last_login= datetime.now()
                user_check.save(update_fields=['last_login'])

                login(request, user_check)

                return redirect('/home/')

            else:
                return HttpResponse('bad request')
        else:
            return render(request, 'login.html')
    except Exception as error:
        print(error)
        return render(request, 'login.html')

#############################################################################################

def log_out(request):
    try:
        del_pass(request)

        logout(request)
        return redirect('/user/log-in/')
    except Exception as error:
        print(error)

#############################################################################################