from django.contrib import admin
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from .forms import RoundAdminForm
from .models import Round, UserRound, Score, Hole


class RoundAdmin(admin.ModelAdmin):
    form = RoundAdminForm
    empty_value_display = "----"
    list_display = ["title", "course", "all_users", "tee_time"]

    @admin.display(description="Users")
    def all_users(self, obj):
        user_links = list()
        for user in obj.users.all():
            url = reverse("admin:users_golfuser_change", args=[user.pk])
            link = f"<a href='{url}'>{obj}</a><br/>"
            user_links.append(link)
        return user_links if user_links else "----"


admin.site.register(Round, RoundAdmin)
admin.site.register(UserRound)
admin.site.register(Score)
admin.site.register(Hole)
