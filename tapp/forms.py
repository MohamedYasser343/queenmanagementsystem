from django import forms
from .models import CVs, Customers, SelledItems, Storage, Writing, Copying, Entry, Deliveries

class CVsForm(forms.ModelForm):
    class Meta:
        model = CVs
        exclude = ('name', 'rest_money')
        labels = {
            'recipient_name': 'اسم المستلم',
            'price': 'السعر',
            'paid_money': 'المبلغ المدفوع',
            'status': 'الحالة',
            'file': 'الملف',
            'language': 'اللغة',
            'delivered_time' : 'وقت التسليم',
        }
        widgets = {
            'status': forms.Select(choices=Deliveries.STATUS_CHOICES),
            'file': forms.ClearableFileInput(),
            'delivered_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        file = cleaned_data.get('file')

        if (status == 'اتعمل' or status == 'اتسلم') and not file:
            self.add_error('file', 'إرفع الشغل طالما خلصته')

class WritingForm(forms.ModelForm):
    class Meta:
        model = Writing
        exclude = ('name', 'rest_money')
        labels = {
            'recipient_name': 'اسم المستلم',
            'price': 'السعر',
            'paid_money': 'المبلغ المدفوع',
            'status': 'الحالة',
            'file': 'الملف',
            'paper_number': 'عدد الورق',
            'delivered_time' : 'وقت التسليم',
        }
        widgets = {
            'status': forms.Select(choices=Deliveries.STATUS_CHOICES),
            'file': forms.ClearableFileInput(),
            'delivered_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        file = cleaned_data.get('file')

        if (status == 'اتعمل' or status == 'اتسلم') and not file:
            self.add_error('file', 'إرفع الشغل طالما خلصته')

class CopyingForm(forms.ModelForm):
    class Meta:
        model = Copying
        exclude = ('name', 'rest_money', 'file')
        labels = {
            'recipient_name': 'اسم المستلم',
            'price': 'السعر',
            'paid_money': 'المبلغ المدفوع',
            'status': 'الحالة',
            'paper_number': 'عدد الورق',
            'delivered_time' : 'وقت التسليم',
        }
        widgets = {
            'status': forms.Select(choices=Deliveries.STATUS_CHOICES),
            'file': forms.ClearableFileInput(),
            'delivered_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['customer', 'service', 'face_type', 'color', 'storage_items', 'number', 'price', 'comment',]
        labels = {
            'customer': 'العميل',
            'service': 'الخدمة',
            'face_type': 'نوع الوش',
            'color': 'اللون',
            'storage_items': 'المخزن',
            'number': 'العدد',
            'price': 'السعر',
            'comment': 'تعليق',
        }

    def clean(self):
        cleaned_data = super().clean()
        service = cleaned_data.get('service')
        face_type = cleaned_data.get('face_type')
        color = cleaned_data.get('color')
        number = cleaned_data.get('number')
        price = cleaned_data.get('price')
        comment = cleaned_data.get('comment')

        if service in ['طباعة', 'تصوير']:
            if not all([face_type, color]):
                raise forms.ValidationError('نوع الوش واللون لازم يتكتبوا')
            if number is None:
                raise forms.ValidationError('عدد الورق لازم يتكتب')
        
        elif service == 'سكان':
            if face_type or color:
                raise forms.ValidationError('متكتبش نوع الوش واللون مع السكان')
            if number is None:
                raise forms.ValidationError('دخل عدد الورق الي معمول ليه سكان')
        
        elif service == 'تقديم':
            if face_type or color or number:
                raise forms.ValidationError('متدخلش عدد الورق ولا لونه ولا نوع الوش مع التقديم')
            
        elif service == 'بضاعة':
            if face_type or color or price:
                raise forms.ValidationError('متدخلش حاجة غير العدد بس')
            if number is None:
                raise forms.ValidationError('دخل العدد')
            
        elif service == 'أخرى':
            if not comment:
                raise forms.ValidationError('اكتب الخدمة في جزء التعليق')
        return cleaned_data

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = ['name', 'phone']
        labels = {
            'name': 'الاسم',
            'phone': 'رقم الهاتف',
        }

class StorageForm(forms.ModelForm):
    """
    Form for adding or editing storage items.
    """
    class Meta:
        model = Storage
        fields = ['name', 'price', 'quantity']
        labels = {
            'name': 'الاسم',
            'price': 'السعر',
            'quantity': 'الكمية',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'أدخل اسم العنصر'}),
            'price': forms.NumberInput(attrs={'placeholder': 'أدخل السعر'}),
            'quantity': forms.NumberInput(attrs={'placeholder': 'أدخل الكمية'}),
        }

    def clean_quantity(self):
        """
        Ensure quantity is not negative.
        """
        quantity = self.cleaned_data.get('quantity')
        if quantity < 0:
            raise forms.ValidationError("الكمية لا يمكن أن تكون سلبية.")
        return quantity

    def clean_price(self):
        """
        Ensure price is not negative or zero.
        """
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("السعر يجب أن يكون أكبر من الصفر.")
        return price


class SelledItemsForm(forms.ModelForm):
    """
    Form for adding sold items.
    """
    class Meta:
        model = SelledItems
        fields = ['item', 'quantity']
        labels = {
            'item': 'الاسم',
            'quantity': 'الكمية',
        }
        widgets = {
            'item': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'placeholder': 'أدخل الكمية المباعة'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit item choices to those with stock available
        self.fields['item'].queryset = Storage.objects.filter(quantity__gt=0)

    def clean_quantity(self):
        """
        Ensure the sold quantity is valid and doesn't exceed available stock.
        """
        quantity = self.cleaned_data.get('quantity')
        item = self.cleaned_data.get('item')

        if quantity <= 0:
            raise forms.ValidationError("الكمية يجب أن تكون أكبر من الصفر.")
        
        if item and quantity > item.quantity:
            raise forms.ValidationError(
                f"الكمية المطلوبة ({quantity}) أكبر من المتوفر ({item.quantity})."
            )
        return quantity
