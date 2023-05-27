import api.views as vs
from django.urls import include, path
from rest_framework import routers

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'categories', vs.CategoryViewSet)
router.register(r'genres', vs.GenreViewSet)
router.register(r'titles', vs.TitleViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    vs.ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    vs.CommentViewSet, basename='comments'
)

urlpatterns = [
    path('', include(router.urls)),
]
