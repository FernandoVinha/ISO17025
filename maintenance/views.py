# maintenance/views.py

import logging
from datetime import datetime, timedelta, date
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import (
    MaintenanceForm, 
    CalibrationForm, 
    TrainingForm, 
    SOPForm, 
    CalibrationStandardForm, 
    DailyVerificationForm
)
from .filters import (
    MaintenanceFilter, 
    CalibrationFilter, 
    TrainingFilter, 
    SOPFilter, 
    CalibrationStandardFilter, 
    DailyVerificationFilter
)
from .models import (
    Maintenance, 
    Calibration, 
    Training, 
    StandardOperatingProcedure, 
    CalibrationStandard, 
    DailyVerification
)
from simple_history.utils import update_change_reason

# Configuração de logging
logger = logging.getLogger(__name__)

# ======= Função Auxiliar para Tratamento de Formulários =======
def handle_form(request, form_class, template_name, success_message, redirect_url, change_reason, instance=None):
    """
    Função auxiliar para processar formulários de criação e edição.
    """
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            try:
                with transaction.atomic():
                    obj = form.save()
                    update_change_reason(obj, change_reason)
                    messages.success(request, success_message)
                    return redirect(redirect_url)
            except Exception as e:
                logger.error(f"Erro ao salvar o formulário: {e}")
                messages.error(request, "Ocorreu um erro ao processar o formulário. Por favor, tente novamente.")
        else:
            messages.error(request, "Erro ao processar o formulário. Por favor, verifique os dados inseridos.")
    else:
        form = form_class(instance=instance)
    
    return render(request, template_name, {'form': form})

# ====== Views de Manutenção ======

@login_required
@permission_required('maintenance.can_view_maintenance', raise_exception=True)
def maintenance_list(request):
    """
    Exibe uma lista paginada de registros de manutenção com funcionalidade de filtro.
    """
    maintenance_records = Maintenance.objects.all()
    maintenance_filter = MaintenanceFilter(request.GET, queryset=maintenance_records)
    maintenance_records = maintenance_filter.qs.order_by('next_maintenance_date')

    paginator = Paginator(maintenance_records, 50)  # 50 itens por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'maintenance/maintenance_list.html', {
        'page_obj': page_obj,
        'filter': maintenance_filter,
    })

@login_required
@permission_required('maintenance.can_add_maintenance', raise_exception=True)
def maintenance_create(request):
    """
    Trata a criação de um novo registro de manutenção.
    O botão de exclusão não estará disponível nesta view.
    """
    return handle_form(
        request=request,
        form_class=MaintenanceForm,
        template_name='maintenance/maintenance_form.html',
        success_message='Registro de manutenção criado com sucesso!',
        redirect_url='maintenance:maintenance_list',
        change_reason=f"Manutenção adicionada por {request.user.get_full_name()}",
        instance=None
    )

@login_required
@permission_required('maintenance.can_change_maintenance', raise_exception=True)
def maintenance_edit(request, pk):
    """
    Trata a edição de um registro de manutenção existente.
    O botão de exclusão estará disponível nesta view.
    """
    maintenance = get_object_or_404(Maintenance, pk=pk)
    return handle_form(
        request=request,
        form_class=MaintenanceForm,
        template_name='maintenance/maintenance_form.html',
        success_message='Registro de manutenção atualizado com sucesso!',
        redirect_url='maintenance:maintenance_list',
        change_reason=f"Manutenção atualizada por {request.user.get_full_name()}",
        instance=maintenance
    )

@login_required
@permission_required('maintenance.can_delete_maintenance', raise_exception=True)
def maintenance_delete(request, pk):
    """
    Trata a exclusão de um registro de manutenção existente.
    """
    maintenance = get_object_or_404(Maintenance, pk=pk)
    if request.method == 'POST':
        try:
            with transaction.atomic():
                update_change_reason(maintenance, f"Manutenção deletada por {request.user.get_full_name()}")
                maintenance.delete()
                messages.success(request, "Registro de manutenção deletado com sucesso!")
                return redirect('maintenance:maintenance_list')
        except Exception as e:
            logger.error(f"Erro ao deletar manutenção: {e}")
            messages.error(request, "Ocorreu um erro ao deletar o registro de manutenção. Por favor, tente novamente.")
    return render(request, 'confirm_delete.html', {
        'item_name': maintenance.description or maintenance.item.name,
        'delete_url': reverse('maintenance:maintenance_delete', args=[maintenance.id]),
        'cancel_url': reverse('maintenance:maintenance_list'),
    })

