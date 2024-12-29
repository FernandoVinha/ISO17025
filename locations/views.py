# locations/views.py

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Building, Room, Measurement
from .forms import BuildingForm, RoomForm, MeasurementForm
from simple_history.utils import update_change_reason
from django.core.paginator import Paginator
from django.http import JsonResponse


from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import RoomSerializer, MeasurementSerializer

import logging

logger = logging.getLogger(__name__)


# ====== Building Views ======

@login_required
@permission_required('locations.view_building', raise_exception=True)
def building_list(request):
    """
    Displays a list of all buildings with search and pagination functionality.
    """
    search_query = request.GET.get('search', '')
    if search_query:
        buildings = Building.objects.filter(name__icontains=search_query)
    else:
        buildings = Building.objects.all()

    # Add pagination
    paginator = Paginator(buildings, 50)  # 50 items per page
    page_number = request.GET.get('page')
    buildings_page = paginator.get_page(page_number)

    # Avoid the N+1 problem by not passing history directly to the template for performance optimization
    # If needed, consider implementing asynchronous loading via AJAX

    return render(request, 'locations/building_list.html', {
        'buildings': buildings_page,
    })


@login_required
@permission_required('locations.add_building', raise_exception=True)
def building_create(request):
    """
    Handles the creation of a new building.
    The delete button will not be available in this view.
    """
    if request.method == 'POST':
        form = BuildingForm(request.POST, request.FILES)
        if form.is_valid():
            building = form.save()
            update_change_reason(building, "Building created")
            messages.success(request, "Building created successfully!")
            return redirect('locations:building_list')
    else:
        form = BuildingForm()
    return render(request, 'locations/building_form.html', {
        'form': form,
        'title': 'Add Building',
        'button_label': 'Save',
        'building': None,  # Pass building as None during creation
    })


@login_required
@permission_required('locations.change_building', raise_exception=True)
def building_edit(request, pk):
    """
    Handles the editing of an existing building.
    The delete button will be available in this view.
    """
    building = get_object_or_404(Building, pk=pk)
    if request.method == 'POST':
        form = BuildingForm(request.POST, request.FILES, instance=building)
        if form.is_valid():
            form.save()
            update_change_reason(building, f"Building updated by {request.user.get_full_name()}")
            messages.success(request, "Building updated successfully!")
            return redirect('locations:building_list')
    else:
        form = BuildingForm(instance=building)

    return render(request, 'locations/building_form.html', {
        'form': form,
        'building': building,
        'title': 'Edit Building',
        'button_label': 'Update',
        'simple_history': building.history.all()[:30],  # Display history
    })


@login_required
@permission_required('locations.delete_building', raise_exception=True)
def building_delete(request, pk):
    """
    Handles the deletion of an existing building.
    """
    building = get_object_or_404(Building, pk=pk)
    if request.method == 'POST':
        building.delete()
        messages.success(request, "Building deleted successfully!")
        return redirect('locations:building_list')
    return render(request, 'confirm_delete.html', {
        'item_name': building.name,
        'delete_url': reverse('locations:building_delete', args=[building.id]),
        'cancel_url': reverse('locations:building_list'),
        'simple_history': building.history.all()[:30],  # Display history
    })

# ====== Room Views ======

@login_required
@permission_required('locations.view_room', raise_exception=True)
def room_list(request):
    """
    Displays a list of all rooms with search and pagination functionality.
    """
    search_query = request.GET.get('search', '')
    if search_query:
        rooms = Room.objects.filter(name__icontains=search_query)
    else:
        rooms = Room.objects.all()

    paginator = Paginator(rooms, 50)  # 50 items per page
    page_number = request.GET.get('page')
    rooms_page = paginator.get_page(page_number)

    return render(request, 'locations/room_list.html', {
        'rooms': rooms_page,
    })


@login_required
@permission_required('locations.add_room', raise_exception=True)
def room_create(request):
    """
    Handles the creation of a new room.
    The delete button will not be available in this view.
    """
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save()
            update_change_reason(room, "Room created")
            messages.success(request, "Room created successfully!")
            return redirect('locations:room_list')
    else:
        form = RoomForm()
    return render(request, 'locations/room_form.html', {
        'form': form,
        'title': 'Add Room',
        'button_label': 'Save',
        'room': None,  # Pass room as None during creation
    })


@login_required
@permission_required('locations.change_room', raise_exception=True)
def room_edit(request, pk):
    """
    Handles the editing of an existing room.
    The delete button will be available in this view.
    """
    # Obter o objeto Room correspondente ao ID (pk) ou retornar 404 se não encontrado
    room = get_object_or_404(Room, pk=pk)
    
    if request.method == 'POST':
        # Vincular dados do formulário enviado à instância existente
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            # Salvar as alterações
            updated_room = form.save(commit=False)
            update_change_reason(updated_room, f"Room updated by {request.user.get_full_name()}")
            updated_room.save()
            messages.success(request, "Room updated successfully!")
            return redirect(reverse('locations:room_list'))
        else:
            # Mensagem de erro se o formulário não for válido
            messages.error(request, "Please correct the errors below.")
    else:
        # Criar o formulário com os dados da instância existente
        form = RoomForm(instance=room)

    # Renderizar o template com o formulário e o contexto adicional
    return render(request, 'locations/room_form.html', {
        'form': form,
        'room': room,
        'title': 'Edit Room',
        'button_label': 'Update Room',
        'simple_history': room.history.all()[:30],  # Mostrar o histórico das alterações (opcional)
    })


