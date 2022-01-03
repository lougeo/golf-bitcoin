from django.contrib import admin

from .models import Friendship, FriendRequest, FriendshipStatus


class FriendshipAdmin(admin.ModelAdmin):
    list_display = ["user", "friend", "status", "created"]
    search_fields = [
        "user__first_name",
        "user__last_name",
        "user__email",
        "friend__first_name",
        "friend__last_name",
        "friend__email",
    ]
    ordering = ["-created"]


class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ["sender", "receiver", "accepted", "active", "created"]
    search_fields = [
        "sender__first_name",
        "sender__last_name",
        "sender__email",
        "receiver__first_name",
        "receiver__last_name",
        "receiver__email",
    ]
    ordering = ["-created"]


class FriendshipStatusAdmin(admin.ModelAdmin):
    list_display = ["name", "verb", "slug"]
    search_fields = [
        "name",
        "verb",
        "slug",
    ]
    ordering = ["name"]


admin.site.register(Friendship, FriendshipAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)
admin.site.register(FriendshipStatus, FriendshipStatusAdmin)
