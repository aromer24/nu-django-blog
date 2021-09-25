from django.urls import path
from blogapp import views


app_name = 'blogapp'

urlpatterns = [
    path('', views.main_view, name='index'),
    path('contact/', views.contact_view, name='contact'),
    path('create/', views.create_post, name='create'),
    path('post/<int:id>/', views.post, name='post'),
    path('tag-list', views.TagListView.as_view(), name='tag_list'),
    path('tag-detail/<int:pk>/', views.TagDetailView.as_view(), name='tag_detail'),
    path('tag-create/', views.TagCreateView.as_view(), name='tag_create'),
    path('tag-update/<int:pk>/', views.TagUpdataView.as_view(), name='tag_update'),
    path('tag-delete/<int:pk>/', views.TagDeleteView.as_view(), name='tag_delete'),
]
