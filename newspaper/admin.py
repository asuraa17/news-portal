from django.contrib import admin
from .models import Advertisement, Category, Post, Tag, OurTeam, Contact, Comment, Newsletter
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Advertisement)
admin.site.register(OurTeam)
admin.site.register(Contact)
admin.site.register(Comment)
admin.site.register(Newsletter)


class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)

admin.site.register(Post, PostAdmin)