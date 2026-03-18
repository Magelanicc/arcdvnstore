from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction, Game, Product
from .forms import TransactionForm, GameForm, ProductForm
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.http import JsonResponse
import uuid
import random

# --- USER VIEWS ---

def home_user(request):
    games = Game.objects.all()
    return render(request, 'home.html', {'games': games})

def game_detail(request, slug):
    game = get_object_or_404(Game, slug=slug)
    products = Product.objects.filter(game=game, is_active=True)
    
    if request.method == 'POST':  
        player_id = request.POST.get('player_id')
        zone_id = request.POST.get('zone_id')
        product_id = request.POST.get('product')
        wa = request.POST.get('whatsapp')
        
        selected_product = get_object_or_404(Product, id=product_id)
        
        now = timezone.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")[:12]

        invoice = f"ARCDVN-{timestamp}"
        

        new_tx = Transaction.objects.create(
            game_name=game.name,
            invoice_id=invoice,
            transaction_id=invoice,
            product=selected_product,
            player_id=player_id,
            zone_id=zone_id,
            whatsapp_number=wa,
            total_price=selected_product.price,
            status='PENDING'
        )
        
        return render(request, 'success_order.html', {'tx': new_tx})

    return render(request, 'checkout.html', {'game': game, 'products': products})

def api_check_payment(request, invoice_id):
    tx = get_object_or_404(Transaction, invoice_id=invoice_id)

    if tx.status == 'PENDING':
        tx.status = 'SUCCESS'
        tx.save()
    return JsonResponse({'status': tx.status})

# --- ADMIN VIEWS ---

@login_required(login_url='login-admin')
def admin_dashboard(request):
    games = Game.objects.all()
    products_list = Product.objects.all()
    transactions_list = Transaction.objects.all().order_by('-created_at')[:10]
    now = timezone.now()

    game_form = GameForm()
    product_form = ProductForm()

    if request.method == 'POST':
        if 'add_game' in request.POST:
            game_form = GameForm(request.POST, request.FILES)
            if game_form.is_valid():
                game_form.save()
                return redirect('admin-dashboard')
        elif 'add_product' in request.POST:
            product_form = ProductForm(request.POST)
            if product_form.is_valid():
                product_form.save()
                return redirect('admin-dashboard')

    # Statistik untuk Dashboard
    total_rev = Transaction.objects.filter(status='SUCCESS').aggregate(Sum('total_price'))['total_price__sum'] or 0
    pending_count = Transaction.objects.filter(status='PENDING').count()
    total_transaksi = Transaction.objects.count()

    context = {
        'games': games,
        'products': products_list,
        'NewTransactions': transactions_list,
        'total_transaksi': total_transaksi,
        'totalRevenue': total_rev,
        'pendingCount': pending_count,
        'game_form': game_form,
        'product_form': product_form
    }
    return render(request, 'admin_kece.html', context)

@login_required(login_url='login-admin')
def delete_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    game.delete()
    messages.success(request, f'Game "{game.name}" berhasil dihapus.')
    return redirect('admin-dashboard')

@csrf_protect
def login_admin(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect('admin-dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

def logout_admin(request):
    logout(request)
    return redirect('login-admin')