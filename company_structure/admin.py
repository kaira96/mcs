from django.contrib import admin

from .models import (City, Region, Address,
                     OfficeBranch, Department,  Position, Holiday)


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
    ordering = ('-date',)


admin.site.register(City)
admin.site.register(Region)
admin.site.register(Address)
admin.site.register(OfficeBranch, OfficeBranchAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Holiday, HolidayAdmin)
