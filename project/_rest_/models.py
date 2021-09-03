from typing import Counter
from django.db import models

from datetime import datetime

from django.db.models import query

##############################################################

class shop_list(models.Model):
    book_id = models.IntegerField(default=0)
    book_name = models.CharField(max_length=150)
    user = models.CharField(max_length=150, default='amir')
    
##############################################################

class mark_book(models.Model):
    book_id = models.IntegerField(default=0)
    book_name = models.CharField(max_length=150)
    user = models.CharField(max_length=150, default='amir')
    
##############################################################

class sold (models.Model):
    book_id = models.IntegerField(default=0)
    book_name = models.CharField(max_length=150)
    user = models.CharField(max_length=150, default='amir')
    price = models.CharField(max_length=15, default="0")
    data_buy = models.DateTimeField(default=datetime.now())


    def __str__(self):
        return "{}{}".format(self.book_name, self.user)
    
##############################################################

class opinions (models.Model):
    book_id = models.IntegerField(default=0)
    book_name = models.CharField(max_length=150)
    user = models.CharField(max_length=150, default='amir13roshan80@gmail.com')
    opinion= models.TextField(max_length=50000)
    star= models.IntegerField(default=0)# کاربر به ان چند ستاره داده است

    def __str__(self):
        return "{}{}".format(self.book_name, self.user)
    
##############################################################

class book_table_manager(models.Manager):

    last_top_book = [(0,-1, -1)]

    def top(self):
        global last_top_book
        books = self.get_queryset().all()
        list_book = []
        for i in books:
            b = (i.id, i.num_sold, i.average)
            list_book.append(b)
        
        test = []
        for i in range(0, 4):
            for ii in list_book:
                if ii[0] in test:
                    continue
                if ii[1] >= self.last_top_book[0][1]:
                        del self.last_top_book[0]
                        self.last_top_book.append(ii)
            test.append(self.last_top_book[0][0])
            self.last_top_book[0] = (0, -1, -1)
        return test
        ##############################################################
    def search(self, work):
        namee = self.get_queryset().filter(name__contains=work)
        authorr = self.get_queryset().filter(author__contains=work)
        Publisherr = self.get_queryset().filter(publisher__contains=work)
        tranlator = self.get_queryset().filter(tranlator=work)

        e = book_table.objects.none()
        f = e.union(namee, authorr, Publisherr, tranlator)
        return f
        ##############################################################
    def low_price(self, name_group):
        q = self.get_queryset().filter(grouping=name_group)
        if q.count() == 0:
            return None
        
        dic = []
        for i in q:
            dic.append({i.id: i.price})
        
        book_id = []
        price = []
        for i in dic:
            for ii, iii in i.items():
                book_id.append(ii)
                price.append(iii)
        
        price.sort()

        result = []

        for i in price:
            for ii in book_id:
                if {ii: i} in dic and {ii: i} not in result :
                    result.append(ii)

        return result
        ##############################################################
    def more_opi(self, name_group):
        q = self.get_queryset().filter(grouping=name_group)
        
        book_id = []
        for i in q:
            if q.count() > 0:
                book_id.append({i.id: i.counter_opi})
            else:
                return None
        
        book_id_opi = []
        count = []
        for i in book_id:
            for ii, iii in i.items():
                book_id_opi.append(ii)
                count.append(iii)

        count.sort()

        result =[]
        for i in count:
            for ii in book_id_opi:
                if {ii: i} in book_id and ii not in result :
                    result.append(ii)

        result.reverse()

        return result
        ##############################################################
    def newest(self, name_group):
        q = self.get_queryset().filter(grouping=name_group)

        book_id = []
        for i in q:
            if q.count() > 0:
                book_id.append(i.id)
            else:
                return None

        book_id.reverse()
        return book_id
        ##############################################################
    def bestsellers(self, name_group):
        q = self.get_queryset().filter(grouping=name_group)
        
        book_id = []
        for i in q:
            if q.count() > 0:
                book_id.append({i.id: i.num_sold})
            else:
                return None
        
        book_id_opi = []
        count = []
        for i in book_id:
            for ii, iii in i.items():
                book_id_opi.append(ii)
                count.append(iii)

        count.sort()

        result =[]
        for i in count:
            for ii in book_id_opi:
                if {ii: i} in book_id and ii not in result :
                    result.append(ii)
                    
        result.reverse()

        return result
    
