from django.contrib import admin
from .models import Course, Scorecard, ScorecardHole


class CourseAdmin(admin.ModelAdmin):
    list_display = ["name"]


class ScorecardAdmin(admin.ModelAdmin):
    list_display = ["title", "course"]


class ScorecardHoleAdmin(admin.ModelAdmin):
    list_display = ["scorecard", "number", "par", "distance", "handicap"]


admin.site.register(Course, CourseAdmin)
admin.site.register(Scorecard, ScorecardAdmin)
admin.site.register(ScorecardHole, ScorecardHoleAdmin)