@login_required
@permission_required('locations.delete_room', raise_exception=True)
def room_delete(request, pk):
    """
    Handles the deletion of an existing room.
    """
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room.delete()
        messages.success(request, "Room deleted successfully!")
        return redirect('locations:room_list')
    return render(request, 'confirm_delete.html', {
        'item_name': room.name,
        'delete_url': reverse('locations:room_delete', args=[room.id]),
        'cancel_url': reverse('locations:room_list'),
        'simple_history': room.history.all()[:30],  # Display history
    })

# ====== Measurement Views ======

@login_required
@permission_required('locations.view_measurement', raise_exception=True)
def measurement_room_list(request):
    """
    Displays a list of all available rooms to view measurements with pagination.
    """
    search_query = request.GET.get('search', '')
    if search_query:
        rooms = Room.objects.filter(name__icontains=search_query)
    else:
        rooms = Room.objects.all()

    paginator = Paginator(rooms, 50)  # 50 items per page
    page_number = request.GET.get('page')
    rooms_page = paginator.get_page(page_number)

    return render(request, 'locations/measurement_room_list.html', {'rooms': rooms_page})


@login_required
@permission_required('locations.view_measurement', raise_exception=True)
def measurement_room_detail(request, pk):
    """
    Displays the measurement details of a specific room, including a measurement chart.
    Provides a button to add new measurements.
    """
    # Get the room corresponding to the ID (pk)
    room = get_object_or_404(Room, pk=pk)

    # Get the room's measurements, ordered by record date
    measurements = Measurement.objects.filter(room=room).order_by('-recorded_at')[:30]
    measurements = list(reversed(measurements))  # Reverse to show oldest first

    # Extract data needed for the chart
    timestamps = [m.recorded_at.strftime('%d/%m/%Y %H:%M') for m in measurements]
    temperatures = [m.temperature for m in measurements]
    humidities = [m.humidity for m in measurements]

    # Create context to be rendered in the template
    context = {
        'room': room,
        'timestamps': timestamps,
        'temperatures': temperatures,
        'humidities': humidities,
    }

    return render(request, 'locations/measurement_room_detail.html', context)


@login_required
@permission_required('locations.add_measurement', raise_exception=True)
def measurement_create(request):
    """
    Handles the creation of a new measurement.
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
            update_change_reason(measurement, "Measurement created")
            messages.success(request, "Measurement created successfully!")
            return redirect('locations:measurement_room_detail', pk=measurement.room.id)
    else:
        form = MeasurementForm(initial=initial_data)

    return render(request, 'locations/measurement_form.html', {
        'form': form,
        'title': 'Add Measurement',
        'button_label': 'Save'
    })


# API Endpoint to create room and measurement (with security and validation corrections)


@api_view(['POST'])
def create_room_and_measurement(request):
    """
    API endpoint para criar uma medição associada a uma sala existente.
    Não exige autenticação.
    """
    try:
        # Obtém os dados do corpo da requisição
        room_id = request.data.get('room')
        measurement_data = request.data

        # Verifica se os dados obrigatórios estão presentes
        if not room_id:
            return Response(
                {"error": "O ID da sala ('room') é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if 'temperature' not in measurement_data or 'humidity' not in measurement_data:
            return Response(
                {"error": "Os campos 'temperature' e 'humidity' são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verifica se a sala existe
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response(
                {"error": f"Sala com ID {room_id} não encontrada."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Cria a medição associada à sala
        measurement_serializer = MeasurementSerializer(data=measurement_data)
        if measurement_serializer.is_valid():
            measurement = measurement_serializer.save(room=room)
            return Response(
                {
                    "id": measurement.id,
                    "room": room.id,
                    "temperature": measurement.temperature,
                    "humidity": measurement.humidity,
                    "recorded_at": measurement.recorded_at
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(measurement_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"Erro ao processar a requisição: {str(e)}")
        return Response(
            {"error": f"Erro interno do servidor: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@permission_required('locations.view_measurement', raise_exception=True)
def get_measurements_data(request, room_id):
    """
    Returns the last 30 measurement data points for a specific room in JSON format.
    """
    measurements = Measurement.objects.filter(room_id=room_id).order_by('-recorded_at')[:30]
    measurements = list(reversed(measurements))  # Reverse to show from oldest to newest

    data = {
        'timestamps': [m.recorded_at.strftime('%d/%m/%Y %H:%M') for m in measurements],
        'temperatures': [m.temperature for m in measurements],
        'humidities': [m.humidity for m in measurements],
    }
    return JsonResponse(data)
