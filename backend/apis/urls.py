from django.urls import include, path
from rest_framework import routers
from .views import APIModelGetView
from django.conf.urls import static
from backend import settings
# define the router
router = routers.DefaultRouter()
 
# define the router path and viewset to be used
router.register('api', APIModelGetView)
 
# specify URL Path for rest_framework
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.BASE_URL)
