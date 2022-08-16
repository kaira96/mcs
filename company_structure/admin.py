from django.contrib import admin

from .models import (City, Region, Address, WorkTime,
                     OfficeBranch, Department,  Position, Holiday)


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_date',)
    search_fields = ('name',)
    list_filter = ('created_date', )


class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_date',)
    search_fields = ('name',)
    list_filter = ('created_date', )
    

class AddressAdmin(admin.ModelAdmin):
    list_display = ('city', 'region', 'street', 'created_date',)
    search_fields = ('city', 'region', 'street',)
    list_filter = ('created_date', )


class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'is_active')
    search_fields = ('name', 'department__name')
    list_filter = ('department__name', )
    


class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'is_active')
    search_fields = ('name', 'department__name')
    list_filter = ('department__name', )


class DepartmentInline(admin.TabularInline):
    model = OfficeBranch.departments.through


class OfficeBranchAdmin(admin.ModelAdmin):
    list_display = ('address', 'phone_number', 'name')
    search_fields = ('address__city__name', 'address__region__name', 'name')
    date_hierarchy = 'created_date'
    inlines = (DepartmentInline, )
    exclude = ('departments', )
    list_filter = ('address__city__name', 'address__region__name', 'is_working')


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', )
    search_fields = ('name', )
    date_hierarchy = 'start_date'


class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'is_active')
    search_fields = ('name', 'department__name')
    list_filter = ('department__name', )


class HolidayAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'created_date')
    search_fields = ('name',)
    date_hierarchy = 'created_date'
    list_filter = ('name', 'date')
    

class WorkTimeAdmin(admin.ModelAdmin):
    list_display = ('branch', 'start_time', 'end_time', 'created_date')
    search_fields = ('created_date',)
    list_filter = ('start_time', 'end_time')


admin.site.register(City, CityAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(OfficeBranch, OfficeBranchAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Holiday, HolidayAdmin)
admin.site.register(WorkTime, WorkTimeAdmin)
