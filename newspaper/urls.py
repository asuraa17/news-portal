from django.urls import path
from newspaper import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("post-list/", views.PostListView.as_view(), name="post-list"),
    path("post-detail/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contact/", views.ContactCreateView.as_view(), name="contact"),
    path("category/<int:category_id>/", views.PostByCategoryView.as_view(), name="category"),
    path("category-list/", views.CategoryList.as_view(), name="category-list"),
    path("tag/<int:tag_id>/", views.PostByTagView.as_view(), name="tag"),
    path("tag-list/", views.TagList.as_view(), name="tag-list"),
    path("newsletter/", views.NewsletterView.as_view(), name="newsletter"),
    path("post-search/", views.PostSearchView.as_view(), name="post-search"),
    path("dashboard/", views.AdminListView.as_view(), name="dashboard"),
    path("dashboard/tags/", views.DashboardTagListView.as_view(), name="dashboard-tags"),
    path("dashboard/categories/", views.DashboardCategoryListView.as_view(), name="dashboard-categories"),
    path("dashboard/posts/", views.DashboardPostListView.as_view(), name="dashboard-posts"),

    # Tag CRUD
    path("dashboard/tags/add/", views.DashboardTagCreateView.as_view(), name="dashboard-tag-add"),
    path("dashboard/tags/<int:pk>/edit/", views.DashboardTagUpdateView.as_view(), name="dashboard-tag-edit"),
    path("dashboard/tags/<int:pk>/delete/", views.DashboardTagDeleteView.as_view(), name="dashboard-tag-delete"),

    # Category CRUD
    path("dashboard/categories/add/", views.DashboardCategoryCreateView.as_view(), name="dashboard-category-add"),
    path("dashboard/categories/<int:pk>/edit/", views.DashboardCategoryUpdateView.as_view(), name="dashboard-category-edit"),
    path("dashboard/categories/<int:pk>/delete/", views.DashboardCategoryDeleteView.as_view(), name="dashboard-category-delete"),

    # Post CRUD
    path("dashboard/posts/add/", views.DashboardPostCreateView.as_view(), name="dashboard-post-add"),
    path("dashboard/posts/<int:pk>/edit/", views.DashboardPostUpdateView.as_view(), name="dashboard-post-edit"),
    path("dashboard/posts/<int:pk>/delete/", views.DashboardPostDeleteView.as_view(), name="dashboard-post-delete"),
]


