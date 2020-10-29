from django.db import models
from django.contrib.auth.models import User

import uuid

from django.utils import timezone
from datetime import timedelta
import datetime

# Create your models here.
class PipeData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mid = models.TextField()
    b = models.TextField()
    c = models.TextField()
    d = models.TextField()
    e = models.TextField()
    ts = models.TextField()
    count = models.TextField()
    weight = models.TextField()
    ps = models.TextField()
    site_time = models.TextField()
    shift = models.CharField(max_length=1, default="1")

    def toDic(self):
        return {'a': self.mid, 'b': self.b, 'c': self.c, 'd': self.d, 'e': self.e, 'ts': self.ts, 'count': self.count, 'weight': self.weight, 'ps': self.ps, "site_time": self.site_time, "shift": self.shift}




#class PipeData1(models.Model):
#    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#    mid = models.TextField()
#    b = models.TextField()
#    c = models.TextField()
#    d = models.TextField()
#    e = models.TextField()
#    ts = models.TextField()
#    count = models.TextField()
#    weight = models.TextField()
#    ps = models.TextField()
#    site_time = models.TextField()
#    shift = models.CharField(max_length=1, default="1")





class PipeDataProcessed(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    machine_id = models.CharField(max_length=100)
    basic_metarial = models.CharField(max_length=100, blank=True, null=True)
    standard_type_classification = models.CharField(max_length=100, blank=True, null=True)
    pressure_type_specification = models.CharField(max_length=100, blank=True, null=True)
    outer_diameter = models.FloatField(blank=True, null=True)
    outer_diameter_unit = models.CharField(max_length=100, blank=True, null=True)
    length = models.FloatField(blank=True, null=True)
    length_unit = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.BigIntegerField(null=True)
    count = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    maxweight = models.IntegerField(blank=True, null=True)
    minweight = models.IntegerField(blank=True, null=True)
    weightgain = models.IntegerField(blank=True, null=True)
    weightloss = models.IntegerField(blank=True, null=True)
    pass_status = models.CharField(max_length=100, blank=True, null=True)
    site_time = models.DateTimeField()
    shift = models.CharField(max_length=1)

    class Meta:
        ordering = ['-site_time']
        unique_together = ('machine_id', 'site_time')

    def toDic(self):
        return {'machine_id': self.machine_id, 'basic_metarial': self.basic_metarial, 'standard_type_classification': self.standard_type_classification, 'pressure_type_specification': self.pressure_type_specification, 'outer_diameter': self.outer_diameter, 'outer_diameter_unit': self.outer_diameter_unit, 'length': self.length, 'length_unit': self.length_unit, 'timestamp': self.timestamp, 'count': self.count, 'weight': self.weight, 'maxweight': self.maxweight, 'minweight': self.minweight, 'weightgain': self.weightgain, 'weightloss': self.weightloss, 'pass_status': self.pass_status, 'site_time': self.site_time, 'shift': self.shift}



#class PipeDataProcessed1(models.Model):
#    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#    machine_id = models.CharField(max_length=100)
#    basic_metarial = models.CharField(max_length=100, blank=True, null=True)
#    standard_type_classification = models.CharField(max_length=100, blank=True, null=True)
#    pressure_type_specification = models.CharField(max_length=100, blank=True, null=True)
#    outer_diameter = models.FloatField(blank=True, null=True)
#    outer_diameter_unit = models.CharField(max_length=100, blank=True, null=True)
#    length = models.FloatField(blank=True, null=True)
#    length_unit = models.CharField(max_length=100, blank=True, null=True)
#    timestamp = models.BigIntegerField()
#    count = models.IntegerField(blank=True, null=True)
#    weight = models.IntegerField(blank=True, null=True)
#    maxweight = models.IntegerField(blank=True, null=True)
#    minweight = models.IntegerField(blank=True, null=True)
#    weightgain = models.IntegerField(blank=True, null=True)
#    weightloss = models.IntegerField(blank=True, null=True)
#    pass_status = models.CharField(max_length=100, blank=True, null=True)
#    site_time = models.DateTimeField()
#    shift = models.CharField(max_length=1)
#
#    class Meta:
#        ordering = ['-timestamp']
#        unique_together = ('machine_id', 'timestamp')





class ShiftDataSession(models.Model):
    shift = models.CharField(max_length=1, default="1")
    shift_time = models.DateTimeField(auto_now=True)

    def toDic(self):
        return {"shift": self.shift, "shift_time": self.shift_time}


class Unit(models.Model):
    unit = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.unit

    def toDic(self):
        return {"unit": self.unit}

class PlantLocation(models.Model):
    location_city = models.CharField(max_length=100)
    location_state = models.CharField(max_length=100)
    location_country = models.CharField(max_length=100)
    plant_name = models.CharField(max_length=100)

    def __str__(self):
        return self.plant_name

    def toDic(self):
        return {"location_city": self.location_city, "location_state": self.location_state, "location_country": self.location_country, "plant_name": self.plant_name}


class Machine(models.Model):
    machine_id = models.CharField(max_length=100, unique=True)
    plant_name = models.ForeignKey('PlantLocation', on_delete=models.CASCADE)
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.machine_id

    def toDic(self):
        return {"machine_id": self.machine_id, "plant_name": self.plant_name}


class BasicMetarialStandard(models.Model):
    basic_metarial = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.basic_metarial

    def toDic(self):
        return {"basic_metarial": self.basic_metarial, "code": str(self.code)}


class StandardTypeClassification(models.Model):
    basic_metarial = models.ForeignKey('BasicMetarialStandard', on_delete=models.CASCADE)
    standard_type_classification = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.standard_type_classification

    def toDic(self):
        return {"basic_metarial": self.basic_metarial, "standard_type_classification": self.standard_type_classification, "code": str(self.code)}
    

class PressureTypeSpecification(models.Model):
    basic_metarial = models.ForeignKey('BasicMetarialStandard', on_delete=models.CASCADE)
    standard_type_classification = models.ForeignKey('StandardTypeClassification', on_delete=models.CASCADE)
    pressure_type_specification = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.pressure_type_specification

    def toDic(self):
        return {"basic_metarial": self.basic_metarial, "standard_type_classification": self.standard_type_classification, "pressure_type_specification": self.pressure_type_specification, "code": str(self.code)}


class PipeOuterDiameter(models.Model):
    standard_type_classification = models.ForeignKey('StandardTypeClassification', on_delete=models.CASCADE)
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE)
    outer_diameter = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    def toDic(self):
        return {"standard_type_classification": self.standard_type_classification, "unit": self.unit, "outer_diameter": self.outer_diameter, "code": str(self.code)}


