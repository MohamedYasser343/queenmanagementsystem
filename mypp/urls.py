from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NameViewSet, EntryViewSet

router = DefaultRouter()
router.register(r'names', NameViewSet)
router.register(r'entries', EntryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
