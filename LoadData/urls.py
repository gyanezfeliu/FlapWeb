from django.urls import path
from LoadData import views

# TEMPLATE URLS!
app_name = 'LoadData'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),

]
