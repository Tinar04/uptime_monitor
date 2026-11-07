from django.shortcuts import render
import json
from .serializers import SiteSerializer,CheckSerializer
from .models import Site,Check
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from . services import run_check
from django.shortcuts import get_object_or_404
from django.db.models import Avg

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
    site = get_object_or_404(Site,id=id)
    obj = run_check(site)
    serializer = CheckSerializer(obj)
    return Response(serializer.data,status=status.HTTP_201_CREATED)

@api_view(['GET'])  
def check_history(request,id):
    site = get_object_or_404(Site,id=id)

    checks  = site.checks.order_by('-checked_at')
    serializer = CheckSerializer(checks,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['PATCH','DELETE'])
def site_detail(request,id):
    site = get_object_or_404(Site,id=id)

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
@api_view(['GET'])
def stats_view(request, id):
    site = get_object_or_404(Site,id=id)

    total_checks = site.checks.count()
    up_checks = site.checks.filter(status='UP').count()
    uptime_percent = round(up_checks / total_checks * 100, 2) if total_checks > 0 else 0
    avg = site.checks.aggregate(Avg('response_time_ms'))['response_time_ms__avg']
    avg_response_time = round(avg, 2) if avg is not None else 0

    stats = {
    "total_checks": total_checks,
    "up_checks": up_checks,
    "uptime_percent": uptime_percent,
    "avg_response_ms": avg_response_time,
    }
    return Response(stats, status=status.HTTP_200_OK)





        
