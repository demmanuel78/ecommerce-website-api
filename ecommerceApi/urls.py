from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("user", views.UserView, basename="user")
router.register("category", views.CategoryView, basename="category")
router.register("product", views.ProductView, basename="product")
router.register("cart", views.CartView, basename="cart")
router.register("cartdetail", views.CartdetailView, basename="cartdetail")
router.register("payment", views.PaymentView, basename="payment")
router.register("deliverypoint", views.DeliverypointView, basename="deliverypoint")

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]


