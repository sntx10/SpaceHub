from rest_framework.viewsets import ModelViewSet
from .models import EducationHistory, Language
from .serializers import EducationHistorySerializer, LanguageSerializer

# Create your views here.


class EducationHistoryViewSet(ModelViewSet):
    queryset = EducationHistory.objects.all()
    serializer_class = EducationHistorySerializer


class LanguageViewSet(ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer