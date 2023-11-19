from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.messages import error, success
from .models import Category, Expense

# Create your views here.
@login_required(login_url = '/authentication/login')
def index(request):
    expenses = Expense.objects.filter(owner = request.user)
    context = {
        'expenses': expenses,
    }
    
    return render(request, 'expenses/index.html', context = context)

def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST,
    }
    
    if request.method == 'POST':
        amount = float(request.POST["amount"])
        if not amount:
            error(request, 'Amount is required')
            
        description = request.POST["description"]
        if not description:
            error(request, 'Description is required')
            
        category = request.POST["category"]
        date = request.POST["expense_date"]
        
        Expense.objects.create(owner = request.user, amount = amount, description = description, category = category, date = date)
        success(request, 'Expense saved successfully!!!')
        
        return redirect("expenses")
    
    return render(request, 'expenses/add_expense.html', context = context)