from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=150)


class Scorecard(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="scorecards",
        related_query_name="scorecard",
    )
    title = models.CharField(max_length=150)


class ScorecardHole(models.Model):
    scorecard = models.ForeignKey(
        Scorecard,
        on_delete=models.CASCADE,
        related_name="scorecard_holes",
        related_query_name="scorecard_hole",
    )
    number = models.PositiveSmallIntegerField()
    par = models.PositiveSmallIntegerField()
    distance = models.PositiveSmallIntegerField()
    handicap = models.PositiveSmallIntegerField()
