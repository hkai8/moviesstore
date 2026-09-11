from django.contrib import admin
from .models import Movie, Review
class MovieAdmin(admin.ModelAdmin):
    ordering = ['name'] #allows customize behavior of admin interface for Movie model
    search_fields = ['name'] # allow searches by name in admin interface
admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)