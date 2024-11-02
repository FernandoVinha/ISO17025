# admin.py
from django.contrib import admin
from .models import Methodology, MethodologySupply

class MethodologySupplyInline(admin.TabularInline):
    model = MethodologySupply
    extra = 1  # Número de formulários extras para adicionar novos insumos

@admin.register(Methodology)
class MethodologyAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')  # Campos exibidos na lista
    search_fields = ('title', 'author__first_name', 'author__last_name')  # Campos de busca
    list_filter = ('author',)  # Filtros na barra lateral
    inlines = [MethodologySupplyInline]  # Adiciona os insumos diretamente na página da metodologia

@admin.register(MethodologySupply)
class MethodologySupplyAdmin(admin.ModelAdmin):
    list_display = ('methodology', 'supply', 'quantity', 'unit')  # Campos exibidos na lista
   
