from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError

from queenBackend import settings

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('normal', 'Normal'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='normal')
    points = models.IntegerField(default=0)
    arabic_name = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return self.username
    
class Entry(models.Model):
    SERVICE_CHOICES = [
        ('طباعة', 'طباعة'),
        ('تصوير', 'تصوير'),
        ('سكان', 'سكان'),
        ('تقديم', 'تقديم'),
        ('بضاعة', 'بضاعة'),
        ('أخرى', 'أخرى'),
    ]
    FACE_TYPE_CHOICES = [
        ('وش واحد', 'وش وحد'),
        ('وشين', 'وشين'),
    ]

    COLOR_CHOICES = [
        ('أسود', 'أسود'),
        ('الوان', 'الوان'),
    ]

    name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.CharField(max_length=10, choices=SERVICE_CHOICES)
    face_type = models.CharField(max_length=50, choices=FACE_TYPE_CHOICES, blank=True, null=True)
    color = models.CharField(max_length=50, choices=COLOR_CHOICES, blank=True, null=True)
    storage_items = models.ForeignKey('Storage', on_delete=models.CASCADE, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    comment = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField()
    customer = models.ForeignKey('Customers', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.service}"

    def formatted_timestamp(self):
        # Localized formatting
        return self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    
    def save(self, *args, **kwargs):
        service_points = {
            'طباعة': 1,     # Printing
            'تصوير': 2,     # Copying
            'سكان': 3,      # Scanning
            'تقديم': 5,     # Submission
            'بضاعة': 1,     # Storage
            'أخرى': 2       # Other
        }
        self.points = service_points.get(self.service, 0)
        super().save(*args, **kwargs)

# Abstract model
class Deliveries(models.Model):
    STATUS_CHOICES = (
        ('متعملش', 'متعملش'),
        ('اتعمل', 'اتعمل'),
        ('اتسلم', 'اتسلم'),
    )

    name = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    recipient_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    paid_money = models.DecimalField(max_digits=10, decimal_places=2)
    rest_money = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    delivered_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='متعملش')
    file = models.FileField(upload_to='deliveries/', blank=True, null=True)
    points = models.IntegerField()


    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.rest_money = self.price - self.paid_money
        super().save(*args, **kwargs)

    def formatted_timestamp(self):
        # Localized formatting
        return self.timestamp.strftime('%Y-%m-%d %H:%M:%S')

class CVs(Deliveries):
    LANG_CHOICES = (
        ('عربي', 'عربي'),
        ('إنجلش', 'إنجلش'),
    )
    language = models.CharField(max_length=100, choices=LANG_CHOICES)

class Writing(Deliveries):
    paper_number = models.IntegerField()

class Copying(Deliveries):
    paper_number = models.IntegerField()

class Customers(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Storage(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Item Name")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Unit Price")
    quantity = models.IntegerField(default=0, verbose_name="Quantity in Stock")

    def __str__(self):
        return f"{self.name} (Stock: {self.quantity})"

    def clean(self):
        if self.price < 0:
            raise ValidationError("Price cannot be negative.")
        if self.quantity < 0:
            raise ValidationError("Quantity cannot be negative.")

    def total_value(self):
        """
        Calculates the total value of the items in stock.
        """
        return self.price * self.quantity

    class Meta:
        verbose_name = "Storage Item"
        verbose_name_plural = "Storage Items"
        ordering = ['name']


class SelledItems(models.Model):
    item = models.ForeignKey(Storage, on_delete=models.CASCADE, related_name="sales", verbose_name="Sold Item")
    quantity = models.IntegerField(default=0, verbose_name="Quantity Sold")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Price")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Sale Timestamp")

    def __str__(self):
        return f"Sold {self.quantity} of {self.item.name} on {self.timestamp.strftime('%Y-%m-%d')}"

    def clean(self):
        if self.quantity < 0:
            raise ValidationError("Quantity sold cannot be negative.")
        if self.price is not None and self.price < 0:
            raise ValidationError("Total price cannot be negative.")
        if self.item and self.quantity > self.item.quantity:
            raise ValidationError(f"Insufficient stock for item '{self.item.name}'. Available: {self.item.quantity}, Requested: {self.quantity}.")

    def save(self, *args, **kwargs):
        """
        Override save method to reduce stock in Storage upon successful sale.
        """
        if not self.pk:  # Only reduce stock on creation
            self.item.quantity -= self.quantity
            self.item.full_clean()  # Revalidate item to ensure stock doesn't go negative
            self.item.save()
        super().save(*args, **kwargs)

    def formatted_timestamp(self):
        """
        Localized formatting for timestamp.
        """
        return self.timestamp.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        verbose_name = "Sold Item"
        verbose_name_plural = "Sold Items"
        ordering = ['-timestamp']
