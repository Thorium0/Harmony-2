
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('username',
                  'password',
                  )

    
    def update(self, instance, validated_data):

        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance



class ProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Profile
        fields = ('image',
                  'user'
                  )
    
    

    