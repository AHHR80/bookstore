from django.urls import path

from .views import sing_up, log_in, log_out, check

app_name="authentication"

urlpatterns = [
    path('register/', sing_up ,name='register'),
    path('log-in/', log_in,name='login'),
    path('log-out/', log_out,name='logout'),
    path('check/', check,name='check'),
]

