from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from graphene_django.views import GraphQLView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from beauty_salon.schema import schema


urlpatterns = [
    path('admin/', admin.site.urls),
    path('drf-auth/', include("rest_framework.urls")),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/v1/', include('services.urls')),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/', include('notifications.urls')),
    path('api/v1/', include('rooms.urls')),
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema)),
    path('__debug__/', include('debug_toolbar.urls')),
    
    
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(
            template_name="swagger-ui.html", url_name="schema"
        ),
        name="swagger-ui",
    ),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns = [
    #     path('__debug__/', include('debug_toolbar.urls')),
    # ] + urlpatterns