##############################################################

class book_table(models.Model):

    CHOICES = (
	    ('ادبیات',
            (
                ('ادبیات پارسی','ادبیات پارسی'),('ادبیات جهان','ادبیات جهان'),('نگارش','نگارش'),('شعر پارسی','شعر پارسی'),('شعر خارجی','شعر خارجی'),('طنز','طنز'),('فرهنگ لغت','فرهنگ لغت'),('زندگی نامه','زندگی نامه'),('سفرنامه','سفرنامه'),('نقد و برسی','نقد و برسی'),
            )
        ),
        ('داستان و رمان',
            (
                ('رمان های خارجی','رمان های خارجی'),('رمان های ایرانی', 'رمان های ایرانی')
            )
        ),
        ('روان شناسی',
            (
                ('موفقیت','موفقیت'),('خانواده و روابط','خانواده و روابط'),('خودسازی','خودسازی'),('ارتباطات','ارتباطات'),('بزرگسال','بزرگسال'),('کودک و نوجوان','کودک و نوجوان'),
            )
        ),
        (
            'اقتصاد و مدیریت',(
                ('بازاریابی و فروش','بازاریابی و فروش'),('مدیریت و رهبری','مدیریت و رهبری'),('کارآفرینی','کارآفرینی'),('حسابداری','حسابداری'),('سرمایه گذاری و بورس','سرمایه گذاری و بورس'),('مدیریت پروژه','مدیریت پروژه'),('امور مالی و بیمه','امور مالی و بیمه'),('مدیریت سازمان','مدیریت سازمان'),('اقتصاد','اقتصاد'),('گزارش‌های آماری','گزارش‌های آماری'),
            )
        ),
        (
            'کامپیوتر',(
                ('آموزش کامپیوتر و اینترنت','آموزش کامپیوتر و اینترنت'),('سیستم عامل','سیستم عامل'),('برنامه نویسی','برنامه نویسی'),('تجارت الکترونیک','تجارت الکترونیک'),('هک و امنیت','هک و امنیت'),('آموزش شبکه','آموزش شبکه'),('سخت افزار','سخت افزار'),('طراحی وب سایت','طراحی وب سایت'),('گرافیک کامپیوتری و انیمیشن','گرافیک کامپیوتری و انیمیشن')
            )
        )
    )
    name= models.CharField(max_length=150, default='amir')
    author= models.CharField(max_length=150, default='amir')
    tranlator= models.CharField(max_length=150, default='amir')
    year= models.CharField(max_length=150, default='amir')
    format_book= models.CharField(max_length=150, default='amir')
    number_of_pages= models.CharField(max_length=150, default='amir')
    language= models.CharField(max_length=150, default='amir')
    ISBN= models.CharField(max_length=150, default='amir')
    contents= models.TextField()# فهرست
    publisher= models.CharField(max_length=150, default='amir')
    description= models.TextField()
    average = models.FloatField(null=True, blank=True, default=0)
    counter_star = models.IntegerField(null=True, blank=True, default=0)
    counter_opi = models.IntegerField(null=True, blank=True, default=0)
    num_sold = models.IntegerField(null=True, blank=True, default=0) # فروخته شده 
    price = models.IntegerField(default=10000)
    image = models.ImageField()
    grouping = models.CharField(max_length=5555550, choices= CHOICES, default='برنامه نویسی')
    file_detail = models.FileField(default='1.jpg')
    file_full = models.FileField(default='1.jpg')
    date_add = models.DateTimeField(default=datetime.now())

    objects = book_table_manager()

    def __str__(self):
        return self.name
