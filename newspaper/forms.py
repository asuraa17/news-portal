from django import forms
from newspaper.models import Contact, Comment, Newsletter, Tag, Category, Post

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["post","content"]

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = "__all__"

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "icon", "description"]

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "featured_image",
            "author",
            "status",
            "views_count",
            "is_breaking_news",
            "published_at",
            "category",
            "tag",
        ]
