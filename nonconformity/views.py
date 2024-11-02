# nonconformity/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import NonConformityForm
from .models import NonConformity

# ====== View para Criar Não Conformidade ======
@login_required
def create_nonconformity(request):
    """
    View para permitir a criação de uma nova não conformidade.
    O usuário logado será automaticamente associado como o criador.
    """
    if request.method == 'POST':
        form = NonConformityForm(request.POST, request.FILES)
        if form.is_valid():
            nonconformity = form.save(commit=False)
            nonconformity.created_by = request.user  # Associa o usuário logado como criador
            nonconformity.save()
            messages.success(request, "Non-conformity report created successfully!")
            return redirect('nonconformity_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = NonConformityForm()

    return render(request, 'nonconformity/nonconformity_form.html', {'form': form})

# ====== View para Listar Não Conformidades ======
@login_required
def nonconformity_list(request):
    """
    View para listar todas as não conformidades criadas.
    """
    nonconformities = NonConformity.objects.all()
    return render(request, 'nonconformity/nonconformity_list.html', {'nonconformities': nonconformities})

# ====== View para Excluir Não Conformidade ======
@login_required
def delete_nonconformity(request, pk):
    """
    View para permitir que o criador da não conformidade a exclua.
    Apenas o usuário que criou pode realizar a exclusão.
    """
    nonconformity = get_object_or_404(NonConformity, pk=pk)
    
    # Verifica se o usuário logado é o criador da não conformidade
    if nonconformity.created_by != request.user:
        messages.error(request, "You are not authorized to delete this non-conformity.")
        return redirect('nonconformity_list')

    if request.method == 'POST':
        nonconformity.delete()
        messages.success(request, "Non-conformity deleted successfully!")
        return redirect('nonconformity_list')

    return render(request, 'nonconformity/nonconformity_confirm_delete.html', {'nonconformity': nonconformity})
