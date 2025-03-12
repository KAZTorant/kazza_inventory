from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Ad"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Təsvir"
    )

    class Meta:
        verbose_name = "Kateqoriya"
        verbose_name_plural = "Kateqoriyalar"

    def __str__(self):
        return self.name
