from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from base.view import BaseModelViewset
from order.serializers import CatalogueSerializer
from .serializers import MarketSerializer, CategoriesSerializer
from .models import Market, Category


class MarketViewSet(BaseModelViewset):
    serializer_class = MarketSerializer
    queryset = Market.valid()

    @action(
        methods=['get'],
        detail=True,
        url_path='catalogues',
        url_name='market_catalogues',
    )
    def catalogues(self, request, pk=None):
        serializer = CatalogueSerializer(self.get_object().catalogues, many=True)
        return Response(serializer.data)
    
class CategoryViewset(viewsets.ModelViewSet):
    serializer_class = CategoriesSerializer
    queryset = Category.objects.all()
