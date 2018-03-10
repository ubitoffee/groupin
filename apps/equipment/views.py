from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404

from apps.equipment.models import Equipment
from .forms import EquipmentForm


@login_required
def get_list(request):

    equip_list = Equipment.objects.all()

    return render(request, 'equipment/equipment.html', {'equip_list': equip_list})


@login_required
def register(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)

        if form.is_valid():

            equipment = Equipment()
            equipment.type = form.cleaned_data['type']
            equipment.manufacturer = form.cleaned_data['manufacturer']
            equipment.model_code = form.cleaned_data['model_code']
            equipment.serial_num = form.cleaned_data['serial_num']
            equipment.owner = form.cleaned_data['owner']
            equipment.received_date = form.cleaned_data['received_date']
            equipment.is_rental = form.cleaned_data['is_rental']
            equipment.rental_date = form.cleaned_data['rental_date']
            equipment.return_date = form.cleaned_data['return_date']
            equipment.purchase_date = form.cleaned_data['purchase_date']
            equipment.creator = request.user

            equipment.save()

            return redirect('equip:list')

    else:
        form = EquipmentForm(initial={'owner': request.user})

    return render(request, 'equipment/form.html', {'form': form})


@login_required
def edit(request, id=None):

    if id:
        equipment = get_object_or_404(Equipment, pk=id)

        if request.user == equipment.owner or request.user == equipment.creator \
                or request.user.is_superuser or request.user.is_staff:
            raise PermissionDenied("You have no permission for this page")

    if request.method == 'POST':
        form = EquipmentForm(request.POST)

        if form.is_valid():

            equipment.type = form.cleaned_data['type']
            equipment.manufacturer = form.cleaned_data['manufacturer']
            equipment.model_code = form.cleaned_data['model_code']
            equipment.serial_num = form.cleaned_data['serial_num']
            equipment.owner = form.cleaned_data['owner']
            equipment.received_date = form.cleaned_data['received_date']
            equipment.is_rental = form.cleaned_data['is_rental']
            equipment.rental_date = form.cleaned_data['rental_date']
            equipment.return_date = form.cleaned_data['return_date']
            equipment.purchase_date = form.cleaned_data['purchase_date']

            equipment.save()

            return redirect('equip:list')

    else:
        initial = {
            'type': equipment.type,
            'manufacturer': equipment.manufacturer,
            'model_code': equipment.model_code,
            'serial_num': equipment.serial_num,
            'user': equipment.user,
            'received_date': equipment.received_date,
            'is_rental': equipment.is_rental,
            'rental_date': equipment.rental_date,
            'return_date': equipment.return_date,
            'purchase_date': equipment.purchase_date
        }

        form = EquipmentForm(initial=initial)

        return render(request, 'equipment/form.html', {'form': form})
