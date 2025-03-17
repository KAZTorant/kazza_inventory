from django.db import models
from django.utils.timezone import now

from inventory.models.category import Category
from inventory.models.supplier import Supplier


class InventoryItem(models.Model):
    UNIT_CHOICES = (
        ('kg', 'Kilogram'),
        ('l', 'Litr'),
        ('pcs', 'Ədəd'),
        ('package', 'Bağlama')
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
        if self.supplier:
            return f"{self.name} ({self.supplier or ''})"
        return f"{self.name or 'Adsız Məhsul'}"
    
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
    RECORD_TYPE_CHOICES = (
        ('add', 'Əlavə'),
        ('remove', 'Silinmə')
    )
    record_type = models.CharField(
        max_length=16,
        choices=RECORD_TYPE_CHOICES,
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
        ('sold', 'Satılmış'),
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
    price = models.FloatField(
            verbose_name="Qiymət",
            default=0
        )

    operation_date = models.DateField(
        verbose_name="Tarix",
         help_text=(
            "<strong>Əməliyyatın həqiqi baş verdiyi tarixi seçin.</strong><br><br>"

            "<strong>📌 Alış üçün nümunə:</strong><br>"
            "Məhsulu <strong>3 gün əvvəl</strong> almışsınız, lakin <strong>bu gün</strong> sistemə əlavə edirsiniz. "
            "Bu halda, məhz <strong>3 gün əvvəlki tarixi</strong> (yəni alışın baş verdiyi günü) seçməlisiniz.<br><br>"

            "<strong>🚨 Silinmə üçün nümunə:</strong><br>"
            "Məhsul <strong>4 gün əvvəl</strong> istifadəyə yararsız olub, lakin siz onu <strong>bu gün</strong> sistemə daxil edirsiniz. "
            "Tarixi düzgün göstərmək üçün <strong>4 gün əvvəlki tarixi</strong> qeyd edin.<br><br>"

            "<em>Əgər bu qaydalara əməl etməsəniz, inventar məlumatları səhv ola bilər və hesabatlar yanlış nəticə verə bilər.</em>"
            "<hr>"
        ),
        default=now,
    )

    expiration_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Son İstifadə Tarixi",
        help_text="Məhsulun son istifadə tarixini varsa, burada qeyd edin ki, nə vaxt istifadəyə yararsız olacağını izləyə biləsiniz."
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
