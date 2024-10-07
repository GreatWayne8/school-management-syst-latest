from django.shortcuts import render, get_object_or_404, redirect
from .models import Bus, Route, StudentPickup, TransportRequest  # Import TransportRequest model
from .forms import BusForm, RouteForm, StudentPickupForm, TransportRequestForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def bus_list(request):
    buses = Bus.objects.all()
    return render(request, 'transportation/bus_list.html', {'buses': buses})

def bus_detail(request, pk):
    bus = get_object_or_404(Bus, pk=pk)
    return render(request, 'transportation/bus_detail.html', {'bus': bus})

def route_list(request):
    routes = Route.objects.all()
    return render(request, 'transportation/route_list.html', {'routes': routes})

def route_detail(request, pk):
    route = get_object_or_404(Route, pk=pk)
    return render(request, 'transportation/route_detail.html', {'route': route})

def student_pickup_list(request):
    pickups = StudentPickup.objects.all()  
    return render(request, 'transportation/student_pickup_list.html', {'student_pickups': pickups})

def student_pickup_detail(request, pk):
    pickup = get_object_or_404(StudentPickup, pk=pk)
    return render(request, 'transportation/student_pickup_detail.html', {'pickup': pickup})

def create_bus(request):
    if request.method == 'POST':
        form = BusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bus created successfully.')
            return redirect('transportation:bus_list')
    else:
        form = BusForm()
    return render(request, 'transportation/create_bus.html', {'form': form})

def create_route(request):
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Route created successfully.')
            return redirect('transportation:route_list')  # Redirect to the list view after successful creation
    else:
        form = RouteForm()
    
    return render(request, 'transportation/create_route.html', {'form': form})

@login_required
def approve_transport_request(request, pk):
    transport_request = get_object_or_404(TransportRequest, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            transport_request.approved = True
            transport_request.status = 'approved'
            messages.success(request, 'Transport request approved successfully.')
        elif action == 'decline':
            transport_request.approved = False
            transport_request.status = 'declined'
            messages.success(request, 'Transport request declined successfully.')

        transport_request.save()
        return redirect('transportation:transport_list')

    return render(request, 'transportation/approve_transport_request.html', {'request': transport_request})

def create_student_pickup(request):
    if request.method == 'POST':
        form = StudentPickupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student pickup created successfully.')
            return redirect('transportation:student_pickup_list')
    else:
        form = StudentPickupForm()
    return render(request, 'transportation/create_student_pickup.html', {'form': form})

def create_transport_request(request):
    if request.method == 'POST':
        form = TransportRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transport request created successfully.')
            return redirect('transportation:transport_list')
    else:
        form = TransportRequestForm()
    return render(request, 'transportation/create_transport_request.html', {'form': form})

def transport_list(request):
    transport_requests = TransportRequest.objects.all()
    return render(request, 'transportation/transport_list.html', {'transport_requests': transport_requests})
