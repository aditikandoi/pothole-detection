from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics
from .models import Post, Vote, Comment, Garbage_User, Vote_table
from .serializers import PostSerializer, VoteSerializer, Garbage_UserSerializer, Vote_tableSerializer
from rest_framework import status
from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from garbage_app.forms import PostForm, CommentForm
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

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


# Create your views here.
@api_view(["GET"])
def delete_post(request, id):
    dict = {}
    try:
        entry = Post.objects.get(id=id)
        entry.delete()
        dict["message"] = "Successfully deleted"
    except:
        dict["message"] = "Error"
        return JsonResponse(dict)
    return JsonResponse(dict, safe=False)


def view_all_users(request):
    return render(request, "garbage_app/usersList.html", {'users_list': Garbage_User.objects.all()})


def view_all_posts(request):
    return render(request, "garbage_app/post_list.html", {'post_list': Post.objects.all()})


def index(request):
    return render(request, "garbage_app/home.html")


def base_page(request):
    return render(request, "garbage_app/base.html")


class Garbage_UserList(generics.ListCreateAPIView):
    queryset = Garbage_User.objects.all()
    serializer_class = Garbage_UserSerializer


@api_view(['POST'])
@parser_classes([JSONParser])
def validate_Garbage_User_view(request):
    dict = {}
    l = []

    try:
        email_id_received = request.data[0]["email_id"]
        password_received = request.data[0]["password"]
        req_user = Garbage_User.objects.filter(email_id=email_id_received).first()
        # if Type(req_user)==None:
        #     return Response({"message":"User Not Found"})
        actual_password = req_user.password

        if actual_password == password_received:
            serializer = Garbage_UserSerializer(req_user)
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


@api_view(['POST'])
def Register_Garbage_User(request):
    serializer = Garbage_UserSerializer(data=request.data)
    dict = {}
    if serializer.is_valid():
        email = request.data["email_id"]
        # logging.debug(email)
        # logging.debug(Garbage_User.objects.get(email_id=email))

        try:
            if Garbage_User.objects.get(email_id=email) != None:
                dict["error"] = True
                dict["message"] = "User with same emailID already exists"
                return Response(dict)

        except Garbage_User.DoesNotExist:
            serializer.save()
            required_user = Garbage_User.objects.get(email_id=email)
            user_id = required_user.id
            dict["message"] = "Succesfully registered"
            dict["error"] = False
            dict["user"] = serializer.data

            return Response(dict)

    return Response({"message": "registration failed"})


class PostList(generics.ListCreateAPIView):
    # logging.debug(request.data)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


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


@api_view(["POST"])
def upvote_view(request):
    # initialize_logger()
    dict = {}

    try:

        serializer = Vote_tableSerializer(data=request.data)
        logging.debug("Data Received")
        logging.debug(request.data["post_id"])
        received_post_id = request.data["post_id"]
        received_user_id=request.data["user_id"]
        logging.debug(received_post_id)
        post_obj = Post.objects.get(id=received_post_id)
        logging.debug(post_obj.id)

        # if len(Vote_table.objects.filter(user_id=received_user_id).filter(post_id=received_post_id))!=0:
        #     return Response({"message":"Already liked"})


        if serializer.is_valid():
            post_obj.vote_count += 1
            post_obj.save()
            serializer.save()
            dict["error"] = False
            dict["message"] = "Upvote Successful"
            dict["send_data"] = serializer.data
            dict["updated vote count"] = post_obj.vote_count
            return Response(dict)
        else:

            return Response({"message": "Already Liked"})

    except Exception as e:
        logging.fatal(e, exc_info=True)
        dict["error"] = True
        dict["message"] = "Upvote Failed"
        dict["send_data"] = request.data
        return Response(dict)


@api_view(["GET"])
def get_users_post(request, uid):
    try:
        user_post = Post.objects.filter(author=uid).values()
        return Response(list(user_post))
    except:
        return Response({"message": "Failed"})


@api_view(["POST"])
def downvote(request):
    try:
        uid = request.data["user_id"]
        pid = request.data["post_id"]
        post = Post.objects.get(id=pid)
        logging.debug(post.vote_count)
        post.vote_count -= 1
        logging.debug("check 1")
        post.save()
        logging.debug("check 2")
        entry = Vote_table.objects.filter(user_id=uid).filter(post_id=pid)
        logging.debug("check 3")

        entry.delete()
        return Response({"message": "successful", "updated_vote_count": post.vote_count})
    except:
        return Response({"message": "Failed"})


@api_view(["GET"])
def liked_post(request, uid):
    try:

        entry = Vote_table.objects.filter(user_id=uid).values()

        logging.debug(list(entry))
        # serializer=Vote_tableSerializer(data=entry,many=True)
        # if serializer.is_valid():
        return Response(list(entry))


    except:
        logging.debug("Exception")
        return Response({"message": "Failed"})


@api_view(["GET"])
def get_users_post(request, uid):
    try:
        users_post = Post.objects.filter(author=uid).values()
        serializer = PostSerializer(users_post)

        return Response([users_post])

    except:
        return Response({"message": "Failed"})


class Vote_table_list(generics.ListCreateAPIView):
    # logging.debug(request.data)
    queryset = Vote_table.objects.all()
    serializer_class = Vote_tableSerializer


class PostDetail(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CreateVote(APIView):
    serializer_class = VoteSerializer

    def post(self, request, pk):
        voted_by = request.data.get("voted_by")
        data = {"post": pk, "voted_by": voted_by}
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            vote = serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.all()


@api_view(['POST'])
def filter_posts(request):

    try:
        to_send = []
        json_object=json.loads(request.body)[0]
        logging.debug(json_object)
        slat = radians(json_object["latitude"])
        slon = radians(json_object["longitude"])
        radius = json_object["radius"]
        all_posts = Post.objects.all()
        i = 0
        for post in all_posts:

            elat = radians(post.latitude)
            elon = radians(post.longitude)

            #
            # if 6371.01* acos(sin(slat) * sin(elat) + cos(slat) * cos(elat) * cos(slon - elon))<=radius:
            #     serialized_obj = serializers.serialize('json', [post, ])
            #     to_send.append(serialized_obj)

            if 6371.01 * 1000 * acos(sin(slat) * sin(elat) + cos(slat) * cos(elat) * cos(slon - elon)) <= radius:
                serializer = PostSerializer(post)
                to_send.append(serializer.data)

        # logging.debug(list(to_send))
        return Response(to_send)
    except Exception as e:
        logging.debug(e)
        return Response(to_send)


class PostDetailView(DetailView):
    model = Post


class UserDetailView(DetailView):
    model = Garbage_User


class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'garbage_app/post_detail.html'

    form_class = PostForm()

    model = Post


class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'garbage_app/post_list.html'

    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'garbage_app/post_detail.html'
    form_class = PostForm
    model = Post


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'garbage_app/comment_form.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)


@api_view(["POST"])
def update_status(request):
    try:

        # form=StatusForm(request.POST)
        # status=request.data['status']
        # uid = request.data["user_id"]
        pid = request.data["post_id"]

        status = request.data["status"]
        post = Post.objects.get(id=pid)
        post.status = status
        post.save()
        serializer = PostSerializer(post)
        return render(request,"garbage_app/post_list.html",{"post_list":Post.objects.all()})
    except Exception as e:
        logging.debug(e)
        return Response({"message": "Failed"})