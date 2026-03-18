from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Game, Product, Transaction


class ProductinLine(admin.TabularInline):
    model = Product
    extra = 1
@admin.register(Game)
class GameAdmin(ModelAdmin): 
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductinLine]


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ('name', 'game', 'price', 'is_active')

@admin.register(Transaction)
class TransactionAdmin(ModelAdmin):
    list_display = ('transaction_id', 'player_id', 'status', 'created_at')
    list_filter = ('status',)   