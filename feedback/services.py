from .models import Like, Favorite
from .serializers import FanSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType


def like_unlike(user, obj):
    """
    Устанавливает или убирает лайк для объекта.

    :param user: Пользователь, который ставит или убирает лайк.
    :param obj: Объект, для которого выполняется действие.
    :return: Статус действия: 'liked' если лайк установлен, 'unliked' если лайк убран.
    """
    content_type = ContentType.objects.get_for_model(obj.__class__)
    like_obj, is_created = Like.objects.get_or_create(user=user, content_type=content_type, object_id=obj.id)
    if not is_created:
        like_obj.delete()
        return 'unliked'
    else:
        like_obj.like = True
        like_obj.save()
        return 'liked'


def get_liked_objects_for_user(user, model):
    """
    Получает все объекты определенной модели, на которые пользователь поставил лайк.

    :param user: Пользователь, для которого выполняется поиск.
    :param model: Модель объектов для поиска.
    :return: Список объектов модели, на которые пользователь поставил лайк.
    """
    content_type = ContentType.objects.get_for_model(model)
    liked_ids = Like.objects.filter(user=user, content_type=content_type).values_list('object_id', flat=True)
    return model.objects.filter(id__in=liked_ids)


def get_fans(obj):
    """
    Получает список пользователей, которые поставили лайк на объект.

    :param obj: Объект, для которого ищутся "фанаты".
    :return: Список пользователей, которые поставили лайк на объект.
    """
    content_type = ContentType.objects.get_for_model(obj.__class__)
    fans = Like.objects.filter(content_type=content_type, object_id=obj.id)
    if fans.exists():
        serializer = FanSerializer(fans, many=True)
        return serializer.data
    return []


def toggle_favorite_status(user, obj):
    """
    Добавляет объект в избранное пользователя или убирает его из избранного.

    :param user: Пользователь, который добавляет или убирает объект из избранного.
    :param obj: Объект, который добавляется или удаляется из избранного.
    :return: Статус действия: 'added to favorites' или 'removed from favorites'.
    """
    favorite_content_type = ContentType.objects.get_for_model(obj)
    favorite_obj, created = Favorite.objects.get_or_create(user=user, content_type=favorite_content_type, object_id=obj.id)

    if not created:
        favorite_obj.delete()
        return 'removed from favorites'
    return 'added to favorites'


def get_favorites_for_model(user, model):
    """
    Получает все объекты определенной модели, добавленные пользователем в избранное.

    :param user: Пользователь, для которого выполняется поиск.
    :param model: Модель объектов для поиска.
    :return: Список объектов модели, добавленных пользователем в избранное.
    """
    model_content_type = ContentType.objects.get_for_model(model)
    return model.objects.filter(favorites__user=user, favorites__content_type=model_content_type)


def give_comment(obj, user, comment, model):
    """
    Пользователь добавляет комментарий к объекту.

    :param obj: Объект, который комментируется.
    :param user: Пользователь, который оставляет комментарий.
    :param comment: Текст комментария.
    :param model: Модель комментария.
    :return: Сообщение о статусе добавления комментария.
    """
    comment_obj = model.objects.create(user=user, content_object=obj, comment=comment)
    return 'Comment created'


def reply_to_comment(user, comment_id, reply_text, model):
    """
    Пользователь отвечает на комментарий.

    :param user: Пользователь, который оставляет ответ.
    :param comment_id: ID комментария, к которому оставляется ответ.
    :param reply_text: Текст ответа.
    :param model: Модель комментария.
    :return: Сообщение о статусе добавления ответа.
    """
    parent = model.objects.get(id=comment_id)

    reply_obj, is_created = model.objects.get_or_create(
        user=user,
        content_type=parent.content_type,
        object_id=parent.object_id,
        comment=reply_text,
        parent=parent
    )

    if not is_created:
        reply_obj.comment = reply_text
        reply_obj.save()

    return 'Reply created' if is_created else 'Reply updated'


def delete_specific_comment(comment_id, user, model):
    """
    Удаляет конкретный комментарий пользователя.

    :param comment_id: ID комментария для удаления.
    :param user: Пользователь, который удаляет комментарий.
    :param model: Модель комментария.
    """
    try:
        comment = model.objects.get(id=comment_id, user=user)
        comment.delete()
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist("Comment not found or you do not have permission to delete it.")


def is_commented(obj, user, model):
    """
    Проверяет, оставлял ли пользователь комментарий к объекту.

    :param obj: Объект, для которого проверяется комментарий.
    :param user: Пользователь, для которого выполняется проверка.
    :param model: Модель комментария.
    :return: True, если пользователь оставлял комментарий, иначе False.
    """
    try:
        return model.objects.filter(user=user, content_object=obj).exists()
    except TypeError:
        return False


def edit_comment(comment_id, user, new_text, model):
    """
    Редактирует существующий комментарий пользователя.

    :param comment_id: ID редактируемого комментария.
    :param user: Пользователь, который редактирует комментарий.
    :param new_text: Новый текст комментария.
    :param model: Модель комментария.
    :return: Сообщение о статусе редактирования комментария.
    """
    try:
        comment_obj = model.objects.get(id=comment_id, user=user)
        comment_obj.comment = new_text
        comment_obj.save()
        return 'Comment updated'
    except model.DoesNotExist:
        raise ValueError('Comment not found or user mismatch')

