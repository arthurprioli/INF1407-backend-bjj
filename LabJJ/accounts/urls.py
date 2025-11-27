from django.urls import path
from accounts import views
from django.urls import include

app_name = 'accounts'

urlpatterns = [
    path('token-auth/', views.CustomAuthToken.as_view(), name='token-auth'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('password_reset/',include('django_rest_passwordreset.urls',namespace='password_reset')),
]