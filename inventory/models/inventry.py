from django.db import models

from inventory.models.category import Category
from inventory.models.supplier import Supplier


class InventoryItem(models.Model):
    UNIT_CHOICES = (
        ('kg', 'Kilogram'),
        ('l', 'Litr'),
        ('pcs', 'Ədəd'),
    )

    name = models.CharField(
        max_length=100,
        verbose_name="Ad"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Kateqoriya"
    )
    unit = models.CharField(
        max_length=20,
        choices=UNIT_CHOICES,
        verbose_name="Vahid"
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Təchizatçı"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaradılma Tarixi"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Yenilənmə Tarixi"
    )

    class Meta:
        verbose_name = "Anbar Məhsulu"
        verbose_name_plural = "Anbar Məhsulları"

    def __str__(self):
        return self.name


class InventoryRecord(models.Model):
    inventory_item = models.ForeignKey(
        InventoryItem,
        on_delete=models.CASCADE,
        related_name='stock_records',
        verbose_name="Anbar Məhsulu"
    )
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Miqdar"
    )
    record_type = models.CharField(
        max_length=16,
        choices=(
            ('add', 'Əlavə'),
            ('remove', 'Çıxış')
        ),
        default="add",
        verbose_name="Əməliyyat növü"
    )
    REASON_CHOICES_ADD = (
        ('purchase', 'Alış'),
        ('gift', 'Hədiyə'),
        ('adjustment', 'Düzəliş'),
    )
    REASON_CHOICES_REMOVE = (
        ('used', 'İstifadə edilmiş'),
        ('expired', 'Müddəti bitmiş'),
        ('damaged', 'Zədələnmiş'),
        ('spoilage', 'Çürükmüş'),
        ('theft', 'Oğurluq'),
        ('other', 'Digər')
    )

    REASON_CHOICES = (*REASON_CHOICES_REMOVE, *REASON_CHOICES_ADD)
    reason = models.CharField(
        max_length=32,
        choices=REASON_CHOICES,
        default="purchase",
        verbose_name="Səbəb"
    )

    purchase_date = models.DateField(
        verbose_name="Alış Tarixi"
    )
    expiration_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Son İstifadə Tarixi"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaradılma Tarixi"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Yenilənmə Tarixi"
    )

    class Meta:
        verbose_name = "Stok Qeyd"
        verbose_name_plural = "Stok Qeydləri"

    def __str__(self):
        return f"{self.inventory_item.name} - {self.quantity} {self.inventory_item.unit}"
