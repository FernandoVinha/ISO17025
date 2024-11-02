from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MaintenanceForm, CalibrationForm, TrainingForm, SOPForm, CalibrationStandardForm, DailyVerificationForm
from .filters import MaintenanceFilter, CalibrationFilter, TrainingFilter, SOPFilter, CalibrationStandardFilter, DailyVerificationFilter
from .models import Maintenance, Calibration, Training, StandardOperatingProcedure, CalibrationStandard, DailyVerification
from datetime import date

# ======= Helper Function for Handling Forms =======
def handle_form(request, form_class, template_name, success_message, redirect_url, instance=None):
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, success_message)
            return redirect(redirect_url)
        else:
            messages.error(request, "Error processing the form. Please check the data.")
    else:
        form = form_class(instance=instance)
    
    return render(request, template_name, {'form': form})

# ====== Maintenance Views ======
@login_required
@permission_required('maintenance.can_view_maintenance', raise_exception=True)
def maintenance_list(request):
    maintenance_records = Maintenance.objects.all()
    paginator = Paginator(maintenance_records, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'maintenance/maintenance_list.html', {
        'page_obj': page_obj,
    })

@login_required
@permission_required('maintenance.can_view_maintenance', raise_exception=True)
def maintenance_list_by_day(request, year, month, day):
    selected_date = date(year, month, day)
    maintenance_items = Maintenance.objects.filter(last_maintenance_date=selected_date)
    calibration_items = Calibration.objects.filter(last_calibration_date=selected_date)

    return render(request, 'maintenance/maintenance_list_by_day.html', {
        'selected_date': selected_date,
        'maintenance_items': maintenance_items,
        'calibration_items': calibration_items,
    })

@login_required
@permission_required('maintenance.can_add_maintenance', raise_exception=True)
def maintenance_create(request):
    return handle_form(
        request, 
        MaintenanceForm, 
        'maintenance/maintenance_form.html', 
        'Maintenance created successfully!', 
        'maintenance_list'
    )

@login_required
@permission_required('maintenance.can_change_maintenance', raise_exception=True)
def maintenance_edit(request, pk):
    maintenance = get_object_or_404(Maintenance, pk=pk)
    return handle_form(
        request, 
        MaintenanceForm, 
        'maintenance/maintenance_form.html', 
        'Maintenance updated successfully!', 
        'maintenance_list', 
        instance=maintenance
    )

@login_required
@permission_required('maintenance.can_delete_maintenance', raise_exception=True)
def maintenance_delete(request, pk):
    maintenance = get_object_or_404(Maintenance, pk=pk)
    if request.method == 'POST':
        maintenance.delete()
        messages.success(request, "Maintenance deleted successfully!")
        return redirect('maintenance_list')
    return render(request, 'confirm_delete.html', {
        'item_name': maintenance.description,
        'delete_url': request.path,
        'cancel_url': 'maintenance_list'
    })

# ====== Calibration Views ======
@login_required
@permission_required('maintenance.can_view_calibration', raise_exception=True)
def calibration_list(request):
    calibration_records = Calibration.objects.all()
    calibration_filter = CalibrationFilter(request.GET, queryset=calibration_records)
    calibration_records = calibration_filter.qs

    paginator = Paginator(calibration_records, 50)
    page_number = request.GET.get('page')
    calibration_records = paginator.get_page(page_number)

    return render(request, 'maintenance/calibration_list.html', {
        'calibration_records': calibration_records,
        'filter': calibration_filter,
    })

@login_required
@permission_required('maintenance.can_add_calibration', raise_exception=True)
def calibration_create(request):
    return handle_form(
        request, 
        CalibrationForm, 
        'maintenance/calibration_form.html', 
        'Calibration created successfully!', 
        'calibration_list'
    )

@login_required
@permission_required('maintenance.can_change_calibration', raise_exception=True)
def calibration_edit(request, pk):
    calibration = get_object_or_404(Calibration, pk=pk)
    return handle_form(
        request, 
        CalibrationForm, 
        'maintenance/calibration_form.html', 
        'Calibration updated successfully!', 
        'calibration_list', 
        instance=calibration
    )

