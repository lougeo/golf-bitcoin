from django.db import models
from django.conf import settings


class Round(models.Model):
    """
    Course can be null so that if there is a course that's not in the system they can still create the round.
    As a result scorecard on score is also nullable for the same reason.
    """

    course = models.ForeignKey(
        "course.Course",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="rounds",
        related_query_name="round",
    )
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through="UserRound")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=150)
    description = models.TextField(max_length=500)
    tee_time = models.DateTimeField(blank=True, null=True)


class UserRound(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_rounds",
        related_query_name="user_round",
    )
    round = models.ForeignKey(
        Round,
        on_delete=models.CASCADE,
        related_name="user_rounds",
        related_query_name="user_round",
    )

    creator = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["round"],
                condition=models.Q(creator=True),
                name="single_creator",
            )
        ]


class Score(models.Model):
    """
    Write signal where if scorecard is set,
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="scores",
        related_query_name="score",
    )
    round = models.ForeignKey(
        Round,
        on_delete=models.CASCADE,
        related_name="scores",
        related_query_name="score",
    )
    scorecard = models.ForeignKey(
        "course.Scorecard",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="scores",
        related_query_name="score",
    )


class Hole(models.Model):
    score = models.ForeignKey(
        Score,
        on_delete=models.CASCADE,
        related_name="holes",
        related_query_name="holes",
    )

    number = models.PositiveSmallIntegerField()
    strokes = models.PositiveSmallIntegerField()

    """
    Copy all metadata fields form ScorecardHole, but nullable.
    """
    par = models.PositiveSmallIntegerField(null=True, blank=True)
    distance = models.PositiveSmallIntegerField(null=True, blank=True)
    handicap = models.PositiveSmallIntegerField(null=True, blank=True)
