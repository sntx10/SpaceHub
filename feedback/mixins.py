from django.core.exceptions import ValidationError
from django.utils.datastructures import MultiValueDictKeyError
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from feedback import services
from feedback.models import Comment


class LikeMixin:

    @swagger_auto_schema(tags=['like'])
    @action(methods=['POST'], detail=True)
    def like(self, request, pk=None):
        obj = self.get_object()
        user = request.user
        status_ = services.like_unlike(user=user, obj=obj)
        return Response({'status': status_}, status=status.HTTP_200_OK)

    @swagger_auto_schema(tags=['like'])
    @action(methods=['GET'], detail=False, url_path='liked-items')
    def get_liked_items(self, request):
        user = request.user
        liked_items = services.get_liked_objects_for_user(user, model=self.queryset.model)
        serializer = self.get_serializer(liked_items, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(tags=['like'])
    @action(methods=['GET'], detail=True)
    def fans(self, request, pk=None):
        obj = self.get_object()
        return Response(services.get_fans(obj=obj), status=status.HTTP_200_OK)


class FavoriteMixin:
    favorite_model = None  # это должно быть определено в каждом ViewSet
    target_model = None   # это тоже должно быть определено в каждом ViewSet

    @swagger_auto_schema(tags=['favorite'])
    @action(methods=['POST'], detail=True)
    def favorite(self, request, pk=None):
        obj = self.get_object()
        user = request.user

        status_ = services.toggle_favorite_status(user=user, obj=obj)

        if not status_:
            return Response({'error': 'Action not successful.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                'status': status_,
                'user': user.email,
                'object': obj.title
            },
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(tags=['favorite'])
    @action(methods=['GET'], detail=False)
    def get_favorites(self, request):
        favorites = services.get_favorites_for_model(user=request.user, model=self.target_model)

        if not favorites:
            return Response({'error': 'No favorites found.'}, status=status.HTTP_404_NOT_FOUND)

        data = []  # универсальное имя вместо project_data
        for obj in favorites:
            data.append({
                'title': obj.title,
                # добавьте другие атрибуты по мере необходимости
            })

        return Response({'favorites': data}, status=status.HTTP_200_OK)


class CommentMixin:
    comment_model = None  # Должен быть переопределен в наследующем классе
    target_model = None  # Должен быть переопределен в наследующем классе

    @swagger_auto_schema(tags=['comment'])
    @action(methods=['POST'], detail=True)
    def give_comment(self, request, pk=None):
        try:
            comment_text = request.data['comment']
            user = request.user
            obj = self.get_object()
            status_ = services.give_comment(user=user, obj=obj,
                                             comment=comment_text, model=self.comment_model)
            return Response(
                {
                    'status': status_,
                    'user_email': user.email,
                    'comment': comment_text
                }, status=status.HTTP_200_OK
            )
        except KeyError:
            raise ValidationError('comment field required')

    @action(methods=['POST'], detail=True, url_path='reply-to-comment')
    def reply_to_comment(self, request, *args, **kwargs):
        try:
            reply_text = request.data['reply']
            user = request.user
            parent_comment_id = request.data['comment_id']

            status_ = services.reply_to_comment(user=user, comment_id=parent_comment_id,
                                                 reply_text=reply_text, model=self.comment_model)

            return Response(
                {
                    'status': status_,
                    'user_name': user.first_name,
                    'reply': reply_text
                }, status=status.HTTP_200_OK
            )
        except (MultiValueDictKeyError, KeyError):
            raise ValidationError('Required fields: reply and comment_id')

    @swagger_auto_schema(tags=['comment'])
    @action(detail=True, methods=['POST'], url_path='edit-comment')
    def edit_comment(self, request, pk=None):
        comment_id = request.data.get('comment_id')
        new_text = request.data.get('new_text')
        if not comment_id or not new_text:
            return Response({"error": "Both comment_id and new_text are required!"}, status=status.HTTP_400_BAD_REQUEST)

        result = services.edit_comment(comment_id, request.user, new_text, model=self.comment_model)

        if result == 'Comment updated':
            return Response({"status": result}, status=status.HTTP_200_OK)
        else:
            return Response({"error": result}, status=status.HTTP_403_FORBIDDEN)

    @swagger_auto_schema(tags=['comment'])
    @action(detail=True, methods=['POST'])
    def del_comment(self, request, pk=None):
        comment_id = request.data.get('comment_id')
        if not comment_id:
            return Response({"error": "Comment ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        try:
            services.delete_specific_comment(comment_id, user, model=self.comment_model)
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Comment.DoesNotExist as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        return Response({"success": "Comment successfully deleted."}, status=status.HTTP_200_OK)