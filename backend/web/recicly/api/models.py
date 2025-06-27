from django.db import models
from django.utils import timezone
from django.urls import reverse
import json

class BlogPost(models.Model):
    # Primary key (Django creates this automatically, but keeping it explicit)
    id = models.AutoField(primary_key=True)

    #Basic content field
    title = models.CharField(max_length=200, null=False, blank=False, help_text="The main title of the blog post")

    subtitle = models.CharField(max_length=300, null=True, blank=True, help_text="Optional subtitle for the blog post")

    content = models.CharField(null=False, blank=False, help_text="The main content of the blog post")

    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True,
                           help_text="URL-friendly version of the title")
    
    meta_description = models.CharField(max_length=160, null=True, blank=True,
                                      help_text="SEO meta description")
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    photo_urls = models.JSONField(default=list, blank=True,
                                help_text="Array of photo URLs for the blog post")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                            default='draft')
    
    date_published = models.DateTimeField(null=True, blank=True,
                                help_text="When the post was published")
    date_created = models.DateTimeField(auto_now_add=True)

    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "blog_posts"
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
        ordering = ['-date_created']
        indexes = [
            models.Index(fields=['status', '-date_created']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return f"{self.title} ({self.status})"
    
    def save(self, *args, **kwargs):
        # Auto-generate slug from title if not provided
        if not self.slug and self.title:
            from django.utils.text import slugify
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            
            # Ensure slug uniqueness
            while BlogPost.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = slug
        
        # Set published date when status changes to published
        if self.status == 'published' and not self.date_published:
            self.date_published = timezone.now()
        
        # Clear published date if status is no longer published
        elif self.status != 'published' and self.date_published:
            self.date_published = None
            
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Get the URL for this blog post"""
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    @property
    def is_published(self):
        """Check if the post is published"""
        return self.status == 'published'
    
    @property
    def reading_time(self):
        """Estimate reading time in minutes"""
        word_count = len(self.content.split())
        return max(1, round(word_count / 200))
    
    def add_photo_url(self, url):
        """Add a photo URL to the list"""
        if url not in self.photo_urls:
            self.photo_urls.append(url)
            self.save()

    def remove_photo_url(self, url):
        """Remove a photo URL from the list"""
        if url in self.photo_urls:
            self.photo_urls.remove(url)
            self.save()
        


