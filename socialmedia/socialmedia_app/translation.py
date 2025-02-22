from .models import  UserProfile, Post
from modeltranslation.translator import TranslationOptions,register

@register(UserProfile)
class UserProfileTranslationOptions(TranslationOptions):
    fields = ('bio',)

@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('hashtag',)