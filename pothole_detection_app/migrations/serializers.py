from rest_framework import serializers
from .models import Post,Vote,Garbage_User,Vote_table



class PostSerializer(serializers.ModelSerializer):
    # votes=VoteSerializer(many=True,required=False)

    class Meta:
        model=Post
        fields="__all__"


class PostappSerializer(serializers.ModelSerializer):
    # votes=VoteSerializer(many=True,required=False)

    class Meta:
        model=Post
        fields="__all__"


class Garbage_UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=Garbage_User
        fields="__all__"

class Vote_tableSerializer(serializers.ModelSerializer):

    class Meta:
        model=Vote_table
        fields="__all__"