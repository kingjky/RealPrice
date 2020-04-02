from api import models, serializers
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from .models import Faq
from .models import Qna

class SmallPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50


class StoreViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StoreSerializer
    pagination_class = SmallPagination

    def get_queryset(self):
        name = self.request.query_params.get("name", "")
        queryset = (
            models.Store.objects.all().filter(store_name__contains=name).order_by("id")
        )
        return queryset


class FaqViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.FaqSerializer
    pagination_class = SmallPagination
    queryset = Faq.objects.all()
    
    
class QnaViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.QnaSerializer
    pagination_class = SmallPagination
    queryset = Qna.objects.all()
