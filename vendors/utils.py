from datetime import datetime, timedelta
from .models import Vendor, PurchaseOrder
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
from .models import PurchaseOrder
def calculate_on_time_delivery_rate(vendor):
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    on_time_delivered_pos = completed_pos.filter(delivery_date__lte=datetime.now())
    return on_time_delivered_pos.count() / completed_pos.count()
def calculate_quality_rating_average(vendor):
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed').exclude(quality_rating=None)
    total_ratings = completed_pos.aggregate(total_ratings=Sum('quality_rating'))
    num_ratings = completed_pos.count()
    if num_ratings > 0:
        return total_ratings['total_ratings'] / num_ratings
    else:
        return 0  # No ratings yet

def calculate_average_response_time(vendor):
    acknowledged_pos = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
    response_times = [po.acknowledgment_date - po.issue_date for po in acknowledged_pos]
    if response_times:
        return sum(response_times, timedelta()) / len(response_times)
    else:
        return timedelta()  # No acknowledged POs yet
def calculate_fulfillment_rate(vendor):
    issued_pos = PurchaseOrder.objects.filter(vendor=vendor)
    completed_pos = issued_pos.filter(status='completed')
    successful_fulfillments = completed_pos.exclude(issue__issue_status='issue').count()
    return successful_fulfillments / issued_pos.count()
