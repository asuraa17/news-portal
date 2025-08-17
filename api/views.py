from api.serializers import AdvertisementSerializer, GroupSerializer, NewsLetterSerializer, PostSerializer, UserSerializer, TagSerializer, CategorySerializer, PostPublishSerializer

from django.shortcuts import render
from django.contrib.auth.models import Group, User
from django.utils import timezone

from newspaper.models import Advertisement, Newsletter, Post, Tag, Category

from rest_framework import status, exceptions, permissions, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tags to be viewed or edited.
    """
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        
        return super().get_permissions()


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        
        return super().get_permissions()


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or edited.
    """
    queryset = Post.objects.all().order_by('-published_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action in ["list", "retrieve"]:
            queryset = queryset.filter(status="active")

        from django.db.models import Q
        query = self.request.query_params.get("query", None)
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )    
        
        return queryset
    
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        
        return super().get_permissions()
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1
        instance.save(update_fields=["views_count"])
        serializer = self.get_serializer(instance)
        
        return Response(serializer.data)
    

class PostbyCategoryViewSet(viewsets.ModelViewSet):
    
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            status="active",
            published_at__isnull=False,
            category=self.kwargs["category_id"]
            )
          
        return queryset

class PostbyTagViewSet(viewsets.ModelViewSet):
    
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            status="active",
            published_at__isnull=False,
            tag=self.kwargs["tag_id"]
            )
          
        return queryset


class AdvertisementViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows advertisement to be viewed or edited.
    """
    queryset = Advertisement.objects.all().order_by('title')
    serializer_class = AdvertisementSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        
        return super().get_permissions()


class DraftListView(ListAPIView):
    queryset = Post.objects.filter(published_at__isnull=True)
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAdminUser]


class DraftDetailView(RetrieveAPIView):
    queryset = Post.objects.filter(published_at__isnull=True)
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAdminUser]



class PostPublishView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = PostPublishSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data

            post = Post.objects.get(pk=data["id"])
            post.published_at = timezone.now()
            post.save()

            serialized_data = PostSerializer(post).data
            return Response(serializer.data, status=status.HTTP_200_OK)


class NewsLetterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows newsletter to be viewed or edited.
    """
    queryset = Newsletter.objects.all()
    serializer_class = NewsLetterSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action in ["list", "retrieve", "destroy"]:
            return [permissions.IsAdminUser()]
        
        return super().get_permissions()
    
    def update(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed(request.method)