class PipeLength(models.Model):
    standard_type_classification = models.ForeignKey('StandardTypeClassification', on_delete=models.CASCADE)
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE)
    length = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    def toDic(self):
        return {"standard_type_classification": self.standard_type_classification, "unit": self.unit, "length": self.length, "code": str(self.code)}


class PipeShiftDuration(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
    shift_date = models.DateField()
    shift_1 = models.DurationField(default=timedelta(minutes=480))
    shift_1_downtime = models.DurationField(default=timedelta(minutes=0))
    shift_2 = models.DurationField(default=timedelta(minutes=480))
    shift_2_downtime = models.DurationField(default=timedelta(minutes=0))
    shift_3 = models.DurationField(default=timedelta(minutes=480))
    shift_3_downtime = models.DurationField(default=timedelta(minutes=0))

    class Meta:
        unique_together = ('user', 'shift_date')

    def toDic(self):
        return {"user": self.user, "shift_date": self.shift_date, "shift_1": self.shift_1, "shift_1_downtime": self.shift_1_downtime, "shift_2": self.shift_2, "shift_2_downtime": self.shift_2_downtime, "shift_3": self.shift_3, "shift_3_downtime": self.shift_3_downtime}

class MachineStatus(models.Model):
    machine_id = models.OneToOneField('Machine', on_delete=models.CASCADE)
    active_date_time = models.DateTimeField()

    def toDic(self):
        return {"machine_id": self.machine_id, "active_date_time": self.active_date_time}
    
    def timeDifference(self):
        return int((timezone.localtime(timezone.now()) - timezone.localtime(self.active_date_time)).total_seconds())


class MetarialIssueShift(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
    shift_date = models.DateField()
    shift_1 = models.IntegerField(blank=True, null=True, default=0)
    shift_2 = models.IntegerField(blank=True, null=True, default=0)
    shift_3 = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        unique_together = ('user', 'shift_date')

    def toDic(self):
        return {"user": self.user, "shift_date": self.shift_date, "shift_1": self.shift_1, "shift_2": self.shift_2, "shift_3": self.shift_3}
