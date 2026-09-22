from django.urls import path

from . import views


app_name = "catalog"


urlpatterns = [

    path(
        "",
        views.home,
        name="home",
    ),

    path(
        "shop/",
        views.product_list,
        name="product_list",
    ),

    path(
        "category/<slug:slug>/",
        views.category_detail,
        name="category_detail",
    ),

    path(
        "product/<slug:slug>/",
        views.product_detail,
        name="product_detail",
    ),

    path(
        "product/<int:pk>/quick-view/",
        views.product_quick_view,
        name="product_quick_view",
    ),
]