# ====== Views de Calibração ======

@login_required
@permission_required('maintenance.can_view_calibration', raise_exception=True)
def calibration_list(request):
    """
    Exibe uma lista paginada de registros de calibração com funcionalidade de filtro.
    """
    calibration_records = Calibration.objects.all()
    calibration_filter = CalibrationFilter(request.GET, queryset=calibration_records)
    calibration_records = calibration_filter.qs.order_by('next_calibration_date')

    paginator = Paginator(calibration_records, 50)  # 50 itens por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'maintenance/calibration_list.html', {
        'calibration_records': page_obj,
        'filter': calibration_filter,
    })

@login_required
@permission_required('maintenance.can_add_calibration', raise_exception=True)
def calibration_create(request):
    """
    Trata a criação de um novo registro de calibração.
    """
    return handle_form(
        request=request,
        form_class=CalibrationForm,
        template_name='maintenance/calibration_form.html',
        success_message='Registro de calibração criado com sucesso!',
        redirect_url='maintenance:calibration_list',
        change_reason=f"Calibração adicionada por {request.user.get_full_name()}",
        instance=None
    )

@login_required
@permission_required('maintenance.can_change_calibration', raise_exception=True)
def calibration_edit(request, pk):
    """
    Trata a edição de um registro de calibração existente.
    """
    calibration = get_object_or_404(Calibration, pk=pk)
    return handle_form(
        request=request,
        form_class=CalibrationForm,
        template_name='maintenance/calibration_form.html',
        success_message='Registro de calibração atualizado com sucesso!',
        redirect_url='maintenance:calibration_list',
        change_reason=f"Calibração atualizada por {request.user.get_full_name()}",
        instance=calibration
    )

@login_required
@permission_required('maintenance.can_delete_calibration', raise_exception=True)
def calibration_delete(request, pk):
    """
    Trata a exclusão de um registro de calibração existente.
    """
    calibration = get_object_or_404(Calibration, pk=pk)
    if request.method == 'POST':
        try:
            with transaction.atomic():
                update_change_reason(calibration, f"Calibração deletada por {request.user.get_full_name()}")
                calibration.delete()
                messages.success(request, "Registro de calibração deletado com sucesso!")
                return redirect('maintenance:calibration_list')
        except Exception as e:
            logger.error(f"Erro ao deletar calibração: {e}")
            messages.error(request, "Ocorreu um erro ao deletar o registro de calibração. Por favor, tente novamente.")
    return render(request, 'confirm_delete.html', {
        'item_name': calibration.description or calibration.item.name,
        'delete_url': reverse('maintenance:calibration_delete', args=[calibration.id]),
        'cancel_url': reverse('maintenance:calibration_list'),
    })

# ====== Views de Treinamento ======

@login_required
@permission_required('maintenance.can_view_training', raise_exception=True)
def training_list(request):
    """
    Exibe uma lista paginada de registros de treinamento com funcionalidade de filtro.
    """
    training_records = Training.objects.all()
    training_filter = TrainingFilter(request.GET, queryset=training_records)
    training_records = training_filter.qs.order_by('-date_completed')

    paginator = Paginator(training_records, 50)  # 50 itens por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'maintenance/training_list.html', {
        'training_records': page_obj,
        'filter': training_filter,
    })

@login_required
@permission_required('maintenance.can_add_training', raise_exception=True)
def training_create(request):
    """
    Trata a criação de um novo registro de treinamento.
    """
    return handle_form(
        request=request,
        form_class=TrainingForm,
        template_name='maintenance/training_form.html',
        success_message='Registro de treinamento criado com sucesso!',
        redirect_url='maintenance:training_list',
        change_reason=f"Treinamento adicionado por {request.user.get_full_name()}",
        instance=None
    )

