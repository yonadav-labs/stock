"""stock URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from general.views import *

admin.site.site_header = "Stock Administration"

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home, name="home"),
    url(r'^issue_offer/(?P<symbol>.*)', issue_offer, name="issue_offer"),
    url(r'^delete_offer$', delete_offer, name="delete_offer"),
    url(r'^offer_list/(?P<symbol>.*)', offer_list, name="offer_list"),

    url(r'^update_history_all$', update_history_all, name="update_history_all"),
    url(r'^update_history$', update_history, name="update_history"),
    url(r'^delete_history$', delete_history, name="delete_history"),
]
