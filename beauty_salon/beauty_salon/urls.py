from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .yasg import urlpatterns as doc_urls
from graphene_django.views import GraphQLView
from beauty_salon.schema import schema


urlpatterns = [
    path('admin/', admin.site.urls),
    path('drf-auth/', include("rest_framework.urls")),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/v1/', include('services.urls')),
    path('api/v1/users/', include('users.urls')),
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema)),
    path('__debug__/', include('debug_toolbar.urls')),
]

urlpatterns += doc_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns = [
    #     path('__debug__/', include('debug_toolbar.urls')),
    # ] + urlpatterns