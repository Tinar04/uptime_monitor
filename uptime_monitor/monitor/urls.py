from django.urls import path
from . import views


urlpatterns = [
    path('sites/', views.site_view),
    path('sites/<int:id>/check', views.check_site),
    path('sites/<int:id>/check/history', views.check_history),
    path('sites/<int:id>/', views.site_detail),
    

]