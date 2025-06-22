from django.contrib import admin
from django.urls import path
from app1 import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('create/', views.create_blog_post, name='create_blog'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),  
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),  # logout view
    path('my_blogs/', views.my_blogs, name='my_blogs'),
    path('liked/', views.liked_blogs, name='liked_blogs'),
    path('blog/<int:pk>/like/', views.like_blog, name='like_blog'),
    path('trending/', views.trending_view, name='trending_blogs'),
    path('explore/', views.explore_view, name='explore'),
    path('Explore/', views.explore_view, name='explore'),


]

# media URL setup
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
