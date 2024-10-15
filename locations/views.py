# locations/views.py

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Building, Room, Measurement
from .forms import BuildingForm, RoomForm, MeasurementForm
import json

# ====== Building Views ======

@login_required
@permission_required('locations.view_building', raise_exception=True)
def building_list(request):
    """
    Display a list of all buildings with optional search functionality.
    """
    search_query = request.GET.get('search', '')
    if search_query:
        buildings = Building.objects.filter(name__icontains=search_query)
    else:
        buildings = Building.objects.all()
    return render(request, 'locations/building_list.html', {'buildings': buildings})


@login_required
@permission_required('locations.add_building', raise_exception=True)
def building_create(request):
    """
    Handle the creation of a new building.
    """
    if request.method == 'POST':
        form = BuildingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Building created successfully!")
            return redirect('building_list')
    else:
        form = BuildingForm()
    return render(request, 'locations/building_form.html', {
        'form': form,
        'title': 'Add Building',
        'button_label': 'Save'
    })


@login_required
@permission_required('locations.change_building', raise_exception=True)
def building_edit(request, pk):
    """
    Handle the editing of an existing building.
    """
    building = get_object_or_404(Building, pk=pk)
    if request.method == 'POST':
        form = BuildingForm(request.POST, request.FILES, instance=building)
        if form.is_valid():
            form.save()
            messages.success(request, "Building updated successfully!")
            return redirect('building_list')
    else:
        form = BuildingForm(instance=building)
    return render(request, 'locations/building_form.html', {
        'form': form,
        'building': building,
        'title': 'Edit Building',
        'button_label': 'Update'
    })


@login_required
@permission_required('locations.delete_building', raise_exception=True)
def building_delete(request, pk):
    """
    Handle the deletion of an existing building.
    """
    building = get_object_or_404(Building, pk=pk)
    if request.method == 'POST':
        building.delete()
        messages.success(request, "Building deleted successfully!")
        return redirect('building_list')
    return render(request, 'confirm_delete.html', {
        'item_name': building.name,
        'delete_url': request.path,
        'cancel_url': 'building_list'
    })


# ====== Room Views ======

@login_required
@permission_required('locations.view_room', raise_exception=True)
def room_list(request):
    """
    Display a list of all rooms with optional search functionality.
    """
    search_query = request.GET.get('search', '')
    if search_query:
        rooms = Room.objects.filter(name__icontains=search_query)
    else:
        rooms = Room.objects.all()
    return render(request, 'locations/room_list.html', {'rooms': rooms})


@login_required
@permission_required('locations.add_room', raise_exception=True)
def room_create(request):
    """
    Handle the creation of a new room.
    """
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Room created successfully!")
            return redirect('room_list')
    else:
        form = RoomForm()
    return render(request, 'locations/room_form.html', {
        'form': form,
        'title': 'Add Room',
        'button_label': 'Save'
    })


@login_required
@permission_required('locations.change_room', raise_exception=True)
def room_edit(request, pk):
    """
    Handle the editing of an existing room.
    """
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, "Room updated successfully!")
            return redirect('room_list')
    else:
        form = RoomForm(instance=room)
    return render(request, 'locations/room_form.html', {
        'form': form,
        'room': room,
        'title': 'Edit Room',
        'button_label': 'Update'
    })


@login_required
@permission_required('locations.delete_room', raise_exception=True)
def room_delete(request, pk):
    """
    Handle the deletion of an existing room.
    """
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room.delete()
        messages.success(request, "Room deleted successfully!")
        return redirect('room_list')
    return render(request, 'confirm_delete.html', {
        'item_name': room.name,
        'delete_url': request.path,
        'cancel_url': 'room_list'
    })


# ====== Measurement Views ======

@login_required
@permission_required('locations.view_room', raise_exception=True)
def measurement_room_list(request):
    """
    Display a list of all rooms available for viewing measurements.
    Similar to room_list.html but specifically for measurements.
    """
    search_query = request.GET.get('search', '')
    if search_query:
        rooms = Room.objects.filter(name__icontains=search_query)
    else:
        rooms = Room.objects.all()
    return render(request, 'locations/measurement_room_list.html', {'rooms': rooms})


@login_required
@permission_required('locations.view_measurement', raise_exception=True)
def measurement_room_detail(request, pk):
    """
    Display the measurement details of a specific room, including a graph of measurements.
    Provides a button to add new measurements.
    """
    room = get_object_or_404(Room, pk=pk)
    measurements = Measurement.objects.filter(room=room).order_by('recorded_at')
    
    # Extract data for the chart
    timestamps = [m.recorded_at.strftime('%d/%m/%Y %H:%M') for m in measurements]
    temperatures = list(measurements.values_list('temperature', flat=True))
    humidities = list(measurements.values_list('humidity', flat=True))
    
    context = {
        'room': room,
        'temperatures': json.dumps(temperatures),
        'humidities': json.dumps(humidities),
        'timestamps': json.dumps(timestamps),
    }
    
    return render(request, 'locations/measurement_room_detail.html', context)


@login_required
@permission_required('locations.add_measurement', raise_exception=True)
def measurement_create(request):
    """
    Handle the creation of a new measurement.
    Measurements are associated with a specific room.
    """
    initial_data = {}
    room_id = request.GET.get('room')
    if room_id:
        initial_data['room'] = room_id
    
    if request.method == 'POST':
        form = MeasurementForm(request.POST)
        if form.is_valid():
            measurement = form.save()
            messages.success(request, "Measurement created successfully!")
            return redirect('measurement_room_detail', pk=measurement.room.id)
    else:
        form = MeasurementForm(initial=initial_data)
    
    return render(request, 'locations/measurement_form.html', {
        'form': form,
        'title': 'Add Measurement',
        'button_label': 'Save'
    })

