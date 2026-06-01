from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, 
                                     min_length=8,
                                     style= {'input_type': 'password'},
                                     trim_whitespace = False,
                                     )

    class Meta:
        model = User
        fields = ['id', 'username','password', 'email', 'first_name', 'last_name']
    
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data["username"],
            password = validated_data["password"],
            email = validated_data.get("email",''),
            first_name = validated_data.get("first_name",''),
            last_name = validated_data.get("last_name",''),
        )
        return user