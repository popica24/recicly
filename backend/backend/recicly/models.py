from django.db import models

class BlogPost(models.Model):
    post_id = models.AutoField(primary_key=True)
    post_title = models.CharField(max_length=255, blank=False, null=False)
    post_subtitle = models.CharField(max_length=255, blank=True, null=True)
    post_content = models.CharField(blank=False, null=False)
    post_images = models.BinaryField(blank=False, null=False)
    
    def __str__(self) -> str:
        return self.post_title

    class Meta:
        managed = True
        db_table = "blog_posts"