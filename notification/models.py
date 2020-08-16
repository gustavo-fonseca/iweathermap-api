from django.db import models


class Email(models.Model):
    """
    Email notification subscriptions
    """
    email = models.EmailField(
        "Email",
        unique=True
    )
    date_joined = models.DateTimeField(
        "Date joined",
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "Email"


class Subscription(models.Model):
    """
    City and state name subscriptions
    Used for task notifications email
    """
    emails = models.ManyToManyField(
        Email,
        verbose_name="Email",
        related_name="subscriptions"
    )
    city_name = models.CharField(
        "City name",
        max_length=150
    )
    state_name = models.CharField(
        "State name",
        max_length=150,
        blank=True
    )

    def __str__(self):
        if self.state_name:
            return f"{self.city_name},{self.state_name}"
        return f"{self.city_name}"

    class Meta:
        verbose_name = "Subscription"
        unique_together = ["city_name", "state_name"]


class EmailNotification(models.Model):
    """
    Email notification for queue sending
    """
    email = models.ForeignKey(
        Email,
        verbose_name="Email",
        related_name="notifications",
        on_delete=models.CASCADE
    )
    template = models.TextField(
        "Email template",
    )
    sent = models.BooleanField(
        "Is email sent",
        default=False
    )
    sent_datetime = models.DateTimeField(
        "Sent datetime",
        null=True,
        blank=True
    )
    opened = models.BooleanField(
        "Is email opened",
        default=False
    )
    opened_datetime = models.DateTimeField(
        "Opened datetime",
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.email.email}"

    class Meta:
        verbose_name = "Email notification"
