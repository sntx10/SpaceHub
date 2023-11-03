from .models import EducationHistory, Language
from rest_framework.serializers import ModelSerializer, ReadOnlyField, ValidationError
from django.contrib.auth import get_user_model


User = get_user_model()


class EducationHistorySerializer(ModelSerializer):
    user = ReadOnlyField(source='user.email')
    profile = ReadOnlyField(source='userprofile.email')

    class Meta:
        model = EducationHistory
        fields = "__all__"

    def create(self, validated_data):
        user = self.context['request'].user
        profile = self.context.get('request').user.userprofile
        return self.Meta.model.objects.create(user=user, profile=profile, **validated_data)


class LanguageSerializer(ModelSerializer):
    user = ReadOnlyField(source='user.email')
    profile = ReadOnlyField(source='userprofile.email')

    class Meta:
        model = Language
        fields = "__all__"

    def create(self, validated_data):
        user = self.context['request'].user
        profile = self.context.get('request').user.userprofile
        return self.Meta.model.objects.create(user=user, profile=profile, **validated_data)