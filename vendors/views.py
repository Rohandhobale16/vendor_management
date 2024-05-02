from datetime import timezone
from urllib import response
from django.shortcuts import render
from rest_framework import generics
from .models import Vendor, PurchaseOrder
from .serializers import PurchaseOrderSerializer, VendorSerializer
from .serializers import PurchaseOrderSerializer

from django.db.models import Avg
from rest_framework.response import Response
# Create your views here.
def home(request):
    context={}
    return render(request, "index.html",context)
class VendorListCreate(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderListCreate(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
class VendorPerformance(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = {
            'on_time_delivery_rate': instance.on_time_delivery_rate,
            'quality_rating': instance.purchaseorder_set.aggregate(Avg('quality_rating'))['quality_rating__avg'],
            'response_time': instance.response_time,
            'fulfilment_rate': instance.fulfilment_rate,
        }
        return Response(data)
    
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Vendor
from .utils import calculate_on_time_delivery_rate, calculate_quality_rating_average, calculate_average_response_time, calculate_fulfillment_rate

def vendor_performance_metrics(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    
    on_time_delivery_rate = calculate_on_time_delivery_rate(vendor)
    quality_rating_average = calculate_quality_rating_average(vendor)
    average_response_time = calculate_average_response_time(vendor)
    fulfillment_rate = calculate_fulfillment_rate(vendor)
    
    data = {
        'on_time_delivery_rate': on_time_delivery_rate,
        'quality_rating_average': quality_rating_average,
        'average_response_time': average_response_time,
        'fulfillment_rate': fulfillment_rate
    }
    
    return JsonResponse(data)
# views.py

from rest_framework import generics
from rest_framework.response import Response
from .models import Vendor
from .serializers import VendorPerformanceSerializer

class VendorPerformanceAPIView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorPerformanceSerializer
    lookup_field = 'vendor_id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
# views.py

from rest_framework import generics
from rest_framework.response import Response
from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer

class AcknowledgePurchaseOrderAPIView(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_field = 'po_id'

    def perform_update(self, serializer):
        instance = serializer.save(acknowledgment_date=timezone.now())
        # Trigger recalculation of average_response_time here if needed

def vendor_detail(request, vendor_id):
    vendor = Vendor.objects.get(pk=vendor_id)
    on_time_delivery_rate = vendor.calculate_on_time_delivery_rate()
    quality_rating_average = vendor.calculate_quality_rating_average()
    average_response_time = vendor.calculate_average_response_time()
    fulfilment_rate = vendor.calculate_fulfilment_rate()
    
    return render(request, 'index.html', {
        'vendor': vendor,
        'on_time_delivery_rate': on_time_delivery_rate,
        'quality_rating_average': quality_rating_average,
        'average_response_time': average_response_time,
        'fulfilment_rate': fulfilment_rate,
    })