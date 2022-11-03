from django.urls import include, path

# настройка роутов для модели
from rest_framework_nested import routers

from ads.views import AdViewSet, CommentViewSet

ad_router = routers.SimpleRouter()
ad_router.register("ads", AdViewSet, basename="ads")

comment_router = routers.NestedSimpleRouter(ad_router, "ads", lookup="ad")
comment_router.register("comments", CommentViewSet, basename="comments")

urlpatterns = [
    path("", include(ad_router.urls)),
    path("", include(comment_router.urls)),
]

