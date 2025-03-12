from django.db import models


class Supplier(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Ad"
    )
    contact_info = models.TextField(
        blank=True,
        verbose_name="Əlaqə Məlumatları"
    )

    class Meta:
        verbose_name = "Təchizatçı"
        verbose_name_plural = "Təchizatçılar"

    def __str__(self):
        return self.name
