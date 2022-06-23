"""Epic_Events URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import ClientView, ContractView, EventView, ReadOnlyClient, ReadOnlyContract, ReadOnlyEvent

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('ReadOnlyClient/', ReadOnlyClient.as_view()),
    path('ReadOnlyContract/', ReadOnlyContract.as_view()),
    path('ReadOnlyEvent/', ReadOnlyEvent.as_view()),
    path('Client/', ClientView.as_view(), name='Client'),
    path('Client/<client_id>', ClientView.as_view(), name='Client'),
    path('Contract/', ContractView.as_view(), name='Contract'),
    path('Contract/<client_id>/<contract_id>', ContractView.as_view(), name='Contract'),
    path('Event/', EventView.as_view(), name='Event'),
    path('Event/<client_id>/<contract_id>/<event_id>', EventView.as_view(), name='Event'),
]
