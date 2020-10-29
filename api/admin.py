from django.contrib import admin


from .models import *

admin.site.site_header = "Pipe Weight Tracker Site Administration"

# Register your models here.
class UnitAdmin(admin.ModelAdmin):
    list_display = ('unit',)
admin.site.register(Unit, UnitAdmin)

class PipeShiftDurationAdmin(admin.ModelAdmin):
    list_display = ('user', 'shift_date', 'shift_1', 'shift_1_downtime', 'shift_2', 'shift_2_downtime', 'shift_3', 'shift_3_downtime',)
admin.site.register(PipeShiftDuration, PipeShiftDurationAdmin)

class MachineStatusAdmin(admin.ModelAdmin):
    list_display = ('machine_id', 'active_date_time')
admin.site.register(MachineStatus, MachineStatusAdmin)

class PlantLocationAdmin(admin.ModelAdmin):
    list_display = ('location_city', 'location_state', 'location_country', 'plant_name')
admin.site.register(PlantLocation, PlantLocationAdmin)

class MachineAdmin(admin.ModelAdmin):
    list_display = ('machine_id', 'plant_name', 'user')
admin.site.register(Machine, MachineAdmin)

class BasicMetarialStandardAdmin(admin.ModelAdmin):
    list_display = ('basic_metarial', 'code')
admin.site.register(BasicMetarialStandard, BasicMetarialStandardAdmin)

class StandardTypeClassificationAdmin(admin.ModelAdmin):
    list_display = ('basic_metarial', 'standard_type_classification', 'code')
admin.site.register(StandardTypeClassification, StandardTypeClassificationAdmin)

class PressureTypeSpecificationAdmin(admin.ModelAdmin):
    list_display = ('basic_metarial', 'standard_type_classification', 'pressure_type_specification', 'code')
admin.site.register(PressureTypeSpecification, PressureTypeSpecificationAdmin)

class PipeOuterDiameterAdmin(admin.ModelAdmin):
    list_display = ('standard_type_classification', 'unit', 'outer_diameter', 'code')
admin.site.register(PipeOuterDiameter, PipeOuterDiameterAdmin)

class PipeLengthAdmin(admin.ModelAdmin):
    list_display = ('standard_type_classification', 'unit', 'length', 'code')
admin.site.register(PipeLength, PipeLengthAdmin)

class PipeDataAdmin(admin.ModelAdmin):
    list_display = ('mid', 'b', 'c', 'd', 'e', 'ts', 'count', 'weight', 'ps', 'site_time', 'shift')
    def has_add_permission(self, request, obj=None):
        return False
admin.site.register(PipeData, PipeDataAdmin)

class PipeDataProcessedAdmin(admin.ModelAdmin):
    list_display = ('machine_id', 'basic_metarial', 'standard_type_classification', 'pressure_type_specification', 'outer_diameter', 'outer_diameter_unit', 'length', 'length_unit', 'timestamp', 'count', 'weight', 'maxweight', 'minweight', 'weightgain', 'weightloss', 'pass_status', 'site_time', 'shift')
admin.site.register(PipeDataProcessed, PipeDataProcessedAdmin)


class MetarialIssueShiftAdmin(admin.ModelAdmin):
    list_display = ('user', 'shift_date', 'shift_1', 'shift_2', 'shift_3')
admin.site.register(MetarialIssueShift, MetarialIssueShiftAdmin)

