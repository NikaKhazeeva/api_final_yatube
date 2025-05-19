from rest_framework import serializers
from posts.models import Comment, Post, Follow, Group
from django.contrib.auth import get_user_model

User = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'text', 'created']


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate(self, data):
        request_user = self.context['request'].user
        target_user = data.get('following')

        if not target_user:
            raise serializers.ValidationError({
                'following': 'Поле обязательно для заполнения.'
            })

        if request_user == target_user:
            raise serializers.ValidationError({
                'following': 'Нельзя оформить подписку на самого себя.'
            })

        if Follow.objects.filter(user=request_user, following=target_user).exists():
            raise serializers.ValidationError({
                'following': 'Вы уже оформили подписку на этого пользователя.'
            })

        return data
