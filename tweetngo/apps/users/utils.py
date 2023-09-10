from graphql_jwt.shortcuts import get_user_by_token

def getting_user(info):
    token = info.context.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
    user = get_user_by_token(token)
    if not user:
        raise Exception('Invalid token')
    return user