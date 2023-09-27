from django.urls import path
from . import views

# from .views import BlogPostListCreateView, BlogPostRetrieveUpdateDestroyView,UserProfileRetrieveUpdateView,CommentListCreateView, CommentRetrieveUpdateDestroyView


urlpatterns = [
    path('viewblog/' , views.PublicView.as_view()),
    path('blog/', views.BlogView.as_view()),
    path('profiles/<uuid:pk>/', views.ProfileView.as_view(), name='profile-detail'),
    
]
