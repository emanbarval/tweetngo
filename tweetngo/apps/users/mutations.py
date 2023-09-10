import graphene
from django.contrib.auth import get_user_model, authenticate
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .models import User, FollowerRequest
from .types import UserType

def get_user_by_token(token):
    # Implementa la lógica para obtener un usuario por su token
    # Esto depende de cómo estés manejando la autenticación y los tokens en tu aplicación
    pass

class UserMutation(graphene.ObjectType):
    create_user = graphene.Field(UserType,
                                 username=graphene.String(required=True),
                                 email=graphene.String(required=True),
                                 password=graphene.String(required=True))

    login_user = graphene.Field(UserType,
                                username=graphene.String(required=True),
                                password=graphene.String(required=True))

    change_password = graphene.Field(UserType,
                                     old_password=graphene.String(required=True),
                                     new_password=graphene.String(required=True))

    restore_password = graphene.Field(graphene.Boolean,
                                      email=graphene.String(required=True))

    follow_user = graphene.Field(UserType,
                                 user_id=graphene.Int(required=True))

    accept_follower_request = graphene.Field(graphene.Boolean,
                                             request_id=graphene.Int(required=True))

    unfollow_user = graphene.Field(UserType,
                                   user_id=graphene.Int(required=True))

    def resolve_create_user(self, info, username, email, password):
        user = User.objects.create_user(username=username, email=email, password=password)
        return user

    def resolve_login_user(self, info, username, password):
        user = authenticate(username=username, password=password)
        if user:
            token = get_token(user)
            return user
        else:
            raise Exception('Invalid credentials')

    def resolve_change_password(self, info, old_password, new_password):
        token = info.context.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        user = get_user_by_token(token)
        if not user:
            raise Exception('Invalid token')
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return user
        else:
            raise Exception('Invalid password')

    def resolve_restore_password(self, info, email):
        request = info.context
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Handle case when user does not exist
            return False

        # Generate magic link URL
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = user.password  # Use the user's current password as the token for simplicity
        domain = get_current_site(request).domain
        magic_link_url = f"http://{domain}/reset-password/{uid}/{token}"

        # Send magic link to user's email
        subject = "Reset your password"
        message = render_to_string("reset_password_email.html", {
            "user": user,
            "magic_link_url": magic_link_url,
        })
        send_mail(subject, message, "from@example.com", [email])

        return True

    def resolve_follow_user(self, info, user_id):
        token = info.context.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        user = get_user_by_token(token)
        if not user:
            raise Exception('Invalid token')

        user_to_follow = User.objects.get(id=user_id)
        existing_request = FollowerRequest.objects.filter(follower=user, target_user=user_to_follow).first()
        if existing_request:
            raise Exception('Follow request already sent')

        # Crear una nueva solicitud de seguimiento
        follow_request = FollowerRequest(follower=user, target_user=user_to_follow)
        follow_request.save()

        return user

    def resolve_accept_follower_request(self, info, request_id):
        token = info.context.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        user = get_user_by_token(token)
        if not user:
            raise Exception('Invalid token')
        # Buscar la solicitud de seguimiento por su ID
        follower_request = FollowerRequest.objects.filter(id=request_id).first()
        if not follower_request:
            raise Exception('Follower request not found')

        # Verificar que el usuario actual es el objetivo de la solicitud
        if follower_request.target_user != user:
            raise Exception('You are not the target user of this request')

        # Marcar la solicitud como aceptada
        follower_request.is_accepted = True
        follower_request.save()

        user.profile.followers.add(follower_request.follower)
        return True

    def resolve_unfollow_user(self, info, user_id):
        token = info.context.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        user = get_user_by_token(token)
        if not user:
            raise Exception('Invalid token')

        user_to_unfollow = User.objects.get(id=user_id)
        user.profile.followers.remove(user_to_unfollow)
        return user