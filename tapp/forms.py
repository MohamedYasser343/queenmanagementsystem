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
    class Meta:
        model = Storage
        fields = ['name', 'price', 'quantity']
        labels = {
            'name': 'الاسم',
            'price': 'السعر',
            'quantity': 'الكمية',
        }

class SelledItemsForm(forms.ModelForm):
    class Meta:
        model = SelledItems
        fields = ['item', 'quantity']
        labels = {
            'item': 'الاسم',
            'quantity': 'الكمية',
        }
