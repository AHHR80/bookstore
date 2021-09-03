from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from _rest_.models import book_table
from _rest_.serialization import book_table_s
from rest_framework import permissions
from rest_framework.decorators import permission_classes


class show(APIView):
    def get(self, request):
        query = book_table.objects.all()
        seri = book_table_s(query, many=True)
        return Response(data=seri.data, status=status.HTTP_200_OK)
    
    
class send(APIView):
    
    permission_classes = [permissions.IsAdminUser]
    
    def post(self, request):
        seri = book_table_s(data = request.data)
        if seri.is_valid():
            seri.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        