@login_required
@permission_required('maintenance.can_change_training', raise_exception=True)
def training_edit(request, pk):
    """
    Trata a edição de um registro de treinamento existente.
    """
    training = get_object_or_404(Training, pk=pk)
    return handle_form(
        request=request,
        form_class=TrainingForm,
        template_name='maintenance/training_form.html',
        success_message='Registro de treinamento atualizado com sucesso!',
        redirect_url='maintenance:training_list',
        change_reason=f"Treinamento atualizado por {request.user.get_full_name()}",
        instance=training
    )

@login_required
@permission_required('maintenance.can_delete_training', raise_exception=True)
def training_delete(request, pk):
    """
    Trata a exclusão de um registro de treinamento existente.
    """
    training = get_object_or_404(Training, pk=pk)
    if request.method == 'POST':
        try:
            with transaction.atomic():
                update_change_reason(training, f"Treinamento deletado por {request.user.get_full_name()}")
                training.delete()
                messages.success(request, "Registro de treinamento deletado com sucesso!")
                return redirect('maintenance:training_list')
        except Exception as e:
            logger.error(f"Erro ao deletar treinamento: {e}")
            messages.error(request, "Ocorreu um erro ao deletar o registro de treinamento. Por favor, tente novamente.")
    return render(request, 'confirm_delete.html', {
        'item_name': training.training_name,
        'delete_url': reverse('maintenance:training_delete', args=[training.id]),
        'cancel_url': reverse('maintenance:training_list'),
    })

# ====== Views de SOP (Standard Operating Procedure) ======

@login_required
@permission_required('maintenance.can_view_sop', raise_exception=True)
def sop_list(request):
    """
    Exibe uma lista paginada de SOPs com funcionalidade de filtro.
    """
    sop_records = StandardOperatingProcedure.objects.all()
    sop_filter = SOPFilter(request.GET, queryset=sop_records)
    sop_records = sop_filter.qs.order_by('title')

    paginator = Paginator(sop_records, 50)  # 50 itens por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'maintenance/sop_list.html', {
        'sop_records': page_obj,
        'filter': sop_filter,
    })

@login_required
@permission_required('maintenance.can_add_sop', raise_exception=True)
def sop_create(request):
    """
    Trata a criação de um novo SOP.
    """
    return handle_form(
        request=request,
        form_class=SOPForm,
        template_name='maintenance/sop_form.html',
        success_message='SOP criado com sucesso!',
        redirect_url='maintenance:sop_list',
        change_reason=f"SOP adicionado por {request.user.get_full_name()}",
        instance=None
    )

@login_required
@permission_required('maintenance.can_change_sop', raise_exception=True)
def sop_edit(request, pk):
    """
    Trata a edição de um SOP existente.
    """
    sop = get_object_or_404(StandardOperatingProcedure, pk=pk)
    return handle_form(
        request=request,
        form_class=SOPForm,
        template_name='maintenance/sop_form.html',
        success_message='SOP atualizado com sucesso!',
        redirect_url='maintenance:sop_list',
        change_reason=f"SOP atualizado por {request.user.get_full_name()}",
        instance=sop
    )

@login_required
@permission_required('maintenance.can_delete_sop', raise_exception=True)
def sop_delete(request, pk):
    """
    Trata a exclusão de um SOP existente.
    """
    sop = get_object_or_404(StandardOperatingProcedure, pk=pk)
    if request.method == 'POST':
        try:
            with transaction.atomic():
                update_change_reason(sop, f"SOP deletado por {request.user.get_full_name()}")
                sop.delete()
                messages.success(request, "SOP deletado com sucesso!")
                return redirect('maintenance:sop_list')
        except Exception as e:
            logger.error(f"Erro ao deletar SOP: {e}")
            messages.error(request, "Ocorreu um erro ao deletar o SOP. Por favor, tente novamente.")
    return render(request, 'confirm_delete.html', {
        'item_name': sop.title,
        'delete_url': reverse('maintenance:sop_delete', args=[sop.id]),
        'cancel_url': reverse('maintenance:sop_list'),
    })

# ====== Views de CalibrationStandard ======

