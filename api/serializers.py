from dataclasses import fields
from rest_framework import serializers
from djoser.serializers import UserSerializer as DjoserUserSerializer
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from .models import RecipeVersion, Note, User, TasterFeedback
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)

class UserSerializer(DjoserUserSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'date_joined',
            'location',
            'business_name',
        )


class UserCreateSerializer(DjoserUserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'password',
            'last_name',
            'date_joined',
            'location',
            'business_name',
        )


class RecipeVersionSerializer (serializers.ModelSerializer):
    chef        = serializers.SlugRelatedField(read_only=True, slug_field="username")
    notes = serializers.SlugRelatedField(many=True, read_only=True, slug_field='note')
    ingredients = serializers.ListField(child=serializers.CharField())
    recipe_steps =serializers.ListField(child=serializers.CharField())
    
    class Meta: 
        model  = RecipeVersion
        fields = [
            'id',
            'title',
            'ingredients',
            'recipe_steps',
            'image',
            'ready_for_feedback',
            'successful_variation',
            'chef',
            'created_at',
            'notes',
            ]


class RecipeVersionDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    chef        = serializers.SlugRelatedField(read_only=True, slug_field="username")
    notes = serializers.SlugRelatedField(many=True, read_only=True, slug_field='note')
    ingredients = serializers.ListField(child=serializers.CharField())
    recipe_steps =serializers.ListField(child=serializers.CharField())
    tags = TagListSerializerField()

    class Meta:
        model  = RecipeVersion
        fields = [
            'id',
            'title',
            'ingredients',
            'recipe_steps',
            'image',
            'ready_for_feedback',
            'successful_variation',
            'chef',
            'created_at',
            'tags',
            'notes',
            ]


# For Taggit
class RecipeListSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = RecipeVersion
        fields = (
            'id',
            'title',
            'chef',
            'tags',
        )


class NoteSerializer(serializers.ModelSerializer):
    note_by = serializers.SlugRelatedField(read_only=True, slug_field="username")
    
    class Meta:
        model = Note
        fields = [
            'id',
            'note',
            'note_by',
            'created_at',
        ]


class NoteDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    note_by = serializers.SlugRelatedField(read_only=True, slug_field="username")
    tags = TagListSerializerField()

    class Meta:
        model = Note
        fields = [
            'id',
            'note',
            'note_by',
            'recipe_version',
            'tags',
            'created_at',
        ]


class TasterFeedbackSerializer(TaggitSerializer, serializers.ModelSerializer):

    class Meta:
        model = TasterFeedback
        fields = [
            'id',
            'rating',
            'saltiness',
            'sweetness',
            'portion',
            'texture',
            'additional_comment',
            'created_at',
        ]


class TasterFeedbackDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    tester = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = TasterFeedback
        fields = [
            'id',
            'test_recipe',
            'rating',
            'saltiness',
            'sweetness',
            'portion',
            'texture',
            'additional_comment',
            'tester',
            'created_at',
        ]