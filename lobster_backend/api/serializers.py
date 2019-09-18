from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User, UserRelations

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], 
                                        validated_data['password'])

        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

class RelationSerializer(serializers.ModelSerializer):
    subscriber_id = serializers.IntegerField()
    target_username = serializers.CharField()

    def create(self, validated_data):
        user_subscriber = User.objects.get(id=validated_data['subscriber_id'])
        user_target = User.objects.get(username=validated_data['target_username'])
        relation = UserRelations.objects.create(subscriber=user_subscriber, target=user_target)

        return relation

    def delete(self, subscriber_id, target_username):
        UserRelations.objects.get(subscriber__id=subscriber_id, target__username=target_username).delete()

    class Meta:
        model = UserRelations
        fields = ('subscriber_id', 'target_username')