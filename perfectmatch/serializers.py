from rest_framework import serializers
from perfectmatch.models import User
from perfectmatch.models import UserProfile
from perfectmatch.models import FriendRequests
from perfectmatch.models import Matches
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
class UserLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        credentials = {
            'email': '',
            'password': attrs.get("password")
        }
        profile_obj=UserProfile.objects.filter(email=attrs.get("email")).first()
        if profile_obj:
            credentials['email'] = profile_obj.email
        data=super().validate(credentials)
        refresh = self.get_token(self.user)
        request = self.context.get('request')
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['email'] = self.user.email
        data['user_id']= self.user.pk
        data['name']=profile_obj.name
        data['bio']=profile_obj.bio
        data['gender']=profile_obj.gender
        data['religion']=profile_obj.religion
        data['age']=profile_obj.age
        data['relationtype']=profile_obj.relationtype
        data['subscriptiontype']=profile_obj.subscriptiontype
        data['subscription']=profile_obj.subscription
        data['paymentid']=profile_obj.paymentid
        data['photo1']=request.build_absolute_uri(profile_obj.photo1.url)
        data['photo2']=request.build_absolute_uri(profile_obj.photo2.url)
        data['photo3']=request.build_absolute_uri(profile_obj.photo3.url)
        data['photo4']=request.build_absolute_uri(profile_obj.photo4.url)
        data['photo5']=request.build_absolute_uri(profile_obj.photo5.url)
        data['reportlist']=profile_obj.reportlist
        data['blocklist']=profile_obj.blocklist
        return data
class ChangePasswordSerializer(serializers.ModelSerializer):
    newpassword = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirmpassword = serializers.CharField(write_only=True, required=True)
    oldpassword = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ('oldpassword', 'newpassword', 'confirmpassword')
    def validate(self, attrs):
        if attrs['newpassword'] != attrs['confirmpassword']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"oldpassword": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['newpassword'])
        instance.save()
        return instance

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','password')
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
class UserProfileSerializer(serializers.ModelSerializer):
    photo1 = serializers.ImageField(required=False)
    photo2 = serializers.ImageField(required=False)
    photo3 = serializers.ImageField(required=False)
    photo4 = serializers.ImageField(required=False)
    photo5 = serializers.ImageField(required=False)
    class Meta:
        model=UserProfile
        fields= ('user_id','isactive','name','bio','gender','email','age','religion','relationtype','subscriptiontype','subscription','paymentid','photo1','photo2','photo3','photo4','photo5','reportlist','blocklist')


class UserDataSerializer(serializers.ModelSerializer):
    photo1 = serializers.SerializerMethodField()
    photo2 = serializers.SerializerMethodField()
    photo3 = serializers.SerializerMethodField()
    photo4 = serializers.SerializerMethodField()
    photo5 = serializers.SerializerMethodField()
    class Meta:
        model=UserProfile
        fields= ('user_id','isactive','name','bio','gender','email','age','religion','relationtype','subscriptiontype','subscription','paymentid','photo1','photo2','photo3','photo4','photo5','reportlist','blocklist')
    def get_photo1(self, obj):
        try:
            request = self.context.get('request')
            return obj.photo1.url
        except Exception as e:
            return "null"

    def get_photo2(self, obj):
        try:
            request = self.context.get('request')
            return obj.photo2.url
        except Exception as e:
            return "null"

    def get_photo3(self, obj):
        try:
            request = self.context.get('request')
            return obj.photo3.url
        except Exception as e:
            return "null"
    def get_photo4(self, obj):
        try:
            request = self.context.get('request')
            return obj.photo4.url
        except Exception as e:
            return "null"
    def get_photo5(self, obj):
        try:
            request = self.context.get('request')
            return obj.photo5.url
        except Exception as e:
            return "null"

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model=FriendRequests
        fields= ('fromuserid','touserid')

class MatchesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Matches
        fields= ('userid','otheruserid','chatid')



