from django.urls import path

from . import views

urlpatterns = [
    path("<int:id>", views.index, name="index"),
    path("", views.home, name="home"),
    path("create", views.create, name="create"),
    path("product_list", views.product_list, name="product_list"),
    path("order_list", views.order_list, name="order_list"),
    path("entegrasyon", views.entegrasyon, name="entegrasyon"),
    path("entegrasyon/trendyol_integration", views.trendyol_integration, name="trendyol_integration"),
    path("woocommerce_integration", views.woocommerce_integration, name="woocommerce_integration"),
    path("parasut_integration", views.parasut_integration, name="parasut_integration"),
    path("order/<int:order_id>", views.order_view, name="order_view"),
    path("product/<int:id>/<int:variation_id>", views.product_view, name="product_view"),
    path("edit-product/<int:id>/<int:variation_id>", views.edit_product, name="edit-product"),
]