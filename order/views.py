# Create your views here.
from rest_framework.decorators import action
from rest_framework.response import Response

from base.view import BaseModelViewset
from market.serializers import MarketSerializer
from order.models import Catalogue, Order
from order.serializers import CatalogueSerializer, OrderSerializer


class OrderViewSet(BaseModelViewset):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        request = self.request
        
        market = getattr(request, 'market', None)
        queryset = super(OrderViewSet, self).get_queryset()
        
        if market:
            queryset = queryset.filter(order__market=market)
        else:
            queryset = queryset.filter(user=request.user)
            
        status = request.GET.get('status', None)
        if status:
            status = str(status).lower()
            return queryset.filter(status=status)

        return queryset

    @action(
        methods=['get'],
        detail=True,
        url_path='rate',
        url_name='rate',
    )
    def rate(self, request, pk=None):
        rate = request.GET.get('rate', None)
        obj = self.get_object()
        if rate:
            obj.rate(rate)
        serializer = self.serializer_class(obj)
        return Response(serializer.data)

    @action(
        methods=['get'],
        detail=True,
        url_path='update',
        url_name='update',
    )
    def update_status(self, request, pk=None):
        status = request.GET.get('status', None)
        obj = self.get_object()
        if status:
            obj.update_status(status)
        serializer = self.serializer_class(obj)
        return Response(serializer.data)


class CatalogueViewSet(BaseModelViewset):
    serializer_class = CatalogueSerializer
    queryset = Catalogue.objects.all()

    def get_queryset(self):
        queryset = super(CatalogueViewSet, self).get_queryset()
        approved = self.request.GET.get('approved', None)
        if approved:
            approved = str(approved).lower()
            if approved == "true" or approved == "1":
                return queryset.filter(approved=True)
            elif approved == "false" or approved == "0":
                return queryset.filter(approved=False)

        return queryset

    @action(
        methods=['get'],
        detail=True,
        url_path='market',
        url_name='market',
    )
    def market(self, request, pk=None):
        serializer = MarketSerializer(self.get_object().market)
        return Response(serializer.data)

    @action(
        methods=['get'],
        detail=True,
        url_path='orders',
        url_name='orders',
    )
    def orders(self, request, pk=None):
        status = request.GET.get('status')
        serializer = OrderSerializer(self.get_object().get_orders(status), many=True)
        return Response(serializer.data)

    @action(
        methods=['get'],
        detail=True,
        url_path='approve',
        url_name='approve',
    )
    def approve(self, request, pk=None):
        serializer = CatalogueSerializer(self.get_object().approve())
        return Response(serializer.data)
