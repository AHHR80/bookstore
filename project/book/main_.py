from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404

from django.views.generic.list import ListView

from _rest_.models import book_table, opinions, sold, mark_book, shop_list
from testapp.models import MyUser
from authentication.views import sendmail
from time import localtime
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate

passlist = []
passlist2 = []
check_limit = [('host', 0, 0, 0)]
blacklist = []
email_list =[]

########################################################################
def del_pass(r):
    try:
        l = localtime()
        global passlist2, passlist, email_list
        m = l.tm_min
        counter = 0
        for i in passlist2:
            if i[0] + 4 < m:
                passlist2.remove(i)
                passlist.remove((r.headers['host'], i[1]))
                counter +=1

        for ii in email_list:
            if ii[0] == r.headers['host'] and ii[2] + 4 < m:
                email_list.remove(ii)
                counter +=1
        if counter > 0:
            return redirect('user/prifile/')

    except Exception as error:
        print("\n im for del_pass function: {}\n".format(error))
########################################################################
def check(request):
    del_pass(request)
    global passlist2, passlist, check_limit, blacklist, email_list
    if request.user.is_authenticated is not True:
        return redirect('/user/log-in/')

    if len(passlist2) == 0:
        return redirect('/user/profile/')


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
                for i in email_list:
                    if request.headers['host'] == i[0]:
                        email = i[1]
                        break
                r = request.user
                query = MyUser.objects.get(email= r.email)
                query.email = email
                query.save(update_fields=['email'])

                query2 = mark_book.objects.filter(user= r.email)
                if len(query2) > 0:
                    for i in query2:
                        q = mark_book.objects.get(book_id=i.book_id, user=i.user)
                        q.user = email
                        q.save()
                query3 = sold.objects.filter(user= r.email)
                if len(query3) > 0:
                    for i in query3:
                        q = sold.objects.get(book_id = i.book_id,user= i.user)
                        q.user = email
                        q.save()
                query4 = opinions.objects.filter(user= r.email)
                if len(query4) > 0:
                    for i in query4:
                        q = opinions.objects.get(book_id=i.book_id, user=i.user)
                        q.user = email
                        q.save()

                for i in email_list:
                    if request.headers['host'] == i[0]:
                        email_list.remove(i)        

                for i in passlist2:
                    if i[1] == get_pass:
                        passlist2.remove(i)

                return redirect('/user/profile/')
    return render(request, 'check.html')
########################################################################
def search(request):
    if request.method == "POST":
        s = request.POST.get('search')
        if s is not None:
            q = book_table.objects.search(s)
            
            book_list = []
            for i in q:
                book_list.append(i)
                
            data = {
                "data": book_list,
                "list": False,
            }
            return render(request, 'card.html', data)
    return HttpResponse('bad request')
########################################################################
def opin(pk, email):
    try:
        query6 = opinions.objects.get(book_id = pk, user = email)
        return query6.opinion
    except:
        return False
########################################################################
def is_sold(pk , email):
    try:
        print(pk , email)
        q = sold.objects.get(book_id = pk, user= email)
        return True

    except Exception:
        return False
########################################################################
def shop_list_(request):
    if request.user.is_authenticated is not True:
        return redirect('/user/log-in/')

    r = request.user
    query = sold.objects.filter(user=r.email)

    price = 0
    counter = 0
    for i in query:
        price = price + int(i.price)
        counter += 1

    data = {
        "user": query,
        "price": price,
        "counter": counter,
    }

    return render(request, 'component/buy_detail.html', data)
########################################################################
def home(request):
    try:
        if request.user.is_authenticated is not True:
            return redirect('/user/log-in/')
        r = request.user
        
        print(r.profile_image)

        query = book_table.objects.top()

        list_book = []
        for i in query:
            if i != 0:
                q = book_table.objects.get(id=i)
                list_book.append(q)

        data = {
            'data': list_book,
        }

        return render(request, 'index.html', data)
    except Exception as error:
        print(error)
########################################################################
class BookInfo(ListView):
    pass
    
