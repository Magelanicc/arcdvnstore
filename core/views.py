from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction, Game, Product
from .forms import TransactionForm, GameForm, ProductForm
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models.functions import TruncDate
import uuid
import random

# --- USER VIEWS ---

def home_user(request):
    games = Game.objects.filter(category='GAME')
    pulsas = Game.objects.filter(category='PULSA')
    ewallets = Game.objects.filter(category='EWALLET')
    
    return render(request, 'home.html', {
        'games': games,
        'pulsas': pulsas,
        'ewallets': ewallets
    })

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
    

    # LOGIKA GRAFIK PENJUALAN 7 HARI TERAKHIR
    hari_ini = timezone.now().date()
    tujuh_hari_lalu = hari_ini - timedelta(days=6)

    # Ambil data transaksi sukses
    sales_data = Transaction.objects.filter(
        status='SUCCESS', 
        created_at__date__range=[tujuh_hari_lalu, hari_ini] 
    ).annotate(date=TruncDate('created_at')) \
     .values('date') \
     .annotate(total=Sum('total_price')) \
     .order_by('date')

    
    sales_dict = {item['date']: float(item['total']) for item in sales_data}
    
    chart_labels = []
    chart_values = []
    
    for i in range(7):
        tgl = tujuh_hari_lalu + timedelta(days=i)
        chart_labels.append(tgl.strftime('%d %b'))
        chart_values.append(sales_dict.get(tgl, 0)) 

    # LOGIKA DOUGHNUT CHART (Game Terpopuler)
    top_games = Transaction.objects.filter(status='SUCCESS') \
        .values('game_name') \
        .annotate(count=Count('id')) \
        .order_by('-count')[:5]
    
    game_labels = [item['game_name'] for item in top_games]
    game_counts = [item['count'] for item in top_games]

    context = {
        'total_transaksi': Transaction.objects.count(),
        'totalRevenue': Transaction.objects.filter(status='SUCCESS').aggregate(Sum('total_price'))['total_price__sum'] or 0,
        'game_count': Game.objects.count(),
        'chart_labels': chart_labels,
        'chart_values': chart_values,
        'game_labels': game_labels,
        'game_counts': game_counts,
        'recent_transactions': Transaction.objects.all().order_by('-created_at')[:3],
    }
    return render(request, 'admin_kece.html', context)

@login_required(login_url='login-admin')
def admin_manage_games(request):
    
    games = Game.objects.all()
    products_list = Product.objects.all()
    
    game_form = GameForm()
    product_form = ProductForm()

    if request.method == 'POST':
        if 'add_game' in request.POST:
            game_form = GameForm(request.POST, request.FILES)
            if game_form.is_valid():
                game_form.save()
                return redirect('admin-games') 
        elif 'add_product' in request.POST:
            product_form = ProductForm(request.POST)
            if product_form.is_valid():
                product_form.save()
                return redirect('admin-games') 

    context = {
        'games': games,
        'products': products_list,
        'game_form': game_form,
        'product_form': product_form
    }
    return render(request, 'admin_games.html', context)

@login_required(login_url='login-admin')
def admin_transactions(request):
    
    transactions_list = Transaction.objects.all().order_by('-created_at')
    return render(request, 'admin_transactions.html', {'transactions': transactions_list})

@login_required(login_url='login-admin')
def delete_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    game.delete()
    messages.success(request, f'Game "{game.name}" berhasil dihapus.')
    return redirect('admin-games') 

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