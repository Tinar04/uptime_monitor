from django.shortcuts import render
import json
from .serializers import SiteSerializer,CheckSerializer
from .models import Site,Check
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from . services import run_check
# Create your views here.
@api_view(['GET','POST'])
def site_view(request):
    if request.method == 'POST':
        serializer  = SiteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {"message":"site has created succefully "}
            return Response(response_data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        sites = Site.objects.all()
        serializer = SiteSerializer(sites,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)



    
@api_view(['POST'])      
# “run a check right now for site X and save the result.”
def check_site(request,id):
    # build a check for site whos id = id
    site = Site.objects.get(id=id)
    obj = run_check(site)
    serializer = CheckSerializer(obj)
    return Response(serializer.data,status=status.HTTP_201_CREATED)

@api_view(['GET'])  
def check_history(request,id):
    try:
        site = Site.objects.get(id=id)
    except Site.DoesNotExist:
        return Response({"message": "Site not found"}, status=status.HTTP_404_NOT_FOUND)

    checks  = site.checks.order_by('-checked_at')
    serializer = CheckSerializer(checks,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['PATCH','DELETE'])
def site_detail(request,id):
    try:
        site = Site.objects.get(id=id)
    except Site.DoesNotExist:
        return Response({"Message":"Site Not Found"},status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PATCH':
        serializer = SiteSerializer(site,data = request.data,partial = True)
        if serializer.is_valid():
            serializer.save()

            response_data = {"Message":'Site updated sucessfully'}
            return Response(response_data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        site.delete()
        response_data = {"Message":"Site delete succefully"}
        return Response(response_data,status=status.HTTP_200_OK)



        




        