@login_required
@permission_required('maintenance.can_delete_calibration', raise_exception=True)
def calibration_delete(request, pk):
    calibration = get_object_or_404(Calibration, pk=pk)
    if request.method == 'POST':
        calibration.delete()
        messages.success(request, "Calibration deleted successfully!")
        return redirect('calibration_list')
    return render(request, 'confirm_delete.html', {
        'item_name': calibration.description,
        'delete_url': request.path,
        'cancel_url': 'calibration_list'
    })

# ====== Training Views ======
@login_required
@permission_required('maintenance.can_view_training', raise_exception=True)
def training_list(request):
    training_records = Training.objects.all()
    training_filter = TrainingFilter(request.GET, queryset=training_records)
    training_records = training_filter.qs

    paginator = Paginator(training_records, 50)
    page_number = request.GET.get('page')
    training_records = paginator.get_page(page_number)

    return render(request, 'maintenance/training_list.html', {
        'training_records': training_records,
        'filter': training_filter,
    })

@login_required
@permission_required('maintenance.can_add_training', raise_exception=True)
def training_create(request):
    return handle_form(
        request, 
        TrainingForm, 
        'maintenance/training_form.html', 
        'Training created successfully!', 
        'training_list'
    )

@login_required
@permission_required('maintenance.can_change_training', raise_exception=True)
def training_edit(request, pk):
    training = get_object_or_404(Training, pk=pk)
    return handle_form(
        request, 
        TrainingForm, 
        'maintenance/training_form.html', 
        'Training updated successfully!', 
        'training_list', 
        instance=training
    )

@login_required
@permission_required('maintenance.can_delete_training', raise_exception=True)
def training_delete(request, pk):
    training = get_object_or_404(Training, pk=pk)
    if request.method == 'POST':
        training.delete()
        messages.success(request, "Training deleted successfully!")
        return redirect('training_list')
    return render(request, 'confirm_delete.html', {
        'item_name': training.description,
        'delete_url': request.path,
        'cancel_url': 'training_list'
    })

# ====== SOP Views ======
@login_required
@permission_required('maintenance.can_view_sop', raise_exception=True)
def sop_list(request):
    sop_records = StandardOperatingProcedure.objects.all()
    sop_filter = SOPFilter(request.GET, queryset=sop_records)
    sop_records = sop_filter.qs

    paginator = Paginator(sop_records, 50)
    page_number = request.GET.get('page')
    sop_records = paginator.get_page(page_number)

    return render(request, 'maintenance/sop_list.html', {
        'sop_records': sop_records,
        'filter': sop_filter,
    })

@login_required
@permission_required('maintenance.can_add_sop', raise_exception=True)
def sop_create(request):
    return handle_form(
        request, 
        SOPForm, 
        'maintenance/sop_form.html', 
        'SOP created successfully!', 
        'sop_list'
    )

@login_required
@permission_required('maintenance.can_change_sop', raise_exception=True)
def sop_edit(request, pk):
    sop = get_object_or_404(StandardOperatingProcedure, pk=pk)
    return handle_form(
        request, 
        SOPForm, 
        'maintenance/sop_form.html', 
        'SOP updated successfully!', 
        'sop_list', 
        instance=sop
    )

@login_required
@permission_required('maintenance.can_delete_sop', raise_exception=True)
def sop_delete(request, pk):
    sop = get_object_or_404(StandardOperatingProcedure, pk=pk)
    if request.method == 'POST':
        sop.delete()
        messages.success(request, "SOP deleted successfully!")
        return redirect('sop_list')
    return render(request, 'confirm_delete.html', {
        'item_name': sop.title,
        'delete_url': request.path,
        'cancel_url': 'sop_list'
    })

# ====== CalibrationStandard Views ======
@login_required
@permission_required('maintenance.can_view_calibrationstandard', raise_exception=True)
def calibration_standard_list(request):
    calibration_standard_records = CalibrationStandard.objects.all()
    calibration_standard_filter = CalibrationStandardFilter(request.GET, queryset=calibration_standard_records)
    calibration_standard_records = calibration_standard_filter.qs

    paginator = Paginator(calibration_standard_records, 50)
    page_number = request.GET.get('page')
    calibration_standard_records = paginator.get_page(page_number)

    return render(request, 'maintenance/calibration_standard_list.html', {
        'calibration_standard_records': calibration_standard_records,
        'filter': calibration_standard_filter,
    })

