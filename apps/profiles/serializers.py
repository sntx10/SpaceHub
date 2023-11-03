from rest_framework import serializers
from apps.profiles.models import UserProfile
from apps.education_history.serializers import EducationHistorySerializer, LanguageSerializer
from django.contrib.auth import get_user_model


User = get_user_model()


# class LanguageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Language
#         fields = "__all__"
#
#
# class LanguageProficiencySerializer(serializers.ModelSerializer):
#     language_name = serializers.ReadOnlyField(source='language.name')
#     level = serializers.ChoiceField(choices=LanguageProficiency.LEVEL_CHOICES)

#     class Meta:
#         model = LanguageProficiency
#         fields = ('language_name', 'level')
#
#
# class ProfileSerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(source="user.email")
#     native_language = serializers.SlugRelatedField(slug_field="name", queryset=Language.objects.all())
#     other_languages = LanguageProficiencySerializer(source="proficiencies", many=True)

    # class Meta:
    #     model = Profile
    #     fields = ('user', 'first_name', 'last_name', 'professions', 'native_language',
    #               'other_languages', 'country', 'arial', 'profile_image', 'created_at', 'updated_at')
    #
    # def validate(self, data):
    #     current_user = self.context.get("request").user
    #     if self.instance and self.instance.user != current_user:
    #         raise serializers.ValidationError("You cannot modify another user's profile")
    #     return data
    #
    # def create(self, validated_data):
    #     other_languages_data = validated_data.pop('other_languages', [])
    #
    #     profile, created = Profile.objects.update_or_create(
        #     user=self.context['request'].user,
        #     defaults=validated_data
        # )
        #
        # existing_languages = set(profile.proficiencies.values_list('language__name', flat=True))
        # new_languages = set([lang_data['language_name'] for lang_data in other_languages_data])
        #
        # languages_to_add = new_languages - existing_languages
        # languages_to_remove = existing_languages - new_languages
        #
        # for lang_data in other_languages_data:
        #     if lang_data['language_name'] in languages_to_add:
        #         language = Language.objects.get(name=lang_data['language_name'])
        #         LanguageProficiency.objects.create(profile=profile, language=language, level=lang_data['level'])
        #
        # for lang_name in languages_to_remove:
        #     language = Language.objects.get(name=lang_name)
        #     profile.proficiencies.filter(language=language).delete()
        #
        # return profile


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    # followers_count = serializers.SerializerMethodField()
    # followers_list = serializers.SerializerMethodField()
    # following = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    subscriptions_count = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        # fields = ('id', 'user', 'username', 'first_name', 'last_name', 'professions', 'country', 'arial', 'profile_image',
        #           'profile_background', 'followers_count', 'subscriptions_count', 'created_at', 'updated_at')
        fields = '__all__'

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_subscriptions_count(self, obj):
        return obj.subscriptions.count()

    def validate(self, data):
        current_user = self.context.get("request").user
        if self.instance and self.instance.user != current_user:
            raise serializers.ValidationError("You cannot modify another user's profile")
        return data

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['languages'] = LanguageSerializer(instance.languages.all(), many=True).data
        rep['education history'] = EducationHistorySerializer(instance.educ_history.all(), many=True).data
        return rep

    def create(self, validated_data):
        user = self.context['request'].user
        return self.Meta.model.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        User.objects.update(is_profile_complete=True)
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.professions = validated_data.get('professions', instance.professions)
        instance.profile_image = validated_data.get('profile_image', instance.profile_image)
        instance.profile_background = validated_data.get('profile_background', instance.profile_background)
        instance.country = validated_data.get('country', instance.country)
        instance.arial = validated_data.get('arial', instance.arial)
        instance.save()
        return instance


class UserSubscriptionSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('username', 'profile_image')

    def get_username(self, obj):
        return f"{obj.first_name} {obj.last_name}"
