from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token 
from rest_framework_simplejwt.views import TokenBlacklistView,TokenRefreshView,TokenObtainPairView
urlpatterns=[
    path("categories",views.CategoriesView.as_view()),
    path("menu-items",views.MenuItemView.as_view()),
    path("menu-items/<int:pk>",views.SingleMenuItemView.as_view()),
    # path("groups/manager/users",views.manager_users),
    # path("groups/manager/users/<int:pk>",views.remove_single_manager),
    # path("groups/delivery_crew/users",views.delivery_crew_users),
    # path("groups/delivery_crew/users/<int:pk>",views.remove_single_delivery_crew),
    path("orders",views.OrderView.as_view()),
    path("cart/menu-items",views.CartView.as_view()),
    path("api-token-auth",obtain_auth_token),
     path("orders/<int:pk>",views.SingleOrderView.as_view()),
     path("groups/manager/users",views.GroupViewSet.as_view(
         {'get':'list','post':'create','delete':'destroy'}
     )),
     path("groups/delivery-crew/users",views.DeliveryCrewViewSet.as_view(
         {'get':'list','post':'create','delete':'destroy'}
     )),
]