from django.shortcuts import render
from newspaper.models import Category, Post, Advertisement, OurTeam, Contact, Tag
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse, reverse_lazy
from .forms import ContactForm, CommentForm, NewsletterForm, TagForm, CategoryForm, PostForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
# Create your views here.

class SidebarMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["popular_posts"] = Post.objects.filter(published_at__isnull = False, status="active").order_by("-published_at")[:5]
        
        context["advertisement"] = (
            Advertisement.objects.all().order_by("-created_at").first()
        )

        return context


class HomeView(SidebarMixin, TemplateView):
    template_name = "newsportal/home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["featured_post"] = (Post.objects.filter(published_at__isnull=False, status="active").order_by("-published_at","-views_count").first())
        
        context["trending_news"] = Post.objects.filter(published_at__isnull = False, status="active").order_by("-views_count")[:4]
                
        one_week_ago = timezone.now()- timedelta(days=7)
        
        context["weekly_top_posts"] = Post.objects.filter(published_at__isnull = False, status="active", published_at__gte=one_week_ago).order_by("-published_at","-views_count")[:5]
        
        context["breaking_news"] = Post.objects.filter(published_at__isnull=False, status="active", is_breaking_news=True).order_by("-published_at")[:5]
        
        return context

class PostListView(SidebarMixin, ListView):
    model = Post
    template_name = "newsportal/list/list.html"
    context_object_name = "posts"
    paginate_by = 2

    def get_queryset(self):
        return Post.objects.filter(
            published_at__isnull = False, status = "active"
        ).order_by("-published_at")
    
    
from django.views.generic.edit import FormMixin
    
class PostDetailView(SidebarMixin, FormMixin, DetailView):
    model = Post
    template_name = "newsportal/detail/detail.html"
    context_object_name = "post"
    form_class = CommentForm

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(published_at__isnull=False, status = "active")
        return query
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_post = self.object
        current_post.views_count += 1
        current_post.save()
        
        context["related_posts"] = (
            Post.objects.filter(
                published_at__isnull=False,
                status= "active",
                category=self.object.category,
            )
            .exclude(id=self.object.id)
            .order_by("-published_at", "-views_count")[:2]
            )
        

        return context
    
    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.pk})
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.user = self.request.user
        comment.save()
        messages.success(self.request, "Your comment has been added successfully.")
        return super().form_valid(form)
    

class AboutView(TemplateView):
    template_name = "newsportal/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["our_teams"] = OurTeam.objects.all()
        return context
    

class ContactCreateView(SuccessMessageMixin, CreateView):
    model = Contact
    template_name = "newsportal/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact")
    success_message = "Your message has been sent successfully!"

    def form_invalid(self, form):
        messages.error(
            self.request,
            "There was an error sending your message. PLease check the form"
        )
        return super().form_invalid(form)


class PostByCategoryView(SidebarMixin, ListView):
    model = Post
    template_name = "newsportal/list/list.html"
    context_object_name = "posts"
    paginate_by = 2

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(
            published_at__isnull = False,
            status = "active",
            category__id = self.kwargs["category_id"],
        ).order_by("-published_at")
        return query
    
    
class CategoryList(ListView):
    model = Category
    template_name = "newsportal/categories.html"
    context_object_name = "categories"


class PostByTagView(SidebarMixin, ListView):
    model = Post
    template_name = "newsportal/list/list.html"
    context_object_name = "posts"
    paginate_by = 2

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(
            published_at__isnull = False,
            status = "active",
            tag__id = self.kwargs["tag_id"],
        ).order_by("-published_at")
        return query
    

class TagList(ListView):
    model = Tag
    template_name = "newsportal/tags.html"
    context_object_name = "tags"


class NewsletterView(View):
    def post(self, request):
        is_ajax = request.headers.get("x-requested-with")
        if is_ajax == "XMLHttpRequest":
            form = NewsletterForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse(
                    {
                        "success": True,
                        "message": "Successfully subscribed to the newsletter.",
                    },
                    status=201,
                    )
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Cannot subscribe to the newsletter.",
                    },
                    status=400,
                )
        else:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Cannot process. Must be an AJAX XMLHttpRequest.",
                },
                status=400,
            )
        

from django.core.paginator import PageNotAnInteger, Paginator
from django.db.models import Q
# | => OR
# & => AND

class PostSearchView(View):
    template_name = "newsportal/list/list.html"
    
    def get(self, request):
    #query=nepal search title nepal or content nepal
    
        print(request.GET)
        query = request.GET["query"]       
        post_list = Post.objects.filter(
            (Q(title__icontains=query) | Q(content__icontains=query))
            & Q(status="active")
            & Q(published_at__isnull=False)
            ).order_by("-published_at") # QuerySet => ORM 
        
        #pagination start
        page = request.GET.get("page", 1) #x
        paginate_by = 1
        paginator = Paginator(post_list, paginate_by)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
            # pagination end
             
        popular_posts = Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at")[:5]
            
        advertisement = Advertisement.objects.all().order_by("-created_at").first()
        return render(
            request,
            self.template_name,
            {
                "page_obj": posts,
                "query": query,
                "popular_posts": popular_posts,
                "advertisement": advertisement,
            },
        )
    
class AdminListView(ListView):
    template_name = "dashboard/index.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.filter(
            published_at__isnull=False,
            status="active"
        ).order_by("-published_at")


class DashboardTagListView(ListView):
    model = Tag
    template_name = "dashboard/tag-list.html"
    context_object_name = "tags"


class DashboardCategoryListView(ListView):
    model = Category
    template_name = "dashboard/category-list.html"
    context_object_name = "categories"


class DashboardPostListView(ListView):
    model = Post
    template_name = "dashboard/post-list.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.all().order_by("-created_at")


class DashboardTagCreateView(SuccessMessageMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = "dashboard/form.html"
    success_url = reverse_lazy("dashboard-tags")
    success_message = "Tag added successfully."

class DashboardTagUpdateView(SuccessMessageMixin, UpdateView):
    model = Tag
    form_class = TagForm
    template_name = "dashboard/form.html"
    success_url = reverse_lazy("dashboard-tags")
    success_message = "Tag updated successfully."

class DashboardTagDeleteView(SuccessMessageMixin, DeleteView):
    model = Tag
    template_name = "dashboard/del.html"
    success_url = reverse_lazy("dashboard-tags")
    success_message = "Tag deleted successfully."


class DashboardCategoryCreateView(SuccessMessageMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "dashboard/form.html"
    success_url = reverse_lazy("dashboard-categories")
    success_message = "Category added successfully."

class DashboardCategoryUpdateView(SuccessMessageMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "dashboard/form.html"
    success_url = reverse_lazy("dashboard-categories")
    success_message = "Category updated successfully."

class DashboardCategoryDeleteView(SuccessMessageMixin, DeleteView):
    model = Category
    template_name = "dashboard/del.html"
    success_url = reverse_lazy("dashboard-categories")
    success_message = "Category deleted successfully."


class DashboardPostCreateView(SuccessMessageMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "dashboard/form.html"
    success_url = reverse_lazy("dashboard-posts")
    success_message = "Post added successfully."

class DashboardPostUpdateView(SuccessMessageMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "dashboard/form.html"
    success_url = reverse_lazy("dashboard-posts")
    success_message = "Post updated successfully."

class DashboardPostDeleteView(SuccessMessageMixin, DeleteView):
    model = Post
    template_name = "dashboard/del.html"
    success_url = reverse_lazy("dashboard-posts")
    success_message = "Post deleted successfully."

