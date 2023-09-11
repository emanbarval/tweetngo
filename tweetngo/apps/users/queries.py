import graphene
from .types import ProfileType, FollowingType, FollowerType, FollowerRequestType # , UserType
from .models import Profile, User # , FollowerRequest
from .utils import getting_user

class UserQuery(graphene.ObjectType):
    profiles = graphene.List(ProfileType)
    following = graphene.List(FollowingType)
    followers = graphene.List(FollowerType)
    follower_requests = graphene.List(FollowerRequestType)

    def resolve_profiles(self, info):
        return Profile.objects.all()

    def resolve_following(self, info):
        user = getting_user(info) 
        return user.profile.followers.all()

    def resolve_followers(self, info):
        user = getting_user(info)
        return User.objects.filter(profile__followers=user)

    def resolve_follower_requests(self, info):
        user = getting_user(info)
        return user.follower_requests.all()