from django.contrib import admin
from .models import Tracker, Visit


admin.site.register(Tracker, Visit)
