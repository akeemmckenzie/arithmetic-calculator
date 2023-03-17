# calculator/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'operations', views.OperationViewSet , basename= 'operations')
router.register(r'records', views.RecordViewSet, basename='record')

urlpatterns = [
    path('signup/', views.UserCreate.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh_token'),
    path('user/', views.user_detail, name='user_details'),
    path('operations/addition/', views.addition, name='addition'),
    path('records/<int:record_id>/', views.delete_record, name='delete_record'),
    path('operations/subtraction/', views.subtraction, name='subtraction'),
    path('operations/multiplication/', views.multiplication, name='multiplication'),
    path('operations/division/', views.division, name='division'),
    path('operations/square_root/', views.square_root, name='square_root'),
    path('operations/random_string/', views.random_string, name='random_string'),
] + router.urls


