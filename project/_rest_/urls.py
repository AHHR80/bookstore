from rest_framework.authtoken.views import obtain_auth_token

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import show, send

app_name = 'rest'

urlpatterns =[
    path('login /', obtain_auth_token, name='api-tokn-auth'),
    path('login/', include('rest_framework.urls')),
    path('book/show/', show.as_view()),
    path('book/make/', send.as_view()),
]


urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)