def book_info(request, pk, name):
    r = request.user
    message = ''

    try:
        if request.method == 'POST':
            
            if request.user.is_authenticated is not True:
                data = {
                    "message": 'برای رای دادن و ویرایش نظر باید وارد حساب خود شوید'
                }
                return render(request, 'book-info.html', data)

            opinion = opin(pk, r.email)
            buy =  is_sold(pk, r.email)

            if opinion is False and buy is True:
                counter = 0
                for i in range(1, 6):
                    if request.POST.get('star{}'.format(i)) == 'on':
                        counter =i
                #print(counter)
                opi = request.POST.get('opi')
                idea = opinions(book_id = pk, book_name= name, user = r.email, opinion = opi, star = counter)
                idea.save()

                b = book_table.objects.get(id = pk)
                b.counter_star = b.counter_star + 1
                b.counter_opi = b.counter_opi + 1
                b.average = (b.average + counter) / b.counter_star
                b.save()
                message = 'نظر شما با موفقیت ذخیره شد شما میتوانید نظر خود را ویرایش کنید'
            elif opinion is not False and buy is True:

                print(opinion, buy)

                if request.POST.get('delete') is not None:
                    message = 'نظر شما با موفقیت حذف شد است.'

                else:

                    counter = 0
                    for i in range(1, 6):
                        if request.POST.get('star{}'.format(i)) == 'on':
                            counter =i
                    #print(counter)
                    opi = request.POST.get('opi')
                    idea = opinions.objects.get(book_id = pk , user = r.email)
                    b = book_table.objects.get(id = pk)


                    if counter == 0 and opi is not None:
                        idea.opinion = opi
                        idea.save()
                        message = 'نظر شما با موفقیت ویرایش شده است'

                    elif opi is None and counter !=0 :
                        b.average = (b.average * b.counter_star ) - idea.star 
                        b.average = (b.average + counter) / b.counter_star
                        idea.star = counter
                        idea.save()
                        b.save()
                        message = 'نظر شما با موفقیت ویرایش شده است'
                    
                    elif opi is not None and counter != 0:
                        #print(idea.star, b.average, b.counter, counter,'yessssss')
                        b.average = (b.average * b.counter_star ) - idea.star 
                        b.average = (b.average + counter) / b.counter_star
                        b.save()
                        idea.opinion = opi
                        idea.star = counter
                        idea.save()
                        message = 'نظر شما با موفقیت ویرایش شده است'
                    
            ############################################################
        if request.user.is_authenticated is not True:
            authenticate=  False
            x = False
            email = None
            count = 0
            is_in_shop = 0
        else:
            authenticate = r.name
            x = is_sold(pk, r.email)
            email = r.email
            count = shop_list.objects.filter(user=r.email).count()
            is_in_shop = shop_list.objects.filter(user = r.email, book_id= pk).count()

        query = get_object_or_404(book_table, name=name, pk=pk)

        c = query.grouping
        d = query.author
        e = query.publisher

        query2 = opinions.objects.filter(book_id = pk, book_name=name)# باید تعداد ستاره ها و نظرات در اورده شود 
        query3 = book_table.objects.filter(grouping = c)
        query4 = book_table.objects.filter(author = d)
        query5 = book_table.objects.filter(publisher = e)
        query6 = mark_book.objects.filter(book_id = pk, user=email).count()
        if query6 == 0:
            query6 = False
        else:
            query6 = True
        data = {
            "data": query,
            "idea": query2,
            "similer": query3,
            "similer_author": query4,
            "similer_publisher": query5,
            "authentication": authenticate,
            "is_sold": x,
            "is_idea": opin(pk, email),
            "test": 'نظر خود را وارد کنید',
            "message": message,
            "is_pin":query6,
            "counter": count,
            "is_in_shop": is_in_shop,
        }

        #print(data)
        return render(request, "book-info.html", data)
    except Exception as error:
        print(error, 'iam for book_info function')
        return HttpResponse('bad request')
########################################################################
def list_book(request, name_group, sort):
    if sort == 'ارزان ترین':
        query = book_table.objects.low_price(name_group)
        query_list = []

        for i in query:
            query2 = book_table.objects.get(id= i)
            query_list.append(query2)

        data ={
            "data": query_list,
        }

        return render(request, 'card.html', data)
    elif sort == 'پربحث ترین':
        query = book_table.objects.more_opi(name_group)
        query_list = []

        for i in query:
            query2 = book_table.objects.get(id= i)
            query_list.append(query2)

        data ={
            "data": query_list,
        }
        return render(request, 'card.html', data)

    elif sort == 'تازه‌ها':
        query = book_table.objects.newest(name_group)
        query_list = []

        for i in query:
            query2 = book_table.objects.get(id= i)
            query_list.append(query2)

        data ={
            "data": query_list,
        }
        return render(request, 'card.html', data)
    elif sort == 'پرفروش ترین':
        query = book_table.objects.bestsellers(name_group)
        query_list = []
        
        for i in query:
            query2 = book_table.objects.get(id= i)
            query_list.append(query2)

        data ={
            "data": query_list,
        }
        return render(request, 'card.html', data)

    return render(request, 'card.html')
