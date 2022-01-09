from django.conf import settings
from django.db import models

from django.utils.translation import ugettext_lazy as _


class FriendshipManager(models.Manager):
    def kindle(self, user, friend, status=None, set_friend=True):
        """
        Update or create a new friend.
        """

        if status is None:
            status = FriendshipStatus.objects.accepted()

        friendship, created = Friendship.objects.update_or_create(
            user=user, friend=friend, defaults={"status": status}
        )

        if set_friend:
            return (
                friendship,
                self.kindle(friend, user, status=status, set_friend=False),
            )
        else:
            return friendship

    def is_mutual_friend(self, friend):
        """
        Is this a mutual friend?
        """
        # if friend in self.friends.all():
        #     return True
        # return False
        pass


class Friendship(models.Model):
    """
    Through model for friends many to many on GolfUser.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="friendships",
        related_query_name="friendship",
    )
    friend = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="friends_friendships",
        related_query_name="friends_friendship",
    )

    status = models.ForeignKey(
        "FriendshipStatus",
        on_delete=models.CASCADE,
        related_name="friendships",
        related_query_name="friendship",
    )

    created = models.DateTimeField(auto_now_add=True)

    objects = FriendshipManager()

    class Meta:
        ordering = ("-created",)
        constraints = [
            models.UniqueConstraint(
                fields=["user", "friend"],
                name="unique_friendship",
            )
        ]

    def __str__(self):
        return f"{self.user.email}, {self.friend.email}"


class FriendRequest(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sender_friend_requests",
        related_query_name="sender_friend_request",
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="receiver_friend_requests",
        related_query_name="receiver_friend_request",
    )

    accepted = models.BooleanField(null=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created",)
        verbose_name = _("Friend Request")
        verbose_name_plural = _("Friend Requests")
        constraints = [
            models.UniqueConstraint(
                fields=["sender", "receiver"],
                name="unique_friend_request",
            )
        ]

    def __str__(self):
        return f"Friend Request from: {self.sender} to: {self.receiver}"

    def accept(self):
        """
        Accept a friend request.
        """

        Friendship.objects.kindle(self.sender, self.receiver)
        self.accepted = True
        self.active = False
        self.save()

    def decline(self):
        """
        Decline a friend request.
        """
        status = FriendshipStatus.objects.declined()
        Friendship.objects.kindle(self.sender, self.receiver, status=status)
        self.accepted = False
        self.active = False
        self.save()

    def cancel(self):
        """
        Cancel a friend request
        Same as decline but different notification behavior.
        """

        self.accepted = False
        self.active = False
        self.save()


class FriendshipStatusManager(models.Manager):
    def accepted(self):
        return self.get(slug="accepted")

    def declined(self):
        return self.get(slug="declined")


class FriendshipStatus(models.Model):
    name = models.CharField(max_length=100)
    verb = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)

    objects = FriendshipStatusManager()

    class Meta:
        ordering = ("name",)
        verbose_name = _("Friendship Status")
        verbose_name_plural = _("Friendship Statuses")

    def __str__(self):
        return self.name