@login_required
@permission_required('maintenance.can_view_calibrationstandard', raise_exception=True)
def calibration_standard_list(request):
    """
    Exibe uma lista paginada de padrões de calibração com funcionalidade de filtro.
    """
    calibration_standard_records = CalibrationStandard.objects.all()
    calibration_standard_filter = CalibrationStandardFilter(request.GET, queryset=calibration_standard_records)
    calibration_standard_records = calibration_standard_filter.qs.order_by('name')

    paginator = Paginator(calibration_standard_records, 50)  # 50 itens por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'maintenance/calibration_standard_list.html', {
        'calibration_standard_records': page_obj,
        'filter': calibration_standard_filter,
    })

@login_required
@permission_required('maintenance.can_add_calibrationstandard', raise_exception=True)
def calibration_standard_create(request):
    """
    Trata a criação de um novo padrão de calibração.
    """
    return handle_form(
        request=request,
        form_class=CalibrationStandardForm,
        template_name='maintenance/calibration_standard_form.html',
        success_message='Padrão de calibração criado com sucesso!',
        redirect_url='maintenance:calibration_standard_list',
        change_reason=f"Padrão de calibração adicionado por {request.user.get_full_name()}",
        instance=None
    )

@login_required
@permission_required('maintenance.can_change_calibrationstandard', raise_exception=True)
def calibration_standard_edit(request, pk):
    """
    Trata a edição de um padrão de calibração existente.
    """
    calibration_standard = get_object_or_404(CalibrationStandard, pk=pk)
    return handle_form(
        request=request,
        form_class=CalibrationStandardForm,
        template_name='maintenance/calibration_standard_form.html',
        success_message='Padrão de calibração atualizado com sucesso!',
        redirect_url='maintenance:calibration_standard_list',
        change_reason=f"Padrão de calibração atualizado por {request.user.get_full_name()}",
        instance=calibration_standard
    )

@login_required
@permission_required('maintenance.can_delete_calibrationstandard', raise_exception=True)
def calibration_standard_delete(request, pk):
    """
    Trata a exclusão de um padrão de calibração existente.
    """
    calibration_standard = get_object_or_404(CalibrationStandard, pk=pk)
    if request.method == 'POST':
        try:
            with transaction.atomic():
                update_change_reason(calibration_standard, f"Padrão de calibração deletado por {request.user.get_full_name()}")
                calibration_standard.delete()
                messages.success(request, "Padrão de calibração deletado com sucesso!")
                return redirect('maintenance:calibration_standard_list')
        except Exception as e:
            logger.error(f"Erro ao deletar padrão de calibração: {e}")
            messages.error(request, "Ocorreu um erro ao deletar o padrão de calibração. Por favor, tente novamente.")
    return render(request, 'confirm_delete.html', {
        'item_name': calibration_standard.name,
        'delete_url': reverse('maintenance:calibration_standard_delete', args=[calibration_standard.id]),
        'cancel_url': reverse('maintenance:calibration_standard_list'),
    })

# ====== Views de Verificação Diária ======

@login_required
@permission_required('maintenance.can_view_dailyverification', raise_exception=True)
def daily_verification_list(request):
    """
    Exibe uma lista paginada de verificações diárias com funcionalidade de filtro.
    """
    daily_verifications = DailyVerification.objects.all()
    verification_filter = DailyVerificationFilter(request.GET, queryset=daily_verifications)
    daily_verifications = verification_filter.qs.order_by('-created_at')

    paginator = Paginator(daily_verifications, 50)  # 50 itens por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'maintenance/daily_verification_list.html', {
        'page_obj': page_obj,
        'filter': verification_filter,
    })

@login_required
@permission_required('maintenance.can_add_dailyverification', raise_exception=True)
def daily_verification_create(request):
    """
    Trata a criação de uma nova verificação diária.
    """
    return handle_form(
        request=request,
        form_class=DailyVerificationForm,
        template_name='maintenance/daily_verification_form.html',
        success_message='Verificação diária criada com sucesso!',
        redirect_url='maintenance:daily_verification_list',
        change_reason=f"Verificação diária adicionada por {request.user.get_full_name()}",
        instance=None
    )

