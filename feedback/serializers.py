from rest_framework import serializers

from .models import Comment, Like, Favorite


class LikeSerializer(serializers.Serializer):
    project = serializers.CharField()

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["likes"] = Like.objects.filter(project=instance.project, like=True).count()
        return rep


class FanSerializer(serializers.Serializer):
    user = serializers.CharField(required=True)


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    content_type = serializers.StringRelatedField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'user', 'content_type', 'object_id', 'comment', 'created_at', 'updated_at', 'parent', 'replies')

    def get_user(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def get_replies(self, obj):
        replies = Comment.objects.filter(parent=obj)
        return CommentSerializer(replies, many=True, context=self.context).data


