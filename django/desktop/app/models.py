from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.username}"


class DirectoryUser(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="directories"
    )

    nome = models.CharField(max_length=255)

    # @parent: mi serve per la ricorsione delle directory
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="subdirectories"
    )

    creation_date = models.DateField()
    last_modify_date = models.DateField()

    class Meta:
        verbose_name = "DirectoryUser"
        verbose_name_plural = "DirectoryUsers"

    def __str__(self):
        return f"{self.user_id} - {self.nome}"


class FileUser(models.Model):
    directory = models.ForeignKey(
        DirectoryUser,
        on_delete=models.CASCADE,
        related_name="file"
    )

    nome = models.CharField(max_length=255)
    content = models.TextField()

    creation_date = models.DateField()
    last_modify_date = models.DateField()

    class Meta:
        verbose_name = "FileUser"
        verbose_name_plural = "FileUsers"

    def __str__(self):
        return f"{self.directory_id} - namefile: {self.nome}"
