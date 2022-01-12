from django.db import models
from django.conf import settings


class Round(models.Model):
    course = models.ForeignKey(
        "course.Course",
        on_delete=models.CASCADE,
        related_name="rounds",
        related_query_name="round",
    )
    scorecard = models.ForeignKey(
        "course.Scorecard",
        on_delete=models.CASCADE,
        related_name="rounds",
        related_query_name="round",
    )
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through="Registration")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tee_time = models.DateTimeField(blank=True, null=True)

    title = models.CharField(max_length=150, blank=True)
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.title if self.title else f"Round: {self.pk}"


class Registration(models.Model):
    """
    Through model for Round <-> User.
    """

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
    accepted = models.BooleanField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["round"],
                condition=models.Q(creator=True),
                name="single_creator",
            )
        ]


class Score(models.Model):
    registration = models.ForeignKey(
        Registration,
        on_delete=models.CASCADE,
        related_name="registrations",
        related_query_name="registration",
    )
    scorecard_hole = models.ForeignKey(
        "course.ScorecardHole",
        on_delete=models.CASCADE,
        related_name="scores",
        related_query_name="score",
    )

    strokes = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"Score: {self.pk}"
