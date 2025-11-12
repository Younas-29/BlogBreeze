from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class Category(models.Model):
    """Category model for organizing blog posts into broad topics"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    """Tag model for keyword-based organization of posts"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    """Blog post model with rich content and metadata"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.CharField(
        max_length=300,
        blank=True,
        help_text="Short description of the post (max 300 characters)"
    )
    content = RichTextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    featured_image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Debug logging for image upload
        if self.featured_image:
            logger.info(f"=" * 80)
            logger.info(f"POST SAVE - Image Upload Debug Info")
            logger.info(f"=" * 80)
            logger.info(f"Post Title: {self.title}")
            logger.info(f"Image Field: {self.featured_image}")
            logger.info(f"Image Name: {self.featured_image.name}")
            logger.info(f"DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
            logger.info(f"MEDIA_URL: {settings.MEDIA_URL}")
            
            # Check if using Azure storage
            if hasattr(settings, 'AZURE_ACCOUNT_NAME'):
                logger.info(f"Azure Storage Account: {settings.AZURE_ACCOUNT_NAME}")
                logger.info(f"Azure Container: {getattr(settings, 'AZURE_CONTAINER', 'NOT SET')}")
                logger.info(f"Expected Azure URL: https://{settings.AZURE_ACCOUNT_NAME}.blob.core.windows.net/{getattr(settings, 'AZURE_CONTAINER', 'media')}/{self.featured_image.name}")
            else:
                logger.info(f"Using Local Storage: {settings.MEDIA_ROOT}")
            
            # Log the storage backend being used
            if hasattr(self.featured_image, 'storage'):
                logger.info(f"Storage Backend: {type(self.featured_image.storage).__name__}")
                logger.info(f"Storage Backend Module: {type(self.featured_image.storage).__module__}")
            
            logger.info(f"=" * 80)
        
        super().save(*args, **kwargs)
        
        # Log after save to confirm URL
        if self.featured_image:
            logger.info(f"POST SAVE COMPLETE - Image URL: {self.featured_image.url}")
            logger.info(f"=" * 80)


class Comment(models.Model):
    """Comment model for user-generated content on posts"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'
