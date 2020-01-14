from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics
from .models import app_User,image_post, accelometer_post,Vote_table
from .serializers import image_postSerializer,accelometer_postSerializer,Vote_tableSerializer,app_UserSerializer
from rest_framework import status
from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
# from garbage_app.forms import PostForm, CommentForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.decorators import parser_classes
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
import logging
from rest_framework.parsers import MultiPartParser, FormParser
from math import sin, cos, sqrt, atan2
from math import radians, sin, cos, acos
import json
from .forms import StatusForm
from django.core import serializers

#log config
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

#list all users
class app_UserList(generics.ListCreateAPIView):
    queryset = app_User.objects.all()
    serializer_class = app_UserSerializer


#validate user API

@api_view(['POST'])
@parser_classes([JSONParser])
def validate_Garbage_User_view(request):
    dict = {}
    l = []

    try:
        email_id_received = request.data[0]["email_id"]
        password_received = request.data[0]["password"]
        req_user = app_User.objects.filter(email_id=email_id_received).first()
        # if Type(req_user)==None:
        #     return Response({"message":"User Not Found"})
        actual_password = req_user.password

        if actual_password == password_received:
            serializer = app_UserSerializer(req_user)
            dict["error"] = False
            dict["message"] = "Login Successful"
            dict["user"] = serializer.data

            l.append(dict)
            # new_dict={**dict,**serializer.data}
            # return Response(dict)
            return JsonResponse(l, safe=False)

        else:
            dict["message"] = "Incorrect Password"
            dict["error"] = True
            l.append(dict)

            return JsonResponse(l, safe=False)

    except:

        dict["error"] = True
        dict["message"] = "User not found"
        l.append(dict)
        return JsonResponse(l, safe=False)



#Register app_user API

@api_view(['POST'])
def Register_Garbage_User(request):
    serializer = app_UserSerializer(data=request.data)
    dict = {}
    if serializer.is_valid():
        email = request.data["email_id"]
        # logging.debug(email)
        # logging.debug(Garbage_User.objects.get(email_id=email))

        try:
            if app_User.objects.get(email_id=email) != None:
                dict["error"] = True
                dict["message"] = "User with same emailID already exists"
                return Response(dict)

        except app_User.DoesNotExist:
            serializer.save()
            required_user = app_User.objects.get(email_id=email)
            user_id = required_user.id
            dict["message"] = "Succesfully registered"
            dict["error"] = False
            dict["user"] = serializer.data

            return Response(dict)

    return Response({"message": "registration failed"})

#list all image_post

class image_postList(generics.ListCreateAPIView):
    # logging.debug(request.data)
    queryset = image_post.objects.all()
    serializer_class = image_postSerializer

#list all accelometer_post

class accelometer_postList(generics.ListCreateAPIView):
    # logging.debug(request.data)
    queryset = accelometer_post.objects.all()
    serializer_class = accelometer_postSerializer

#image_post Post from android
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def send_post(request):
    dict = {}
    # serializer=PostSerializer(data=request.data)
    # null=None
    serializer = PostSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        dict["message"] = "successful"
        dict["error"] = False
        dict["Post"] = serializer.data
        # queryset=Post.objects.all()
        return Response(dict)
    dict["message"] = "Unsuccessful"
    dict["error"] = True
    return Response(request.data)


#accelometer_post Post from android
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def send_post(request):
    dict = {}
    # serializer=PostSerializer(data=request.data)
    # null=None
    serializer = PostSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        dict["message"] = "successful"
        dict["error"] = False
        dict["Post"] = serializer.data
        # queryset=Post.objects.all()
        return Response(dict)
    dict["message"] = "Unsuccessful"
    dict["error"] = True
    return Response(request.data)