from django.urls import path
import library.views as views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', views.index),
    path('upload/', views.upload),
    path('delete/', views.delete),
    path('search/', views.search),
    path('accounts/register/', views.register),
    path('accounts/login/', views.login),
    path('accounts/logout/', views.logout),
    path('api/getBooks/', views.BookView.as_view())

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
