from django.db import models

# Create your models here.

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True #dont create table in db


class Category(TimeStampModel):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["name"] #category.objects.all()
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Tag(TimeStampModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        """
        Return a string representation of the tag, which is its name.
        """
        return self.name


class Post(TimeStampModel):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("in_active", "Inactive"),
    ]

    title = models.CharField(max_length=100)
    content = models.TextField()
    featured_image = models.ImageField(upload_to="post_images/%Y/%m/%d", blank=False)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default="active")
    views_count = models.PositiveBigIntegerField(default=0)
    is_breaking_news = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
    

class Advertisement(TimeStampModel):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="advertisements/%Y/%m/%d", blank=False)

    def __str__(self):
        return self.title


class OurTeam(TimeStampModel):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    image = models.ImageField(upload_to="teams_images/%Y/%m/%d", blank=False)
    description = models.TextField()

    def __str__(self):
        return self.name
    
    
class Contact(TimeStampModel):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["created_at"]


class Comment(TimeStampModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"{self.content[:50]} | {self.user.username}"

class Newsletter(TimeStampModel):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

# user - post
# 1 user can have many posts - M
# 1 post belongs to 1 user - 1
# ForeignKey on Post model

# user - comment
# 1 user can write many comments - M
# 1 comment is written by 1 user - 1
# ForeignKey on Comment model

# post - comment
# 1 post can have many comments - M
# 1 comment belongs to 1 post - 1
# ForeignKey on Comment model

# post-user
# 1 user can have many posts -M
# 1 post can have 1 user - 1
# foreignkey -m-Post

# post-category
# 1 category can have many posts -M
# 1 post can have 1 category - 1
# foreign key -m-post

# post-tag
# 1 tag can have many posts -M
# 1 post can have many tags - M
# manytomany field - m-any-post