@login_required
@permission_required('maintenance.can_change_dailyverification', raise_exception=True)
def daily_verification_edit(request, pk):
    """
    Trata a edição de uma verificação diária existente.
    """
    verification = get_object_or_404(DailyVerification, pk=pk)
    return handle_form(
        request=request,
        form_class=DailyVerificationForm,
        template_name='maintenance/daily_verification_form.html',
        success_message='Verificação diária atualizada com sucesso!',
        redirect_url='maintenance:daily_verification_list',
        change_reason=f"Verificação diária atualizada por {request.user.get_full_name()}",
        instance=verification
    )

@login_required
@permission_required('maintenance.can_delete_dailyverification', raise_exception=True)
def daily_verification_delete(request, pk):
    """
    Trata a exclusão de uma verificação diária existente.
    """
    verification = get_object_or_404(DailyVerification, pk=pk)
    if request.method == 'POST':
        try:
            with transaction.atomic():
                verification.delete()
                messages.success(request, "Verificação diária deletada com sucesso!")
                return redirect('maintenance:daily_verification_list')
        except Exception as e:
            logger.error(f"Erro ao deletar verificação diária: {e}")
            messages.error(request, "Ocorreu um erro ao deletar a verificação diária. Por favor, tente novamente.")
    return render(request, 'confirm_delete.html', {
        'item_name': verification.created_at.strftime('%d/%m/%Y %H:%M'),
        'delete_url': reverse('maintenance:daily_verification_delete', args=[verification.id]),
        'cancel_url': reverse('maintenance:daily_verification_list'),
    })

# ====== View de Lista por Dia ======

@login_required
@permission_required('maintenance.can_view_maintenance', raise_exception=True)
def maintenance_list_by_day(request, year, month, day):
    """
    Exibe uma lista de manutenções e calibrações para uma data específica.
    """
    try:
        selected_date = date(year, month, day)
    except ValueError:
        messages.error(request, "Data inválida.")
        return redirect('maintenance:maintenance_list')

    maintenance_items = Maintenance.objects.filter(
        last_maintenance_date=selected_date
    ).select_related('item', 'technician', 'sop')

    calibration_items = Calibration.objects.filter(
        last_calibration_date=selected_date
    ).select_related('item', 'technician', 'sop', 'standard')

    return render(request, 'maintenance/maintenance_list_by_day.html', {
        'selected_date': selected_date,
        'maintenance_items': maintenance_items,
        'calibration_items': calibration_items,
    })

# ====== View de Calendário de Manutenção ======

@login_required
@permission_required('maintenance.can_view_maintenance', raise_exception=True)
def maintenance_calendar(request, year=None, month=None):
    """
    Exibe um calendário de manutenção e calibração.
    """
    if year is None or month is None:
        today = datetime.today()
        year = today.year
        month = today.month
    else:
        try:
            year = int(year)
            month = int(month)
            if not (1 <= month <= 12):
                raise ValueError
        except ValueError:
            messages.error(request, "Ano ou mês inválido.")
            return redirect('maintenance:maintenance_calendar')

    first_day_of_month = date(year, month, 1)
    last_day_of_month = (first_day_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    first_day_weekday = first_day_of_month.weekday()

    empty_days_start = first_day_weekday  # Dias vazios no início da semana
    empty_days_end = 6 - last_day_of_month.weekday()  # Dias vazios no final da semana

    maintenance_records = Maintenance.objects.filter(
        last_maintenance_date__year=year,
        last_maintenance_date__month=month
    )
    calibration_records = Calibration.objects.filter(
        last_calibration_date__year=year,
        last_calibration_date__month=month
    )

    maintenance_days = maintenance_records.values_list('last_maintenance_date', flat=True)
    calibration_days = calibration_records.values_list('last_calibration_date', flat=True)

    prev_month = month - 1 if month > 1 else 12
    next_month = month + 1 if month < 12 else 1
    prev_year = year if month > 1 else year - 1
    next_year = year if month < 12 else year + 1

    days_in_month = [first_day_of_month + timedelta(days=i) for i in range(last_day_of_month.day)]

    return render(request, 'maintenance/maintenance_calendar.html', {
        'year': year,
        'month': month,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'first_day_of_month': first_day_of_month,
        'last_day_of_month': last_day_of_month,
        'empty_days_start': range(empty_days_start),
        'empty_days_end': range(empty_days_end),
        'maintenance_days': maintenance_days,
        'calibration_days': calibration_days,
        'days_in_month': days_in_month,
    })
