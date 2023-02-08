from django.urls import path
from perfectmatch.views import CustomerLoginView
from perfectmatch.views import CustomerRegistrationView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt import views as jwt_views
from django.conf.urls.static import static
from django.conf import settings
from perfectmatch import views 
urlpatterns = [
    path('login', CustomerLoginView.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup', CustomerRegistrationView.as_view()),
    path('findmatch', views.findmatches),
    path('addfriendrequest', views.friendrequests),
    path('friendrequest/<userid>/', views.friendrequestsdetail),
    path('getmatches/<userid>/', views.getmatches),
    path('addmatch', views.addmatches),
    path('deletematch', views.deletematches),
    path('updateprofilepic', views.updateprofilepic),
    path('updatebio', views.updatebio),
    path('blockuser', views.blockuser),
    path('reportuser', views.reportuser),
    path('getusers/<userid>/', views.getusers),
    path('getuser/<userid>/', views.getuser),
    path('getlikes/<userid>/', views.getlikes),
    path('addpayments', views.addpayments),
    path('allmatches', views.getallmatches),
    path('deleteallmatches', views.deleteallmatches),
    path('allusers', views.getallusers),
    path('deleteallusers', views.deleteallusers),
    path('deletelike/<userid>/', views.deletelike),
    path('updatedeviceid', views.updatedeviceid),
    path('testconnection', views.testconnection),
    path('testpushnotification', views.testpushnotification)
    ]