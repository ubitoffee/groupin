from django.db import models
from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver


class Equipment(models.Model):
    # 제품종류 / 제조사 / 제품코드 / serial num / 임대여부(Y/N) / 임대사 / 임대기간 / 소유자 / 받은 날짜
    type = models.CharField(max_length=50, blank=False)
    manufacturer = models.CharField(max_length=50, blank=False)
    model_code = models.CharField(max_length=100, blank=False)
    serial_num = models.CharField(max_length=100, blank=False, unique=True)
    owner = models.ForeignKey('auth.User', related_name='owner')
    received_date = models.DateField(blank=True, null=True)

    # 대여기기 관련
    is_rental = models.BooleanField(default=False)
    rental_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)

    purchase_date = models.DateField(null=True, blank=True)
    is_delete = models.BooleanField(default=False, blank=True)

    author = models.ForeignKey('auth.User', related_name='author')


class EquipmentHistory(models.Model):
    equip = models.ForeignKey('equipment.Equipment')
    owner = models.ForeignKey('auth.User')

    received_date = models.DateField(blank=True, null=True)


@receiver(pre_save, sender=Equipment)
def create_equip(sender, instance, created, **kwargs):
    prev_equip = Equipment.objects.get(instance.pk)

    if prev_equip.owner != instance.owner:
        history = EquipmentHistory.objects.create(
            equip=instance,
            owner=instance.owner,
            received_date=instance.received_date
        )

        history.save()
