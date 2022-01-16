from django.contrib import admin

from .models import CustomUser, Follow


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'first_name', 'last_name', )
    list_filter = ('email', 'username', )


class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author', )


admin.site.register(Follow, FollowAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
