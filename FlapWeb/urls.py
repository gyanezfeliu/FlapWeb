"""FlapWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from LoadData import views

# TEMPLATE URLS!
# app_name = 'LoadData'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('monkey/sample', views.leer),
    path('monkey/search', views.search),
    path('monkey/analysis', views.to_analysis),
    path('monkey/make_analysis', views.make_analysis),
    path('monkey/plots/<int:id>', views.plots),
    path('monkey/upload', views.index),
    path('monkey/massupload', views.massUpload),
    path('monkey/plot', views.plot),
    ###### Para login
    path('LoadData/', include('LoadData.urls')),
    path('logout/', views.user_logout, name='logout'),
    path('special/', views.special, name='special'),
    ######
    path('', views.home, name='home')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
