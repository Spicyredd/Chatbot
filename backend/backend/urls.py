"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path

from apis.views import APIModelGetView,APIModelPostView,APIModelFilePostView

 
# import everything from views
 
 
# # specify URL Path for rest_framework
urlpatterns = [    
    path('api/messages/', APIModelGetView.as_view(), name='get_messages'),
    path('api/post/', APIModelPostView.as_view(), name='post_message'),
    path('api/filepost/', APIModelFilePostView.as_view(), name='post_file')
]
