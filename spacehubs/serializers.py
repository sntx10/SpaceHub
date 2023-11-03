from rest_framework import serializers
from django.contrib.auth import get_user_model

from feedback.models import Like, Comment
from feedback.serializers import CommentSerializer
from feedback.services import is_commented
from spacehubs.models import News, Blog, PodCast, Project, Post
from django.contrib.contenttypes.models import ContentType


# Create your serializers here.

User = get_user_model()


def enhance_representation(self, instance):
    rep = super().to_representation(instance)
    request = self.context.get("request")
    user = request.user if request else None

    current_content_type = ContentType.objects.get_for_model(instance)
    rep["likes"] = Like.objects.filter(content_type=current_content_type, object_id=instance.id, like=True).count()

    comments = Comment.objects.filter(content_type=current_content_type, object_id=instance.id)
    rep['comments'] = CommentSerializer(comments, many=True, context=self.context).data

    if user:
        rep['is_commented'] = Comment.objects.filter(content_type=current_content_type, object_id=instance.id,
                                                     user=user).exists()
    else:
        rep['is_commented'] = False

    return rep


class TheNewsSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)  # добавляем новое поле для комментариев

    class Meta:
        model = News
        fields = ('id', "title", "content", "date_posted", "expanded_date_posted", "comments", )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get("request")
        user = request.user if request else None

        news_content_type = ContentType.objects.get_for_model(instance)

        rep["likes"] = Like.objects.filter(content_type=news_content_type, object_id=instance.id, like=True).count()

        return rep

    def get_comments(self, obj):
        """
        Получить все комментарии для данной новости.
        """
        comments = Comment.objects.filter(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id)
        return CommentSerializer(comments, many=True).data


class BlogSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        fields = ('id', "category", "title", "description", "date_posted", "expanded_date_posted", "comments")

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get("request")
        user = request.user if request else None
        blog_content_type = ContentType.objects.get_for_model(instance)
        rep["likes"] = Like.objects.filter(content_type=blog_content_type, object_id=instance.id, like=True).count()
        return rep

    def create(self, validated_data):
        user = self.context.get("request").user

        validated_data["author"] = user
        return super(BlogSerializer, self).create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', "blog", "title", 'category', "content", "date_posted", "expanded_date_posted", "comments", 'category')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get("request")
        user = request.user if request else None
        post_content_type = ContentType.objects.get_for_model(instance)
        rep["likes"] = Like.objects.filter(content_type=post_content_type, object_id=instance.id, like=True).count()
        return rep

    def create(self, validated_data):
        user = self.context.get("request").user
        validated_data["author"] = user
        return super(PostSerializer, self).create(validated_data)


class PodCastSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = PodCast
        fields = ('id', "title", "category", "audio_file", "description", "category", "date_posted", "expanded_date_posted", "comments")

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get("request")
        user = request.user if request else None
        podcast_content_type = ContentType.objects.get_for_model(instance)
        rep["likes"] = Like.objects.filter(content_type=podcast_content_type, object_id=instance.id, like=True).count()
        return rep

    def create(self, validated_data):
        user = self.context.get("request").user
        validated_data["author"] = user
        return super(PodCastSerializer, self).create(validated_data)


class ProjectSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='user.email')
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('id', "title", "category", "description", "code", "date_posted", "expanded_date_posted",
                  "author", "location", "views_count", "comments")

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get("request")
        user = request.user if request else None

        project_content_type = ContentType.objects.get_for_model(instance)
        rep["likes"] = Like.objects.filter(content_type=project_content_type, object_id=instance.id, like=True).count()

        comments = Comment.objects.filter(content_type=project_content_type, object_id=instance.id)
        rep['comments'] = CommentSerializer(comments, many=True, context=self.context).data

        if user:
            rep['is_commented'] = Comment.objects.filter(content_type=project_content_type, object_id=instance.id,
                                                         user=user).exists()
        else:
            rep['is_commented'] = False

        return rep

    def create(self, validated_data):
        author = self.context['request'].user
        return self.Meta.model.objects.create(author=author, **validated_data)



