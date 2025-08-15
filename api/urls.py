from django.urls import include, path
from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'advertisements', views.AdvertisementViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('postbycategory/<int:category_id>/', views.PostbyCategoryViewSet.as_view({'get': 'list'}), name="postbycategory-api"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
