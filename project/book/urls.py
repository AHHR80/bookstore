from django.contrib import admin
from django.contrib.auth import authenticate
from django.urls import path, include
from .main_ import home, book_info, shop_list_, list_book, my_book, pin, profile, check, shop, search, stream
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name='home'),
    path('user/', include('authentication.urls')),
    path('book/<pk>/<name>/', book_info),
    path('book/list/<name_group>/<sort>/', list_book),
    path('book/shoping-list/', shop_list_, name='list'),
    path('book/my-book/', my_book, name='my-book'),
    path('book/pin/', pin, name='pin'),
    path('book/shop/', shop, name='shop'),
    path('profile/check-email/', check),
    path('user/profile/', profile, name='profile'),
    path('book/search/', search, name='search'),
    path('stream/', stream, name='stream'),
    path('rest/', include('_rest_.urls')),
]

urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)