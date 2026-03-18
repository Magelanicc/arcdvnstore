from django.db import models

# Create your models here.
class Game(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.ImageField(upload_to='game_icons/')

    def __str__(self):
        return self.name
    
class Product(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.game.name} - {self.name}"

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Menunggu Pembayaran'),
        ('SUCCESS', 'Berhasil'),
        ('FAILED', 'Gagal'),
    ]

    game_name = models.CharField(max_length=100)
    invoice_id = models.CharField(max_length=100, unique=True)
    transaction_id = models.CharField(max_length=100, unique=True, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    player_id = models.CharField(max_length=50)
    zone_id = models.CharField(max_length=50, blank=True, null=True)
    whatsapp_number = models.CharField(max_length=20)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_id} - {self.player_id}"