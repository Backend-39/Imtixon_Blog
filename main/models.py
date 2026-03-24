from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        tag_name = self.name.strip()
        if not tag_name.startswith('#'):
            tag_name = '#' + tag_name
        self.name = tag_name

        super().save(*args,**kwargs)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True,null=True, blank=True)
    context = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tag,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    article_type = models.CharField(
        choices=[
            ('shaxsiy', 'Shaxsiy'),
            ('ommaviy', 'Ommaviy')
        ],
        default='shaxsiy'
    )

    def __str__(self):
        return f"{self.user.username}: {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while Article.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        return super().save(*args, **kwargs)

