"""pothole_detection URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),

    #URLS API POSTS
    #
    # path("api/listallaccpost", views.PostList.as_view(), name="post_listAPI"),
    # path("api/listallimagepost", views.PostList.as_view(), name="post_listAPI"),
    # path("api/uploadimagepost/", views.send_post, name="post_listAPIModified"),
    # path("api/deleteimagepost/<int:id>/", views.delete_post, name="delete post"),
    #
    # #URLS API USER
    #
    # path("api/listallusers", views.Garbage_UserList.as_view(), name="Garbage_UserListAPI"),
    #
    #  #not sure about this api
    # # path("postAPI/<int:pk>/", views.PostDetail.as_view(), name="post_details"),
    # # path("postAPI/<int:pk>/vote/", views.CreateVote.as_view(), name="create_vote"),
    #
    # path("api/appuser/login/", views.validate_Garbage_User_view, name="validate_Garbage_User"),
    # path("api/appuser/register/", views.Register_Garbage_User, name="Register_Garbage_User"),
    # path("api/userlikedpost/<int:uid>/", views.liked_post, name="getuserslikedspost"),
    # path("api/getuserpost/<int:uid>/", views.get_users_post, name="getuserspost"),
    # path("api/downvote/", views.downvote, name="downvote"),
    # path("api/filterpost/", views.filter_posts, name="filterpost"),
    # path("api/updateStatus/", views.update_status, name="updatestatus"),
    #
    #
    #
    #
    #
    # #API VOTES
    #
    # path("api/upvote/", views.upvote_view, name="Upvote"),
    # path("api/upvotelist/", views.Vote_table_list.as_view(), name="UpvoteTable"),#gives upvote table

]
