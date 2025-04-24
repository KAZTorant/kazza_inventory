from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.db.models import Sum
from django import forms

from inventory.models import InventoryItem
from inventory.models import InventoryRecord


class InventoryItemAdmin(admin.ModelAdmin):
    change_form_template = "admin/inventory/inventory_item_change_form.html"

    list_display = (
        'name',
        'supplier',
        'category',
        'total_quantity',
        # 'total_money_spent',
        'action_buttons'
    )
    list_filter = ('category',)
    ordering = ('category', 'name')
    readonly_fields = ('latest_added_time', 'latest_removed_time')

    def total_quantity(self, obj):
        added = obj.stock_records.filter(record_type='add').aggregate(total=Sum('quantity'))['total'] or 0
        removed = obj.stock_records.filter(record_type='remove').aggregate(total=Sum('quantity'))['total'] or 0
        net_total = added - removed
        return f"{round(net_total, 3)} {obj.unit}"

    total_quantity.short_description = "Miqdar"

    # def total_money_spent(self, obj):
    #     total_price = obj.stock_records.aggregate(total=Sum('price'))['total'] or 0
    #     return f"{total_price} ₼"
    # total_money_spent.short_description = "Xərclər"

    def latest_added_time(self, obj):
        latest_record = obj.stock_records.filter(
            record_type='add').order_by('-created_at').first()
        if latest_record:
            return latest_record.created_at.strftime("%Y-%m-%d %H:%M:%S")
        return "-"
    latest_added_time.short_description = "Son Əlavə"

    def latest_removed_time(self, obj):
        latest_record = obj.stock_records.filter(
            record_type='remove').order_by('-created_at').first()
        if latest_record:
            return latest_record.created_at.strftime("%Y-%m-%d %H:%M:%S")
        return "-"
    latest_removed_time.short_description = "Son Silinmə"

    def action_buttons(self, obj):
        add_url = reverse('admin:inventory_inventoryrecord_add') + \
            f"?inventory_item={obj.pk}&record_type=add"
        remove_url = reverse('admin:inventory_inventoryrecord_add') + \
            f"?inventory_item={obj.pk}&record_type=remove"
        return format_html(
            '<button type="button" class="button" style="padding: 5px 10px; background-color: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer; margin-right: 5px;" onclick="window.location.href=\'{}\'">Əlavə et</button>'
            '<button type="button" class="button" style="padding: 5px 10px; background-color: #f44336; color: white; border: none; border-radius: 4px; cursor: pointer;" onclick="window.location.href=\'{}\'">Silinmə</button>',
            add_url,
            remove_url
        )
    action_buttons.short_description = "Əməliyyatlar"
    

class InventoryRecordForm(forms.ModelForm):
    inventory_unit = forms.CharField(
        label="Vahid", 
        disabled=True,
        required=False
    )
    record_type = forms.ChoiceField(
        choices=InventoryRecord.RECORD_TYPE_CHOICES,
        label="Əməliyyat növü"
    )
    reason = forms.ChoiceField(
        label="Səbəb",
        choices=InventoryRecord.REASON_CHOICES,
        required=False
    )

    class Meta:
        model = InventoryRecord
        fields = (
            'inventory_item',
            'inventory_unit',
            'record_type',
            'reason',
            'quantity',
            'operation_date',
            'expiration_date'
        )

    ADD_REASON_CHOICES = InventoryRecord.REASON_CHOICES_ADD

    REMOVE_REASON_CHOICES = InventoryRecord.REASON_CHOICES_REMOVE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "record_type" not in self.initial:
            return

        inventory_item_id = 0

        # Prefill inventory_unit based on the selected InventoryItem.
        if self.instance and self.instance.pk and self.instance.inventory_item:
            inventory_item_id = self.instance.inventory_item.pk
        elif 'inventory_item' in self.initial:
            inventory_item_id = self.initial['inventory_item']

        inventory_items = InventoryItem.objects.filter(pk=inventory_item_id)
        
        if inventory_items.exists():
            self.fields['inventory_unit'].initial = inventory_items.first().get_unit_display()
            self.fields['inventory_item'].queryset = inventory_items
            self.fields['inventory_item'].empty_label = None

        # Determine current record_type from POST data or initial values.
        record_type = ( self.data.get('record_type') or self.initial.get('record_type'))

        # Set reason choices based on record_type.
        if record_type == 'add':
            self.fields['reason'].choices = self.ADD_REASON_CHOICES
            self.fields['record_type'].choices = [InventoryRecord.RECORD_TYPE_CHOICES[0]]
        elif record_type == 'remove':
            self.fields['reason'].choices = self.REMOVE_REASON_CHOICES
            self.fields['record_type'].choices = [InventoryRecord.RECORD_TYPE_CHOICES[1]]


class InventoryRecordAdmin(admin.ModelAdmin):
    form = InventoryRecordForm
    fields = (
        'inventory_item',
        'inventory_unit',
        'record_type',
        'reason',
        'quantity',
        'price',
        'operation_date',
        'expiration_date'
    )

    list_display = ('inventory_item', 'record_type', 'reason', 'quantity_with_unit','price', 'operation_date')
    list_filter = ('inventory_item', 'record_type', 'operation_date', )
    list_per_page = 100 

    def quantity_with_unit(self, obj) -> str:
        return f"{obj.quantity} {obj.inventory_item.unit}"

    quantity_with_unit.short_description = "Miqdar"

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        if 'inventory_item' in request.GET:
            initial['inventory_item'] = request.GET.get('inventory_item')

        if 'record_type' in request.GET:
            initial['record_type'] = request.GET.get('record_type')
        return initial

    def response_add(self, request, obj, post_url_continue=None):
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(reverse('admin:inventory_inventoryitem_changelist'))


admin.site.register(InventoryItem, InventoryItemAdmin)
admin.site.register(InventoryRecord, InventoryRecordAdmin)