########################################################################
def my_book(request):
    if request.user.is_authenticated is not True:
        return redirect('/user/log-in/')
    
    r = request.user
    query = sold.objects.filter(user=r.email)

    Book_Info = []
    for i in query:
        q = book_table.objects.get(id = i.book_id)
        Book_Info.append(q)

    data ={
        "data": Book_Info,
        "data2": query,
    }

    return render(request, 'component/my-book.html', data)
########################################################################
def pin(request):
    if request.method == 'POST':
        if request.user.is_authenticated is not True:
            return redirect('/user/log-in/')

        book_id = request.POST.get('id')
        book_name = request.POST.get('name')
        user = request.POST.get('email')
        delete = request.POST.get('delete')
        print(book_id, book_name, user, delete)

        if book_id is not None and book_name is not None and user is not None and delete is None:
            if mark_book.objects.filter(user=user, book_id= book_id).count() == 0 :
                query = mark_book(book_id=book_id, book_name=book_name, user=user)
                query.save()
                return redirect('/book/{}/{}/'.format(book_id, book_name))
        elif book_id is not None and book_name is not None and delete == 'yes' and user is not None:
            query = mark_book.objects.get(book_id=book_id, book_name=book_name, user=user)
            query.delete()
            return redirect('/book/pin/')
        else:
            return HttpResponse('back request')

    if request.user.is_authenticated is not True:
        return redirect('/user/log-in/')

    r = request.user
    query = mark_book.objects.filter(user = r.email)

    Book_Info = []
    for i in query:
        q = book_table.objects.get(id = i.book_id)
        Book_Info.append(q)

    data = {
        "data": Book_Info,
    }
    return render(request, 'mark-book.html', data)
########################################################################
def profile(request):
    del_pass(request)
    if request.user.is_authenticated is not True:
        return redirect('/user/log-in/')
    message = ''
    if request.method == 'POST':
        r = request.user
        name = request.POST.get('name')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        pass_now = request.POST.get('pass-now')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        query = MyUser.objects.get(email= r.email)
        if all([name, lastname]) is not False:
            query.name = name
            query.lastname = lastname
            query.save(update_fields=['name', 'lastname'])
            message = 'نام و نام خانوادگی شما با موفقیت تغییر کرد'
        elif email is not None:
            counter = MyUser.objects.filter(email= email).count()
            print(counter)
            if counter == 0:
                global passlist, passlist2, email_list
                l = localtime()
                pa = sendmail(name='amir', mail=email)
                print(pa)
                passlist.append((request.headers['host'], pa))
                passlist2.append((l.tm_min, pa))
                email_list.append((request.headers['host'], email, l.tm_min))
                return redirect('/profile/check-email/')
            else:
                message = 'ایمیلی که وارد کرده اید قبلا انتخاب شده ایمیل دیگیری وارد کنید'
        elif phone is not None:
            query.phone = phone
            query.save()
            message = 'شماره شما تغییر کرد'
        elif pass_now is not None and pass1 is not None and pass2 is not None:
            print(pass1, pass2, pass_now)
            if pass1 == pass2:
                if authenticate(request, email=r.email, password=pass_now) is not None:
                    query.set_password(pass1)
                    query.save()
                    message = 'پسورد شما با موفقیت تغییر کرد'
                else:
                    message = 'پسورد شما نادرست است لطفا پسورد حال خود را درست وارد کنید'
            else:
                message = 'پسورد های جدید باید باهم برابر باشند'



    r = request.user
    query = MyUser.objects.get(email= r.email)
    data = {
        "data": query,
        "message": message,
    }
    return render(request, 'profile-edit.html', data)
########################################################################
def shop(request):
    if request.user.is_authenticated is not True:
        return redirect('/user/log-in/')
    r = request.user
    if request.method == "POST":
        book_id = request.POST.get('id')
        book_name = request.POST.get('name')
        user = request.POST.get('email')
        delete = request.POST.get('delete')
        if all([book_id, book_name, user]) is not False and delete is None:
            if shop_list.objects.filter(user= r.email, book_id=book_id).count() == 0:
                q = shop_list(book_id=book_id, book_name=book_name, user = user)
                q.save()
                return redirect('/book/{}/{}'.format(book_id, book_name))
        elif all([book_id, book_name, user, delete]) is not False:
            q = shop_list.objects.filter(book_id=book_id, user = user)
            q.delete()
            return redirect('/book/shop/')
        else:
            return HttpResponse('bad request')

    query = shop_list.objects.filter(user= r.email)

    query_list = []
    price = 0
    for i in query:
        q = book_table.objects.get(id = i.book_id)
        query_list.append(q)
        price = q.price + price

    data = {
        "data": query_list,
        "counter": len(query_list),
        "price":price,
    }
    return render(request, 'shop.html', data)
########################################################################
def stream(request):
    return render(request, "stream.html")

# a = BookInfo()
# print(dir(a))