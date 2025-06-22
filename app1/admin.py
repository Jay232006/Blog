from django.contrib import admin

# Register your models here.
from .models import BlogPost  # import your model

admin.site.register(BlogPost) 