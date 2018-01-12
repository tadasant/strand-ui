from django.conf import settings
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from app.api.views import CustomObtainAuthTokenView


urlpatterns = [
    path('auth-token', CustomObtainAuthTokenView.as_view(), name='auth-token'),
    path('graphql', csrf_exempt(GraphQLView.as_view(graphiql=settings.ENABLE_GRAPHIQL)))
]
