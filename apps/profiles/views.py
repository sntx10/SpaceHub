
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, Http404
from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from account.serializers import UsersSerializer
from .permissions import IsAdminPermission, IsAuthorPermission
from apps.profiles.models import UserProfile
from apps.profiles.serializers import ProfileSerializer, UserSubscriptionSerializer
from rest_framework.response import Response

User = get_user_model()

# class ProfileViewSet(viewsets.ModelViewSet):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer
#
#     @action(detail=True, methods=["POST"], url_path='add-languages')
#     def add_languages(self, request, pk=None):
#         profile = self.get_object()
#
#         if profile.user != request.user:
#             return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)
#
#         new_languages = request.data.get("other_languages", [])
#
#         for lang_data in new_languages:
#             language = Language.objects.get(name=lang_data['language_name'])
#             level = lang_data['level']

        #     proficiency, created = LanguageProficiency.objects.get_or_create(
        #         profile=profile,
        #         language=language,
        #         defaults={'level': level}
        #     )
        #
        #     if not created and proficiency.level != level:
        #         proficiency.level = level
        #         proficiency.save()
        #
        # return Response({"detail": "Languages added/updated successfully"}, status=status.HTTP_200_OK)


class RomProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, IsAdminPermission]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthorPermission]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get(self, request, user_id, *args, **kwargs):
        user = User.objects.get(id=user_id)
        serializer = UsersSerializer(user)
        return Response(serializer.data)



class ToggleSubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id, *args, **kwargs):
        if request.user.id == user_id:
            return Response({"error": "Cannot subscribe to or unsubscribe from self."}, status=status.HTTP_400_BAD_REQUEST)

        target_user = get_object_or_404(User, id=user_id)
        target_profile = get_object_or_404(UserProfile, user=target_user)

        user_profile = get_object_or_404(UserProfile, user=request.user)

        if target_profile in user_profile.subscriptions.all():
            user_profile.subscriptions.remove(target_profile)
            return Response({"message": "Unsubscribed successfully."}, status=status.HTTP_200_OK)
        else:
            user_profile.subscriptions.add(target_profile)
            return Response({"message": "Subscribed successfully."}, status=status.HTTP_200_OK)


class SubscriptionsListView(ListAPIView):
    serializer_class = UserSubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.userprofile.subscriptions.all()


class FollowersListView(ListAPIView):
    serializer_class = UserSubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.userprofile.followers.all()

