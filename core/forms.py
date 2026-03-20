from django import forms
from .models import Transaction
from .models import Game, Product

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['invoice_id', 'game_name', 'total_price', 'status']
        widgets = {
            'invoice_id': forms.TextInput(attrs={'class': 'w-full p-2 rounded bg-gray-700 border-none text-white'}),
            'game_name': forms.TextInput(attrs={'class': 'w-full p-2 rounded bg-gray-700 border-none text-white'}),
            'total_price': forms.NumberInput(attrs={'class': 'w-full p-2 rounded bg-gray-700 border-none text-white'}),
            'status': forms.Select(attrs={'class': 'w-full p-2 rounded bg-gray-700 border-none text-white'}),
        }

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'slug', 'icon', 'category'] # Tambahin category
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full bg-slate-900 border border-slate-700 p-3 rounded-xl text-white'}),
            'slug': forms.TextInput(attrs={'class': 'w-full bg-slate-900 border border-slate-700 p-3 rounded-xl text-white'}),
            'icon': forms.FileInput(attrs={'class': 'w-full text-slate-400'}),
            'category': forms.Select(attrs={'class': 'w-full bg-slate-900 border border-slate-700 p-3 rounded-xl text-white'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['game', 'name', 'price', 'is_active']
        widgets = {
            'game': forms.Select(attrs={'class': 'w-full bg-slate-900 border border-slate-700 p-3 rounded-xl text-white'}),
            'name': forms.TextInput(attrs={'class': 'w-full bg-slate-900 border border-slate-700 p-3 rounded-xl text-white'}),
            'price': forms.NumberInput(attrs={'class': 'w-full bg-slate-900 border border-slate-700 p-3 rounded-xl text-white'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox h-5 w-5 text-blue-600'}),
        }