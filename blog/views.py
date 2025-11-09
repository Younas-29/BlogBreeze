from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Prefetch, Q
from django.urls import reverse_lazy
from accounts.mixins import RoleRequiredMixin, AuthorRequiredMixin
from .models import Post, Comment, Category, Tag
from .forms import CommentForm, PostForm


class PostListView(ListView):
    """
    Display paginated list of published posts on the home page.
    Optimized with select_related and prefetch_related for performance.
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        """
        Return optimized queryset of posts.
        Show only published posts for non-admin users.
        """
        queryset = Post.objects.select_related('author', 'category').prefetch_related('tags')
        
        # Filter to show only published posts for non-admin users
        user = self.request.user
        if not user.is_authenticated or not hasattr(user, 'profile') or user.profile.role != 'admin':
            queryset = queryset.filter(status='published')
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        """
        Add hero_post and remaining_posts to context.
        The first post is displayed as hero, remaining posts in grid.
        """
        context = super().get_context_data(**kwargs)
        posts = context['posts']
        
        if posts:
            context['hero_post'] = posts[0]
            context['remaining_posts'] = posts[1:]
        else:
            context['hero_post'] = None
            context['remaining_posts'] = []
        
        return context


class PostDetailView(DetailView):
    """
    Display individual post with comments and comment form.
    Optimized query to fetch related data efficiently.
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        """
        Return optimized queryset with related data.
        """
        return Post.objects.select_related('author', 'category').prefetch_related(
            'tags',
            Prefetch('comments', queryset=Comment.objects.select_related('user').order_by('created_at'))
        )
    
    def get_context_data(self, **kwargs):
        """
        Add comment form, comments, read time, and related posts to context.
        """
        context = super().get_context_data(**kwargs)
        post = self.object
        
        # Add comment form and comments
        context['comment_form'] = CommentForm()
        context['comments'] = post.comments.all()
        
        # Calculate read time (assuming 200 words per minute)
        word_count = len(post.content.split())
        context['read_time'] = max(1, round(word_count / 200))
        
        # Get related posts (same category, exclude current, limit 3)
        context['related_posts'] = Post.objects.filter(
            category=post.category,
            status='published'
        ).exclude(id=post.id).select_related('author', 'category').prefetch_related('tags')[:3]
        
        return context
    
    def post(self, request, *args, **kwargs):
        """
        Handle comment creation via POST request.
        """
        # Check if user is authenticated
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to comment.')
            return redirect('accounts:login')
        
        # Get the post object
        self.object = self.get_object()
        
        # Create comment form with POST data
        form = CommentForm(request.POST)
        
        if form.is_valid():
            # Create comment but don't save yet
            comment = form.save(commit=False)
            comment.post = self.object
            comment.user = request.user
            comment.save()
            
            messages.success(request, 'Your comment has been posted successfully!')
            return redirect('blog:post_detail', slug=self.object.slug)
        else:
            # Form is invalid, re-render with errors
            messages.error(request, 'There was an error with your comment. Please check and try again.')
            context = self.get_context_data()
            context['comment_form'] = form
            return self.render_to_response(context)


def home(request):
    """
    Temporary home view for testing authentication.
    Will be replaced with PostListView in later tasks.
    """
    return render(request, 'blog/home.html')


class PostCreateView(RoleRequiredMixin, CreateView):
    """
    View for creating new blog posts.
    Restricted to Author and Admin roles.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    required_roles = ['author', 'admin']
    
    def form_valid(self, form):
        """
        Auto-assign current user as author before saving.
        """
        # Set the author to the current user
        form.instance.author = self.request.user
        
        # Save the post
        response = super().form_valid(form)
        
        # Add success message
        messages.success(
            self.request,
            f'Post "{self.object.title}" has been created successfully!'
        )
        
        return response
    
    def get_success_url(self):
        """
        Redirect to the post detail page after successful creation.
        """
        return reverse_lazy('blog:post_detail', kwargs={'slug': self.object.slug})


class PostUpdateView(AuthorRequiredMixin, UpdateView):
    """
    View for editing existing blog posts.
    Restricted to post author or admin.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    context_object_name = 'post'
    
    def form_valid(self, form):
        """
        Save the updated post and add success message.
        The updated_at timestamp is automatically updated by the model.
        """
        response = super().form_valid(form)
        
        # Add success message
        messages.success(
            self.request,
            f'Post "{self.object.title}" has been updated successfully!'
        )
        
        return response
    
    def get_success_url(self):
        """
        Redirect to the post detail page after successful update.
        """
        return reverse_lazy('blog:post_detail', kwargs={'slug': self.object.slug})


