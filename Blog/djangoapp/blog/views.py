from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.http import Http404
from django.db.models import Q
from blog.models import Post, Page

PER_PAGE = 9


class PostListView(ListView):
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'page_title': 'Home - ',
        })

        return context
    

class CreatedByListView(PostListView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._temp_context = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self._temp_context['user']
        user_full_name = user.username
        
        if user.first_name:
            user_full_name = f'{user.first_name} {user.last_name}'

        page_title = f'Posts de {user_full_name} - '
        context.update({
            'page_title':page_title
        })

        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(created_by__pk=self._temp_context['user'].pk)
        return queryset
    
    def get(self, request, *args, **kwargs):
        author_pk = self.kwargs.get('author_pk')
        user = User.objects.filter(pk=author_pk).first()

        if user is None:
            raise Http404
        
        self._temp_context.update({
            'author_pk': author_pk,
            'user': user,
        })

        return super().get(request, *args, **kwargs)


class CategoryListView(PostListView):
    allow_empty = False

    def get_queryset(self):
        return super().get_queryset().filter(
            category__slug=self.kwargs.get('slug')
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_title = (
            f'{self.object_list[0].category.name} - Categoria - '
        )

        context.update({
            'page_title': page_title,
        })

        return context


class SearchListView(PostListView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._search_value = ''

    def setup(self, request, *args, **kwargs):
        self._search_value = request.GET.get('search', '').strip()
        return super().setup(request, *args, **kwargs)
    
    def get_queryset(self):
        search_value = self._search_value
        return super().get_queryset().filter(
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value)
        )[:PER_PAGE]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_value = self._search_value


        context.update({
            'page_title': f'{search_value[:30]} - Search - ',
            'search_value': search_value,
        })
        return context

    def get(self, request, *args, **kwargs):
        if self._search_value == '':
            return redirect('blog:index')
        
        return super().get(request, *args, **kwargs)


class TagsListView(PostListView):
    allow_empty = False

    def get_queryset(self):
        qs = super().get_queryset().filter(
            tags__slug=self.kwargs.get('slug')
        )

        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')

        page_title = None
        for tag in self.object_list[0].tags.all():
            if tag.slug == slug:
                
                page_title = (
                    f'{tag.name} - Tag - '
                )

        context.update({
            'page_title': page_title,
        })

        return context


class PageDetailView(DetailView):
    model = Page
    template_name = 'blog/pages/page.html'
    slug_field = 'slug'
    context_object_name = 'page'

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)

        page = self.get_object()
        page_title = f'{page.title} - Página - '
        context.update({
            'page_title': page_title,
        })
        return context

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/pages/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        page_title = f'{post.title} - Post - '

        context.update({
            'page_title': page_title,
        })
        return context
    
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)



def post(request, slug):
    post_obj = (
        Post.objects.get_published().filter(slug=slug).first()
    )

    if post_obj is None:
        raise Http404()
    
    page_title = f'{post_obj.title}- Post - '

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post_obj,
            'page_title': page_title,
        }
    )
