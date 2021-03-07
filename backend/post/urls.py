from django.urls import path

from . import views
from . import indicators

urlpatterns = [
    path('', views.ListPost.as_view()),
    path('<int:pk>/', views.DetailPost.as_view()),
    path('requestUsdkrw/', indicators.usdkrw.as_view())
]