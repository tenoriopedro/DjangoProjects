from django.urls import path
from blog.views import PostDetailView, PageDetailView, CreatedByListView, CategoryListView, TagsListView, SearchListView, PostListView

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post'),
    path('page/<slug:slug>/', PageDetailView.as_view(), name='page'),
    path(
        'created_by/<int:author_pk>/',
        CreatedByListView.as_view(),
        name='created_by',
    ),
    path('category/<slug:slug>/',
         CategoryListView.as_view(),
         name='category'),
    path('tags/<slug:slug>/', TagsListView.as_view(), name='tags'),
    path('search/', SearchListView.as_view(), name='search'),
]
