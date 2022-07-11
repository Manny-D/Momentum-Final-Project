from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import HiddenInput
from taggit.managers import TaggableManager
from django.contrib.postgres.fields import ArrayField

class User(AbstractUser):
    location = models.CharField(max_length=100, blank=True, null=True)
    business_name = models.CharField(max_length=200, blank=True, null=True)
    
    def __repr__(self):
        return f"<User username={self.username} pk={self.pk}>"

    def __str__(self):
        return self.username


class RecipeVersion(models.Model):
    title = models.CharField(max_length=255)
    ingredients = ArrayField(models.TextField())
    recipe_steps = ArrayField(models.TextField())
    image = models.ImageField(blank=True, null=True)
    ready_for_feedback = models.BooleanField(default=False)
    successful_variation = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    chef = models.ForeignKey('User', on_delete=models.CASCADE, related_name='recipe_versions', max_length=255)

    tags = TaggableManager(blank=True)

    class Meta:
        verbose_name = 'RecipeVersion'
        verbose_name_plural = 'RecipeVersions'

    def __str__(self):
        return f"{self.title} by {self.chef}"


class Note(models.Model):
    note = models.TextField(blank=False)
    recipe_version = models.ForeignKey('RecipeVersion', on_delete=models.CASCADE, related_name='notes', max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    note_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='notes')

    tags = TaggableManager(blank=True)
    
    def __str__(self):
        return f"{self.recipe_version} by {self.note_by}"


class TasterFeedback(models.Model):

    BLANK = '-'
    ONE   = '1' 
    TWO   = '2'
    THREE = '3'
    FOUR  = '4'
    FIVE  = '5'

    RADIO = [ 
        (BLANK , '-'),
        (ONE , '1'), 
        (TWO , '2'), 
        (THREE , '3'), 
        (FOUR , '4'), 
        (FIVE , '5'), 
        ]

    NO_ANSWER  = '----------'
    TOO_LITTLE = 'Too Little'
    JUST_RIGHT = 'Just Right'
    TOO_MUCH   = 'Too Much'

    SCALE = [ 
        (NO_ANSWER  , '----------'),
        (TOO_LITTLE , 'Too Little'), 
        (JUST_RIGHT , 'Just Right'),
        (TOO_MUCH , 'Too Much'), 
        ]
    
    NONE = '---'
    YES  = 'Yes'
    NO   = 'No'

    CHOICE = [ 
        (NONE , '---'),
        (YES , 'Yes'), 
        (NO , 'No'), 
        ]
    
    rating = models.CharField(max_length=6, choices=RADIO, default=BLANK,)
    saltiness = models.CharField(max_length= 11, choices=SCALE, default=NO_ANSWER,)
    sweetness = models.CharField(max_length= 11, choices=SCALE, default=NO_ANSWER,)
    portion = models.CharField(max_length= 11, choices=SCALE, default=NO_ANSWER,)
    texture = models.CharField(max_length= 5, choices=CHOICE, default=NONE,)
    additional_comment = models.CharField(max_length=200,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    test_recipe = models.ForeignKey('RecipeVersion', on_delete=models.CASCADE, related_name='taster_feedbacks', max_length = 255)
    tester = models.ForeignKey('User', on_delete=models.CASCADE, related_name='taster_feedbacks', null=True, max_length=50)

    class Meta:
        verbose_name = 'TasterFeedback'
        verbose_name_plural = 'TasterFeedbacks'


    def __str__(self):
        return f"Feedback for {self.test_recipe}"