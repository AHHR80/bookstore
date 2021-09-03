from django.contrib import admin
from .models import book_table, opinions, sold, mark_book, shop_list

class sold_edit(admin.ModelAdmin):
    list_display = ['book_name', 'user', 'data_buy']
    search_fields = ['book_id', 'book_name', 'user']
    

admin.site.register(book_table)
admin.site.register(opinions)
admin.site.register(shop_list)
admin.site.register( mark_book )
admin.site.register(sold, sold_edit)