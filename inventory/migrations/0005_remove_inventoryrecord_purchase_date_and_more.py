# Generated by Django 4.2.15 on 2025-03-12 09:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0004_alter_inventoryrecord_reason"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="inventoryrecord",
            name="purchase_date",
        ),
        migrations.AddField(
            model_name="inventoryrecord",
            name="operation_date",
            field=models.DateField(
                default=django.utils.timezone.now,
                help_text="Bu, əməliyyatın baş verdiyi tarixi göstərir. Əgər bir məhsulu alıb sistemə gec (məsələn, 3 gün sonra) daxil edirsinizsə, məhz alışın həqiqi baş verdiyi tarixi seçməlisiniz. Bu, inventarın düzgün izlənməsinə və hesabatların dəqiq olmasına kömək edəcək. \n\n\n            **Alış üçün nümunə:** Əgər bir məhsulu bazar ertəsi alıb, lakin cümə axşamı sistemə daxil edirsinizsə, tarixi bazar ertəsi olaraq qeyd edin. \n\n\n            **Silinmə üçün nümunə:** Bir məhsul bazar günü istifadəyə yararsız olubsa, lakin siz bu məlumatı çərşənbə axşamı sistemə daxil edirsinizsə, tarixi bazar günü kimi qeyd etməlisiniz. \n\n\n            **Diqqət:** Əməliyyatın həqiqi tarixini qeyd etmədikdə, hesabatlarda yanlış məlumatlar yaranacaq və inventar idarəçiliyində problemlər baş verə bilər.",
                verbose_name="Tarix",
            ),
        ),
    ]
