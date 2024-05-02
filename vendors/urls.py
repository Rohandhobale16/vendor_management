from . import views
from django.urls import path


urlpatterns = [
    path("",views.home, name="home"),
    path('api/vendors/', views.VendorListCreate.as_view()),
    path('api/vendors/<int:pk>/', views.VendorRetrieveUpdateDestroy.as_view()),
    path('api/purchase_orders/', views.PurchaseOrderListCreate.as_view()),
    path('api/purchase_orders/<int:pk>/', views.PurchaseOrderRetrieveUpdateDestroy.as_view()),
    path('api/vendors/<int:pk>/performance/', views.VendorPerformance.as_view()),

]
