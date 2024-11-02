from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Methodology, MethodologySupply
from .forms import MethodologyForm, MethodologySupplyForm
from .filters import MethodologyFilter

# ====== Methodology Views ======

@login_required
@permission_required('methodologies.can_view_methodology', raise_exception=True)
def methodology_list(request):
    """
    Display a list of all methodologies with filter functionality.
    """
    methodologies = Methodology.objects.all()
    
    # Apply filters
    methodology_filter = MethodologyFilter(request.GET, queryset=methodologies)
    methodologies = methodology_filter.qs

    return render(request, 'methodologies/methodology_list.html', {
        'methodologies': methodologies,
        'filter': methodology_filter,
    })


@login_required
@permission_required('methodologies.can_add_methodology', raise_exception=True)
def methodology_create(request):
    """
    Handle the creation of a new methodology.
    """
    if request.method == 'POST':
        form = MethodologyForm(request.POST)
        if form.is_valid():
            methodology = form.save()
            messages.success(request, "Methodology created successfully!")
            return redirect('methodology_edit', pk=methodology.pk)
    else:
        form = MethodologyForm()

    return render(request, 'methodologies/methodology_form.html', {
        'form': form,
        'title': 'Create Methodology',
        'button_label': 'Save'
    })


@login_required
@permission_required('methodologies.can_view_methodology', raise_exception=True)
def methodology_edit_or_view(request, pk):
    """
    Handle viewing or editing a methodology. If the user has the permission to edit, the form will be editable.
    Otherwise, the form will be displayed in a read-only mode.
    """
    methodology = get_object_or_404(Methodology, pk=pk)
    can_edit = request.user.has_perm('methodologies.can_change_methodology')

    if request.method == 'POST' and can_edit:
        form = MethodologyForm(request.POST, instance=methodology)
        if form.is_valid():
            form.save()
            messages.success(request, "Methodology updated successfully!")
            return redirect('methodology_edit', pk=methodology.pk)
    else:
        form = MethodologyForm(instance=methodology)

    # Supply form to add new supplies dynamically
    supply_form = MethodologySupplyForm()

    # List of existing supplies
    supplies = MethodologySupply.objects.filter(methodology=methodology)

    return render(request, 'methodologies/methodology_form.html', {
        'form': form,
        'supply_form': supply_form,
        'supplies': supplies,
        'methodology': methodology,
        'can_edit': can_edit,
        'title': 'View/Edit Methodology',
        'button_label': 'Update' if can_edit else 'View'
    })


@login_required
@permission_required('methodologies.can_delete_methodology', raise_exception=True)
def methodology_delete(request, pk):
    """
    Handle the deletion of an existing methodology.
    """
    methodology = get_object_or_404(Methodology, pk=pk)
    if request.method == 'POST':
        methodology.delete()
        messages.success(request, "Methodology deleted successfully!")
        return redirect('methodology_list')
    return render(request, 'confirm_delete.html', {
        'item_name': methodology.title,
        'delete_url': request.path,
        'cancel_url': 'methodology_list'
    })

# ====== AJAX Views for MethodologySupply ======

@login_required
@permission_required('methodologies.can_change_methodology', raise_exception=True)
def methodology_supply_add(request, pk):
    """
    Handle the addition of a new supply via AJAX.
    """
    methodology = get_object_or_404(Methodology, pk=pk)
    if request.method == 'POST':
        supply_form = MethodologySupplyForm(request.POST)
        if supply_form.is_valid():
            supply = supply_form.save(commit=False)
            supply.methodology = methodology
            supply.save()
            supplies = MethodologySupply.objects.filter(methodology=methodology)
            # Return updated supply list as HTML
            html = render_to_string('methodologies/partial_supply_list.html', {'supplies': supplies, 'can_edit': True})
            return JsonResponse({'success': True, 'html': html})

    return JsonResponse({'success': False})


@login_required
@permission_required('methodologies.can_change_methodology', raise_exception=True)
def methodology_supply_delete(request, pk):
    """
    Handle the deletion of a supply via AJAX without confirmation.
    """
    supply = get_object_or_404(MethodologySupply, pk=pk)
    methodology = supply.methodology
    supply.delete()
    supplies = MethodologySupply.objects.filter(methodology=methodology)
    # Return updated supply list as HTML
    html = render_to_string('methodologies/partial_supply_list.html', {'supplies': supplies, 'can_edit': True})
    return JsonResponse({'success': True, 'html': html})