class PostDeleteView(AuthorRequiredMixin, DeleteView):
    """
    View for deleting blog posts.
    Restricted to post author or admin.
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('blog:post_list')
    
    def delete(self, request, *args, **kwargs):
        """
        Delete the post and add success message.
        """
        post = self.get_object()
        post_title = post.title
        
        # Delete the post
        response = super().delete(request, *args, **kwargs)
        
        # Add success message
        messages.success(
            request,
            f'Post "{post_title}" has been deleted successfully!'
        )
        
        return response


class CategoryPostListView(ListView):
    """
    Display paginated list of posts filtered by category.
    Shows category name in page title and filters by category slug.
    """
    model = Post
    template_name = 'blog/category_posts.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        """
        Return optimized queryset of posts filtered by category.
        Show only published posts for non-admin users.
        """
        # Get the category by slug
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        
        # Filter posts by category
        queryset = Post.objects.filter(category=self.category).select_related(
            'author', 'category'
        ).prefetch_related('tags')
        
        # Filter to show only published posts for non-admin users
        user = self.request.user
        if not user.is_authenticated or not hasattr(user, 'profile') or user.profile.role != 'admin':
            queryset = queryset.filter(status='published')
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        """
        Add category to context for display in template.
        """
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class TagPostListView(ListView):
    """
    Display paginated list of posts filtered by tag.
    Shows tag name in page title and filters by tag slug.
    """
    model = Post
    template_name = 'blog/tag_posts.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        """
        Return optimized queryset of posts filtered by tag.
        Show only published posts for non-admin users.
        """
        # Get the tag by slug
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        
        # Filter posts by tag
        queryset = Post.objects.filter(tags=self.tag).select_related(
            'author', 'category'
        ).prefetch_related('tags')
        
        # Filter to show only published posts for non-admin users
        user = self.request.user
        if not user.is_authenticated or not hasattr(user, 'profile') or user.profile.role != 'admin':
            queryset = queryset.filter(status='published')
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        """
        Add tag to context for display in template.
        """
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


class CategoryListView(ListView):
    """
    Display list of all categories with post counts.
    """
    model = Category
    template_name = 'blog/category_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        """
        Return all categories ordered by name.
        """
        return Category.objects.all().order_by('name')


class SearchView(ListView):
    """
    Display paginated search results for posts.
    Searches in post title and content using Q objects.
    Shows only published posts for non-admin users.
    """
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        """
        Return optimized queryset of posts filtered by search query.
        Search in title and content fields using Q objects.
        Show only published posts for non-admin users.
        """
        # Get the search query from GET parameters
        self.query = self.request.GET.get('q', '').strip()
        
        # Start with base queryset
        queryset = Post.objects.select_related('author', 'category').prefetch_related('tags')
        
        # Apply search filter if query exists
        if self.query:
            # Use Q objects to search in title or content
            queryset = queryset.filter(
                Q(title__icontains=self.query) | Q(content__icontains=self.query)
            )
        
        # Filter to show only published posts for non-admin users
        user = self.request.user
        if not user.is_authenticated or not hasattr(user, 'profile') or user.profile.role != 'admin':
            queryset = queryset.filter(status='published')
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        """
        Add search query to context for display and pagination.
        """
        context = super().get_context_data(**kwargs)
        context['query'] = self.query
        context['search_performed'] = bool(self.query)
        return context
