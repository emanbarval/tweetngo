import graphene
from graphene_django.types import DjangoObjectType
from django.db import models
from .models import User, Profile, FollowerRequest

class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile

class UserType(DjangoObjectType):
    profile = graphene.Field(ProfileType)
    is_following = graphene.Boolean()
    following = graphene.List(lambda:UserType)
    follower_requests = models.ManyToManyField(FollowerRequest, related_name='target_user')

    class Meta:
        model = User
        fields = '__all__'

    def resolve_profile(self, info):
        return self.profile
    
    def resolve_is_following(self, info):
        user = info.context.user
        if user.is_anonymous:
            return False
        return self.profile.followers.filter(id=user.id).exists()
    
    @classmethod
    def get_node(cls, info, id):
        # Aquí puedes obtener un único objeto de usuario utilizando el ID
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None
    
    def resolve_following(self, info):
        return self.profile.followers.all()
    
    def resolve_follower_requests(self, info):
           return self.follower_requests.all()


class FollowingType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username')

class FollowerType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username')

class FollowerRequestType(DjangoObjectType):
    class Meta:
        model = FollowerRequest
        fields = '__all__'