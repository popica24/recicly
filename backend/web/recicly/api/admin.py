from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.db import models
from django.forms import Textarea
from .models import BlogPost


class BlogPostAdmin(admin.ModelAdmin):
    # List view configuration
    list_display = [
        'title', 
        'status_badge', 
        'status',
        'slug',
        'photo_count',
        'date_created', 
        'date_published',
        'reading_time_display'
    ]
    
    list_filter = [
        'status', 
        'date_created', 
        'date_published'
    ]
    
    search_fields = [
        'title', 
        'subtitle', 
        'content', 
        'meta_description',
        'slug'
    ]
    
    list_editable = [
        'status'
    ]
    
    list_per_page = 25
    
    # Detail view configuration
    fieldsets = (
        ('Content', {
            'fields': (
                'title', 
                'subtitle', 
                'slug', 
                'content'
            )
        }),
        ('SEO & Metadata', {
            'fields': (
                'meta_description',
            ),
            'classes': ('collapse',)
        }),
        ('Media', {
            'fields': (
                'photo_urls_display',
                'photo_urls'
            ),
            'description': 'Add photo URLs as a JSON array, e.g., ["url1", "url2"]'
        }),
        ('Publishing', {
            'fields': (
                'status', 
                'date_published'
            )
        }),
        ('Timestamps', {
            'fields': (
                'date_created', 
                'date_updated'
            ),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = [
        'date_created', 
        'date_updated', 
        'photo_urls_display',
        'reading_time_display'
    ]
    
    prepopulated_fields = {
        'slug': ('title',)
    }
    
    # Custom form field configurations
    formfield_overrides = {
        models.CharField: {
            'widget': Textarea(attrs={'rows': 1, 'cols': 80})
        } if 'content' else {},
    }
    
    # Actions
    actions = ['make_published', 'make_draft', 'make_archived']
    
    def get_queryset(self, request):
        """Optimize queryset for admin list view"""
        return super().get_queryset(request).select_related()
    
    # Custom display methods
    def status_badge(self, obj):
        """Display status as a colored badge"""
        colors = {
            'draft': '#ffc107',      # Yellow
            'published': '#28a745',  # Green
            'archived': '#6c757d'    # Gray
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; '
            'border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'
    
    def photo_count(self, obj):
        """Display number of photos"""
        count = len(obj.photo_urls) if obj.photo_urls else 0
        if count > 0:
            return format_html(
                '<span style="background-color: #007bff; color: white; padding: 2px 6px; '
                'border-radius: 10px; font-size: 10px;">{} photos</span>',
                count
            )
        return '-'
    photo_count.short_description = 'Photos'
    
    def photo_urls_display(self, obj):
        """Display photo URLs as clickable links with thumbnails"""
        if not obj.photo_urls:
            return "No photos"
        
        html_parts = []
        for i, url in enumerate(obj.photo_urls, 1):
            html_parts.append(
                f'<div style="margin-bottom: 10px;">'
                f'<strong>Photo {i}:</strong><br>'
                f'<a href="{url}" target="_blank" style="color: #007bff;">{url}</a><br>'
                f'<img src="{url}" style="max-width: 100px; max-height: 100px; '
                f'margin-top: 5px; border: 1px solid #ddd;" '
                f'onerror="this.style.display=\'none\'" />'
                f'</div>'
            )
        
        return mark_safe('<div>' + ''.join(html_parts) + '</div>')
    photo_urls_display.short_description = 'Photo Preview'
    
    def reading_time_display(self, obj):
        """Display estimated reading time"""
        time = obj.reading_time
        return f"{time} min{'s' if time != 1 else ''}"
    reading_time_display.short_description = 'Reading Time'
    
    # Custom actions
    def make_published(self, request, queryset):
        """Bulk action to publish posts"""
        updated = queryset.update(status='published')
        self.message_user(
            request, 
            f'{updated} post{"s" if updated != 1 else ""} successfully published.'
        )
    make_published.short_description = "Mark selected posts as published"
    
    def make_draft(self, request, queryset):
        """Bulk action to set posts as draft"""
        updated = queryset.update(status='draft')
        self.message_user(
            request, 
            f'{updated} post{"s" if updated != 1 else ""} set to draft.'
        )
    make_draft.short_description = "Mark selected posts as draft"
    
    def make_archived(self, request, queryset):
        """Bulk action to archive posts"""
        updated = queryset.update(status='archived')
        self.message_user(
            request, 
            f'{updated} post{"s" if updated != 1 else ""} archived.'
        )
    make_archived.short_description = "Archive selected posts"
    
    # Override form to customize content field
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Make content field a textarea since it's likely long text
        if 'content' in form.base_fields:
            form.base_fields['content'].widget = Textarea(attrs={
                'rows': 10, 
                'cols': 80,
                'style': 'width: 100%;'
            })
        return form
    

# Register the model with the admin
admin.site.register(BlogPost, BlogPostAdmin)