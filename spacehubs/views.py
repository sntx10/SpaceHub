from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework import generics
from rest_framework.response import Response
from feedback.mixins import LikeMixin, FavoriteMixin, CommentMixin

from feedback.models import Like, Comment
from spacehubs import services
from spacehubs.models import News, Project, Blog, Post, PodCast
from spacehubs.serializers import TheNewsSerializer, BlogSerializer,\
    PodCastSerializer, ProjectSerializer, PostSerializer

from surprise import Dataset, Reader
from surprise.model_selection import train_test_split
from surprise import KNNBasic
import random


# Create your views here


class ProjectViewSet(LikeMixin, FavoriteMixin, CommentMixin, viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    like_model = Like
    comment_model = Comment
    target_model = Project

    def get_recommendations(self, user):
        # Создайте объект Reader для настройки данных
        reader = Reader(rating_scale=(0, 1))

        # Создайте Dataset из ваших данных
        data = Dataset.load_from_df(Project[['user', 'category', 'likes', 'favorites']], reader)

        # Разделите данные на обучающий и тестовый наборы
        trainset, _ = train_test_split(data, test_size=0.2)

        # Создайте и обучите модель для рекомендаций (например, KNNBasic)
        algo = KNNBasic()
        algo.fit(trainset)

        # Получите идентификатор пользователя (user_id), для которого вы хотите получить рекомендации
        user_id = user.id

        # Получите список контента, который пользователь еще не просматривал
        user_ratings = Project[Project['user'] == user_id]
        user_content_ids = user_ratings['category'].unique()

        all_content_ids = Project.objects.values_list('id', flat=True)
        unwatched_content_ids = set(all_content_ids) - set(user_content_ids)

        # Получите рекомендации для пользователя
        predictions = [algo.predict(user_id, content_id) for content_id in unwatched_content_ids]
        top_n = sorted(predictions, key=lambda x: x.est, reverse=True)[:10]

        recommended_content_ids = [pred.iid for pred in top_n]

        # Получите рекомендации в виде объектов контента
        recommended_content = Project.objects.filter(id__in=recommended_content_ids)

        return recommended_content

    def list(self, request, **kwargs):
        if request.user.is_authenticated:
            queryset = services.get_recommended_project(request.user)
        else:
            queryset = Project.objects.all()

        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user.is_authenticated:
            services.add_project_view(request.user, instance)

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status.HTTP_200_OK)


class BlogViewSet(LikeMixin, FavoriteMixin, CommentMixin, viewsets.ModelViewSet):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    like_model = Like
    comment_model = Comment
    target_model = Blog

    def list(self, request, *args, **kwargs):
        queryset = services.get_recommended_blog(request.user)
        serializer = BlogSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user.is_authenticated:
            services.add_blog_view(request.user, instance)

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status.HTTP_200_OK)


class PostViewSet(LikeMixin, FavoriteMixin, CommentMixin, viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    like_model = Like
    comment_model = Comment
    target_model = Post

    def list(self, request, *args, **kwargs):
        queryset = services.get_recommended_post(request.user)
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user.is_authenticated:
            services.add_post_view(request.user, instance)

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status.HTTP_200_OK)


class PodCastViewSet(LikeMixin, FavoriteMixin, CommentMixin, viewsets.ModelViewSet):
    serializer_class = PodCastSerializer
    queryset = PodCast.objects.all()
    like_model = Like
    comment_model = Comment
    target_model = PodCast

    def list(self, request, *args, **kwargs):
        queryset = services.get_recommended_podcast(request.user)
        serializer = PodCastSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user.is_authenticated:
            services.add_podcast_view(request.user, instance)

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status.HTTP_200_OK)


class NewsViewSet(LikeMixin, FavoriteMixin, CommentMixin, viewsets.ModelViewSet):
    serializer_class = TheNewsSerializer
    queryset = News.objects.all()
    like_model = Like
    comment_model = Comment
    target_model = News

    def list(self, request, *args, **kwargs):
        news = services.get_latest_news(request.user)
        serializer = TheNewsSerializer(news, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user.is_authenticated:
            services.add_news_view(request.user, instance)

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status.HTTP_200_OK)

