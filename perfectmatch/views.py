from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from perfectmatch.serializers import UserLoginSerializer
from perfectmatch.serializers import RegisterUserSerializer
from perfectmatch.serializers import UserProfileSerializer
from perfectmatch.serializers import UserDataSerializer
from perfectmatch.serializers import FriendRequestSerializer
from perfectmatch.serializers import MatchesSerializer
from perfectmatch.models import Matches
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import RetrieveAPIView
from rest_framework import generics
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from perfectmatch.models import User
from perfectmatch.models import UserProfile
import json
from perfectmatch.models import FriendRequests
from rest_framework_simplejwt.tokens import SlidingToken, RefreshToken
class CustomerRegistrationView(generics.ListCreateAPIView):
    def post(self, request, format=None):
        request_data= request.data
        request.data._mutable=True
        request_data['isactive']=True
        isactive=True
        request.data._mutable=False
        serializer = RegisterUserSerializer(data=request_data)
        customerserizer=UserProfileSerializer(data=request_data)
        cid=0
        if serializer.is_valid():
            user=serializer.save()
            cid=user.id
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if customerserizer.is_valid():
            user=User.objects.get(id=cid)
            user.is_active=isactive
            user.save()
            try:
                customerserizer.save(user=user)
            except Exception as e:
                print(e)
                User.objects.get(id=cid).delete()
                return Response("Unable to register try again later", status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_201_CREATED)
        else:
            User.objects.get(id=cid).delete()
            return Response(customerserizer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerLoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

@api_view(['POST'])
def findmatches(request):
    data = request.data
    gnd=""
    gender=data['gender']
    blocklist=data['blocklist']
    if gender=="Male":
        gnd="Female"
    elif gender=="Female":
        gnd="Male"
    user=UserProfile.objects.filter(gender=gnd)
    serializer = UserDataSerializer(user,context={"request": request}, many=True)
    return Response(serializer.data)
  
@api_view(['GET'])
def getusers(request,userid):
    user = UserProfile.objects.filter(user_id=userid)
    serializer =UserDataSerializer(user, context={"request": request},many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getuser(request,userid):
    try:
        user = UserProfile.objects.get(user_id=userid)
        serializer =UserDataSerializer(user, context={"request": request})
        return Response(serializer.data)
    except UserProfile.DoesNotExist:
        return Response({"status":"fail","message":"user not found"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getallusers(request):
    user = UserProfile.objects.all()
    serializer =UserDataSerializer(user, context={"request": request},many=True)
    return Response(serializer.data)

@api_view(['GET'])
def deleteallusers(request):
    User.objects.all().delete()
    user = UserProfile.objects.all().delete()
    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def getmatches(request,userid):
    user=Matches.objects.filter(userid=userid).order_by('-id')
    serializer = MatchesSerializer(user, many=True)
    return Response(serializer.data)
  
@api_view(['POST'])
def deletematches(request):
    data = request.data
    userid=data['myuserid']
    otheruserid=data['otheruserid']
    try:
        matches1 = Matches.objects.get(userid=userid)
        matches2=Matches.objects.get(userid=otheruserid)
        matches1.delete()
        matches2.delete()
        return Response(status=status.HTTP_200_OK)
    except Matches.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
@api_view(['POST'])
def addmatches(request):
    data = request.data
    userid=data['userid']
    otheruserid=data['otheruserid']
    chatid=data['chatid']
    data1={"userid":userid,"otheruserid":otheruserid,"chatid":chatid}
    data2={"userid":otheruserid,"otheruserid":userid,"chatid":chatid}
    serializer1 = MatchesSerializer(data=data1)
    serializer2=MatchesSerializer(data=data2)
    if serializer1.is_valid():
        serializer1.save()
    else:
        return Response(serializer1.errors, status=status.HTTP_400_BAD_REQUEST)
    if serializer2.is_valid():
        serializer2.save()
    else:
        return Response(serializer2.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)



@api_view(['GET','DELETE'])
def friendrequestsdetail(request,userid):
    try:
        friends = FriendRequests.objects.get(touserid=userid)
    except FriendRequests.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
            serializer =FriendRequestSerializer(friends)
            return Response(serializer.data)
    elif request.method=='DELETE':
        friends.delete()
        return Response(status=status.HTTP_200_OK) 

@api_view(['GET'])
def getlikes(request, userid):
    likes=FriendRequests.objects.filter(touserid=userid)
    user = UserProfile.objects.filter(user_id__in=[like.fromuserid for like in likes])
    serializer =UserDataSerializer(user, context={"request": request}, many=True)
    return Response(serializer.data)



@api_view(['POST'])
def friendrequests(request):
    serializer = FriendRequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "message":"data saved"},status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def blockuser(request):
    data = request.data
    myuserid=data['userid']
    otheruserid=int(data['otheruserid'])
    try:
        transaction = UserProfile.objects.get(user_id=myuserid)
        if transaction.blocklist is None:
            blocklist=list()
            blocklist.append(otheruserid)
            transaction.blocklist=str(blocklist)
            transaction.save()
        else:
            blocklist=eval(transaction.blocklist)
            blocklist.append(otheruserid)
            transaction.blocklist=str(blocklist)
            transaction.save()
        return Response({"status":"success"}, status=status.HTTP_200_OK)
    except UserProfile.DoesNotExist:
        return Response({"status":"fail","message":"user not found"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def updateprofilepic(request):
    data = request.data
    myuserid=data['userid']
    photo=data['photo']
    try:
        transaction = UserProfile.objects.get(user_id=myuserid)
        transaction.photo1=photo
        transaction.save()
        return Response({"status":"success"}, status=status.HTTP_200_OK)
    except UserProfile.DoesNotExist:
        return Response({"status":"fail","message":"user not found"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def updatebio(request):
    data = request.data
    myuserid=data['userid']
    bio=data['bio']
    try:
        transaction = UserProfile.objects.get(user_id=myuserid)
        transaction.bio=bio
        transaction.save()
        return Response({"status":"success"}, status=status.HTTP_200_OK)
    except UserProfile.DoesNotExist:
        return Response({"status":"fail","message":"user not found"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def reportuser(request):
    data = request.data
    myuserid=data['userid']
    otheruserid=data['otheruserid']
    return Response({"status":"success"}, status=status.HTTP_200_OK)
@api_view(['POST'])
def addpayments(request):
    data = request.data
    userid=data['userid']
    paymentid=data['paymentid']
    subscription=data['subscription']
    subscriptiontype=data['subscriptiontype']
    try:
        transaction = UserProfile.objects.get(user_id=userid)
        transaction.paymentid=paymentid
        transaction.subscription=subscription
        transaction.subscriptiontype=subscriptiontype
        transaction.save()
        return Response({"status":"success"}, status=status.HTTP_200_OK)
    except UserProfile.DoesNotExist:
        return Response({"status":"fail","message":"user not found"}, status=status.HTTP_400_BAD_REQUEST)
 
    
