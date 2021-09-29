from django.contrib import admin
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from .forms import RoundAdminForm
from .models import Round, UserRound, Score, Hole


class RoundAdmin(admin.ModelAdmin):
    form = RoundAdminForm
    empty_value_display = "----"
    list_display = ["title", "course", "all_users", "tee_time"]

    @admin.display(description="Users")
    def all_users(self, obj):
        user_links = ""
        for user in obj.users.all():
            url = reverse("admin:users_golfuser_change", args=[user.pk])
            user_links += f"<a href='{url}'>{user}</a><br/>"
        return mark_safe(user_links) if user_links else "----"


class UserRoundAdmin(admin.ModelAdmin):
    list_display = ["user", "round", "creator"]


class ScoreAdmin(admin.ModelAdmin):
    list_display = ["user", "round", "scorecard"]


class HolesAdmin(admin.ModelAdmin):
    list_display = ["score", "number", "strokes"]


admin.site.register(Round, RoundAdmin)
admin.site.register(UserRound, UserRoundAdmin)
admin.site.register(Score, ScoreAdmin)
admin.site.register(Hole, HolesAdmin)