@login_required
@permission_required('maintenance.can_add_calibrationstandard', raise_exception=True)
def calibration_standard_create(request):
    return handle_form(
        request, 
        CalibrationStandardForm, 
        'maintenance/calibration_standard_form.html', 
        'Calibration Standard created successfully!', 
        'calibration_standard_list'
    )

@login_required
@permission_required('maintenance.can_change_calibrationstandard', raise_exception=True)
def calibration_standard_edit(request, pk):
    calibration_standard = get_object_or_404(CalibrationStandard, pk=pk)
    return handle_form(
        request, 
        CalibrationStandardForm, 
        'maintenance/calibration_standard_form.html', 
        'Calibration Standard updated successfully!', 
        'calibration_standard_list', 
        instance=calibration_standard
    )

@login_required
@permission_required('maintenance.can_delete_calibrationstandard', raise_exception=True)
def calibration_standard_delete(request, pk):
    calibration_standard = get_object_or_404(CalibrationStandard, pk=pk)
    if request.method == 'POST':
        calibration_standard.delete()
        messages.success(request, "Calibration Standard deleted successfully!")
        return redirect('calibration_standard_list')
    return render(request, 'confirm_delete.html', {
        'item_name': calibration_standard.name,
        'delete_url': request.path,
        'cancel_url': 'calibration_standard_list'
    })

# ====== DailyVerification Views ======
@login_required
@permission_required('maintenance.can_view_dailyverification', raise_exception=True)

def daily_verification_list(request):
    email_query = request.GET.get('email', '')
    date_query = request.GET.get('date', '')
    equipment_query = request.GET.get('equipment', '')

    daily_verifications = DailyVerification.objects.all()

    # Filtro por email
    if email_query:
        daily_verifications = daily_verifications.filter(
            Q(user__email__icontains=email_query)
        )

    # Filtro por data
    if date_query:
        try:
            date_obj = datetime.strptime(date_query, '%Y-%m-%d')
            daily_verifications = daily_verifications.filter(
                created_at__date=date_obj
            )
        except ValueError:
            pass  # Ignora erro de formatação de data

    # Filtro por equipamento
    if equipment_query:
        daily_verifications = daily_verifications.filter(
            Q(item__name__icontains=equipment_query)
        )

    verification_filter = DailyVerificationFilter(request.GET, queryset=daily_verifications)
    daily_verifications = verification_filter.qs

    paginator = Paginator(daily_verifications, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'maintenance/daily_verification_list.html', {
        'page_obj': page_obj,
        'filter': verification_filter,
    })


@login_required
@permission_required('maintenance.can_add_dailyverification', raise_exception=True)
def daily_verification_create(request):
    return handle_form(
        request, 
        DailyVerificationForm, 
        'maintenance/daily_verification_form.html', 
        'Daily verification created successfully!', 
        'daily_verification_list'
    )

@login_required
@permission_required('maintenance.can_change_dailyverification', raise_exception=True)
def daily_verification_edit(request, pk):
    verification = get_object_or_404(DailyVerification, pk=pk)
    return handle_form(
        request, 
        DailyVerificationForm, 
        'maintenance/daily_verification_form.html', 
        'Daily verification updated successfully!', 
        'daily_verification_list', 
        instance=verification
    )

@login_required
@permission_required('maintenance.can_delete_dailyverification', raise_exception=True)
def daily_verification_delete(request, pk):
    verification = get_object_or_404(DailyVerification, pk=pk)
    if request.method == 'POST':
        verification.delete()
        messages.success(request, "Daily verification deleted successfully!")
        return redirect('daily_verification_list')
    return render(request, 'confirm_delete.html', {
        'item_name': verification.created_at.strftime('%d/%m/%Y %H:%M'),
        'delete_url': request.path,
        'cancel_url': 'daily_verification_list'
    })

# ====== Maintenance Calendar View ======
@login_required
@permission_required('maintenance.can_view_maintenance', raise_exception=True)
def maintenance_calendar(request, year=None, month=None):
    if year is None or month is None:
        today = datetime.today()
        year = today.year
        month = today.month
    else:
        year = int(year)
        month = int(month)

    first_day_of_month = datetime(year, month, 1)
    last_day_of_month = (first_day_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    first_day_weekday = first_day_of_month.weekday()

    empty_days_start = first_day_weekday
    empty_days_end = 6 - last_day_of_month.weekday()

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
