from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profiles, Favorites, Comparisons, Orders, Purchases


admin.site.register(Profiles)
admin.site.register(Favorites)
admin.site.register(Comparisons)
admin.site.register(Orders)
admin.site.register(Purchases)
