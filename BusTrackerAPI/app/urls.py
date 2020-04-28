from django.urls import path
from .views import RouteView, getBuses

# Create your views here.
urlpatterns = [
    path('route/', RouteView.as_view()),
    path('route/<int:route_id>/', getBuses.as_view())
]
