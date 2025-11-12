from django.contrib import admin
from django.contrib import messages
from .models import Category, Tag, Post, Comment
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'category', 'created_at', 'author']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'category')
        }),
        ('Content', {
            'fields': ('description', 'content', 'featured_image')
        }),
        ('Metadata', {
            'fields': ('status', 'tags')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Override save_model to add debug logging and user feedback"""
        logger.info(f"=" * 80)
        logger.info(f"ADMIN SAVE - Starting Post Save")
        logger.info(f"=" * 80)
        logger.info(f"User: {request.user.username}")
        logger.info(f"Post: {obj.title}")
        logger.info(f"Change: {change}")
        
        if 'featured_image' in form.changed_data:
            logger.info(f"Image field changed!")
            if obj.featured_image:
                logger.info(f"New image: {obj.featured_image.name}")
                
                # Show storage info to admin
                storage_backend = settings.DEFAULT_FILE_STORAGE
                if 'azure' in storage_backend.lower():
                    msg = f"✅ Image will be uploaded to Azure Blob Storage: {settings.AZURE_ACCOUNT_NAME}/{getattr(settings, 'AZURE_CONTAINER', 'media')}"
                    messages.success(request, msg)
                    logger.info(f"Using Azure Storage: {settings.AZURE_ACCOUNT_NAME}")
                else:
                    msg = f"⚠️ Image will be saved locally (not Azure): {storage_backend}"
                    messages.warning(request, msg)
                    logger.warning(f"Using Local Storage: {storage_backend}")
        
        super().save_model(request, obj, form, change)
        
        # Confirm save and show URL
        if obj.featured_image:
            logger.info(f"Image saved successfully!")
            logger.info(f"Image URL: {obj.featured_image.url}")
            messages.info(request, f"📷 Image URL: {obj.featured_image.url}")
        
        logger.info(f"=" * 80)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'content_preview', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['user__username', 'post__title', 'content']
    actions = ['approve_comments', 'unapprove_comments']
    date_hierarchy = 'created_at'
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'{queryset.count()} comments approved.')
    approve_comments.short_description = 'Approve selected comments'
    
    def unapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f'{queryset.count()} comments unapproved.')
    unapprove_comments.short_description = 'Unapprove selected comments'
