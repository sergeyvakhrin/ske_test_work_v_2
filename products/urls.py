from django.urls import path

from products.apps import ProductsConfig
from products.views import home, ProductCreateAPIView, ProductListAPIView, ProductRetrieveAPIView, ProductUpdateAPIView, \
    ProductDeleteAPIView, WarehouseCreateAPIView, WarehouseListAPIView, WarehouseRetrieveAPIView, \
    WarehouseDeleteAPIView, ProductCreateView, ProductListView, ProductDetailView, ProductUpdateView

app_name = ProductsConfig.name

urlpatterns = [
    path("api/product/create/", ProductCreateAPIView.as_view(), name="api-product-create"),
    path("api/product/list/", ProductListAPIView.as_view(), name="api-product-list"),
    path("api/product/<int:pk>/", ProductRetrieveAPIView.as_view(), name="api-product-get"),
    path("api/product/update/<int:pk>/", ProductUpdateAPIView.as_view(), name="api-product-update"),
    path("api/product/delete/<int:pk>/", ProductDeleteAPIView.as_view(), name="api-product-delete"),

    path("api/warehouse/create/", WarehouseCreateAPIView.as_view(), name="api-warehouse-create"),
    path("api/warehouse/list/", WarehouseListAPIView.as_view(), name="api-warehouse-list"),
    path("api/warehouse/<int:pk>/", WarehouseRetrieveAPIView.as_view(), name="api-warehouse-get"),
    path("api/warehouse/delete/<int:pk>/", WarehouseDeleteAPIView.as_view(), name="api-warehouse-delete"),

    path('', home, name='home'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/list/', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),

]
