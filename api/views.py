from django.shortcuts import render
from djoser.views import UserViewSet as DjoserUserViewSet
from django.db.models import Count
from requests import Response
from rest_framework.generics import get_object_or_404, ListAPIView
from api.models import User, RecipeVersion, Note, TasterFeedback
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import UpdateAPIView, RetrieveUpdateDestroyAPIView
from api.serializers import NoteDetailSerializer, NoteSerializer, RecipeVersionSerializer, RecipeVersionDetailSerializer, UserCreateSerializer, UserSerializer, TasterFeedbackSerializer, TasterFeedbackDetailSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsChefOrReadOnly, RecipeIsChefOrReadOnly
from django.db.models import Q
from taggit.models import Tag
from django.db.models.query import QuerySet
from rest_framework.permissions import AllowAny


class UserViewSet(DjoserUserViewSet):
    queryset            = User.objects.all()
    serializer_class    = UserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            serializer_class = UserCreateSerializer
        else:
            serializer_class = UserSerializer
        return serializer_class


class RecipeVersionViewSet(ModelViewSet):
    queryset          = RecipeVersion.objects.all().order_by('-id')
    serializer_class  = RecipeVersionSerializer
    permission_classes = (RecipeIsChefOrReadOnly,)

    # For Taggit
    def index(request):
        recipe_versions = RecipeVersion.get.prefetch_related('tags').all()
        tags = Tag.objects.all()
        context = {'recipe_versions':recipe_versions, 'tags': tags}
        return render(request, 'api/index.html', context)

    def get_queryset(self):
        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            queryset = queryset.all()
            if self.request.user.is_authenticated:
                queryset = queryset.filter(chef=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(chef=self.request.user)

    def perform_destroy(self, instance):
        if self.request.user  == instance.chef:
            instance.delete()

    def perform_update(self,serializer):
        if self.request.user == serializer.instance.chef:
            serializer.save()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RecipeVersionSerializer
        return RecipeVersionDetailSerializer


class AllRecipeVersionViewSet(ModelViewSet):
    queryset          = RecipeVersion.objects.all()
    serializer_class  = RecipeVersionSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    # For Taggit
    def index(request):
        recipe_versions =RecipeVersion.get.prefetch_related('tags').all()
        tags = Tag.objects.all()
        context = {'recipe_versions':recipe_versions, 'tags': tags}
        return render(request, 'api/index.html', context)

    def get_queryset(self):
        search_term = self.request.query_params.get("search")
        if search_term is not None:
            results = RecipeVersion.objects.filter(
                Q(title__icontains=search_term) |
                Q(ingredients__icontains=search_term)
            )
            results.order_by('-id')

        else:
            results = RecipeVersion.objects.annotate(
                total_recipes=Count('recipe_steps')
            )
        return results.order_by('-id')


class NoteViewSet(ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsChefOrReadOnly]

    def get_queryset(self):
        assert self.queryset is not None, (
            "'%s' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method."
            % self.__class__.__name__
        )

        queryset = self.queryset
        recipe_version = get_object_or_404(RecipeVersion, pk=self.kwargs["recipe_pk"])
        if isinstance(queryset, QuerySet):
            queryset = queryset.all()
            queryset = queryset.filter(recipe_version=recipe_version)

        return queryset

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            recipe_version = get_object_or_404(RecipeVersion, pk=self.kwargs["recipe_pk"])
            serializer.save(note_by=self.request.user, recipe_version=recipe_version)

    def perform_update(self,serializer):
        if self.request.user == serializer.instance.note_by:
            serializer.save()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NoteSerializer
        return NoteDetailSerializer


class AllNoteViewSet(ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        search_term = self.request.query_params.get("search")
        if search_term is not None:
            results = Note.objects.filter(
                Q(note__icontains=search_term)
                )
            results

        else:
            results = Note.objects.annotate(
                total_recipes=Count('note')
            )
        return results.order_by('-id')


class TasterFeedbackView(ModelViewSet):
    queryset = TasterFeedback.objects.all().order_by('-created_at')
    serializer_class = TasterFeedbackSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        assert self.queryset is not None, (
            "'%s' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method."
            % self.__class__.__name__
        )

        queryset = self.queryset
        test_recipe = get_object_or_404(RecipeVersion, pk=self.kwargs["recipe_pk"])
        if isinstance(queryset, QuerySet):
            queryset = queryset.all()
            queryset = queryset.filter(test_recipe=test_recipe)

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            serializer_class = TasterFeedbackSerializer
        else:
            serializer_class = TasterFeedbackDetailSerializer
        return serializer_class

    def perform_create(self, serializer):
        test_recipe = get_object_or_404(RecipeVersion, pk=self.kwargs["recipe_pk"])
        if self.request.user.is_authenticated:
            serializer.save(tester=self.request.user, test_recipe=test_recipe)
        else:
            serializer.save(test_recipe=test_recipe)

    def perform_destroy(self, instance):
        if self.request.user  == instance.tester:
            instance.delete()

    def perform_update(self,serializer):
        if self.request.user == serializer.instance.tester:
            serializer.save()


class TasterFeedbackDetailView(ModelViewSet):
    queryset = TasterFeedback.objects.all().order_by('-created_at')
    serializer_class = TasterFeedbackDetailSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        assert self.queryset is not None, (
            "'%s' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method."
            % self.__class__.__name__
        )

        queryset = self.queryset
        test_recipe = get_object_or_404(RecipeVersion, pk=self.kwargs["recipe_pk"])
        if isinstance(queryset, QuerySet):
            queryset = queryset.all()
            queryset = queryset.filter(test_recipe=test_recipe)

        return queryset

    def perform_destroy(self, instance):
        if self.request.user  == instance.tester:
            instance.delete()

    def perform_update(self,serializer):
        if self.request.user == serializer.instance.tester:
            serializer.save()


# For Taggit
class RecipeListAPIView(ListAPIView):
        queryset = RecipeVersion.objects.all()
        serializer_class = RecipeVersionSerializer
