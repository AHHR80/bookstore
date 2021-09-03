from rest_framework import serializers
from .models import book_table
from testapp.models import MyUser

class book_table_s(serializers.ModelSerializer):
    class Meta:
        model = book_table
        fields = '__all__'