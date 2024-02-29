from django.http import JsonResponse
from .models import Image
from .serializers import ImageSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST'])
def image_list(request, format=None):
    if request.method == 'GET':
        #get all imagedeata
        images = Image.objects.all()
        #serialize them
        serializer = ImageSerializer(images, many=True)
        #import them
        return JsonResponse({'images': serializer.data})
    
    if request.method == 'POST':
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
@api_view(['GET', 'PUT', 'DELETE'])
def image_detail(request, id, format=None):
    
    try:
        image = Image.objects.get(pk=id)
    except Image.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ImageSerializer(image)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ImageSerializer(image, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
