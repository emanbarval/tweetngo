import graphene
from apps.users.schema import Query as QueryUserThings
#from apps.posts.schema import Query as QueryPostThings
from apps.users.schema import Mutation as UserThings
#from apps.posts.schema import Mutation as PostsThings


class Query(QueryUserThings, QueryPostThings, graphene.ObjectType):
   pass

class Mutation(UserThings, PostsThings, graphene.ObjectType):
   pass

schema = graphene.Schema(query=Query, mutation=Mutation) 