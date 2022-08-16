from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import PasswordResetForm

from .forms import UserCreationForm
from .models import (
    Employee, Salary, SalaryHistory, 
    DisciplinaryAction, Bonus, BonusHistory, 
    PositionHistory, DisciplinaryActionHistory
    )


class PositionHistoryTabularInlineAdmin(admin.TabularInline):
    model = PositionHistory
    extra = 1
    max_num = 1
    can_delete = False

    fields = ('position',)
    editable = False
    ordering = ('-end_date', )
    
    
class SalaryTabularInlineAdmin(admin.TabularInline):
    model = Salary
    extra = 1
    max_num = 1
    can_delete = False

    fields = ('salary',)
    editable = False


class PositionHistoryAdmin(admin.ModelAdmin):
    list_display = ('employee', 'position', 'is_current', 'start_date', 'end_date')
    search_fields = ('employee__first_name', 'employee__last_name', 'employee__middle_name',
                     'employee__login', 'position__name',)
    list_filter = ('position__name', )


class DisciplinaryActionAdmin(admin.TabularInline):
    model = DisciplinaryAction
    extra = 1
    max_num = 1
    can_delete = False

    fields = ('disciplinary_action_amount', 'disciplinary_action_period')
    editable = False
    ordering = ('-end_date', )
    

class EmployeeAdmin(UserAdmin):
    add_form = UserCreationForm

    list_display = ('login', 'full_name', 'status', 'position', 'created_date', 'updated_date')
    search_fields = ('first_name', 'last_name')
    date_hierarchy = 'created_date'
    inlines = (SalaryTabularInlineAdmin, PositionHistoryTabularInlineAdmin, DisciplinaryActionAdmin)
    list_filter = ('status', 'office_branch')
    readonly_fields = ('full_name', 'position')

    fieldsets = (
        (None, {
            'fields': (
                'login', 'password', 'status', 'first_name', 'last_name', 'middle_name', 'img',
                'office_branch', 'full_name', 'position', 'address',
                'date_of_birth', 'passport', 'phone_number', 'email','registration_address', 'gender',
                'is_married', 'is_criminal_record', 'education_status', 'is_beneficiary',
                'is_political_man'
                )
            }
         ),
        ('Права доступа', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'first_name', 'last_name', 'middle_name', 'img', 'office_branch', 'address',
                'date_of_birth', 'passport', 'phone_number', 'email', 'registration_address', 'gender',
                'is_married', 'is_criminal_record', 'education_status', 'is_beneficiary',
                'is_political_man'
                )
            }
         ),
        ('Пароль', {
            'description': "По желанию здесь можно задать пароль сотрудника",
            'fields': ('password1', 'password2'),
            'classes': ('collapse', 'collapse-closed'),
        }),
    )
    ordering = ('login',)
    filter_horizontal = ()

    def save_model(self, request, obj, form, change):
        if not change and (not form.cleaned_data['password1'] or not obj.has_usable_password()):
            # Django's PasswordResetForm won't let us reset an unusable
            # password. We set it above super() so we don't have to save twice.
            obj.set_password('default')
            reset_password = True
        else:
            reset_password = False

        super(UserAdmin, self).save_model(request, obj, form, change)
    

class SalaryAdmin(admin.ModelAdmin):
    list_display = ('employee', 'salary', 'updated_date')
    search_fields = ('employee',)
    date_hierarchy = 'created_date'
    ordering = ('-updated_date',)


class SalaryHistoryAdmin(admin.ModelAdmin):
    list_display = ('employee', 'salary', 'is_current','start_date', 'end_date', 'created_date')
    search_fields = ('employee',)
    date_hierarchy = 'created_date'
    list_filter = ('employee', 'is_current')
    ordering = ('-updated_date',)


class BonusAdmin(admin.ModelAdmin):
    list_display = ('bonus_amount', 'min_credit_quantity', 'position', 'updated_date')
    search_fields = ('position',)
    list_filter = ('position',)
    date_hierarchy = 'created_date'
    ordering = ('-updated_date',)


class BonusHistoryAdmin(admin.ModelAdmin):
    list_display = ('position', 'bonus_amount', 'min_credit_quantity', 'is_active','start_date', 'end_date')
    search_fields = ('position',)
    date_hierarchy = 'created_date'
    list_filter = ('is_active', 'position')
    ordering = ('-updated_date',)


class DisciplinaryActionAdmin(admin.ModelAdmin):
    list_display = ('disciplinary_action_amount', 'employee', 'disciplinary_action_period', 'is_active', 'end_date')
    search_fields = ('employee_id',)
    date_hierarchy = 'created_date'
    list_filter = ('is_active', 'employee_id')
    ordering = ('-updated_date',)
    
    
class DisciplinaryActionHistoryAdmin(admin.ModelAdmin):
    list_display = ('disciplinary_action_amount', 'employee', 'disciplinary_action_period', 'is_active', 'end_date')
    search_fields = ('employee_id',)
    date_hierarchy = 'created_date'
    list_filter = ('is_active', 'employee_id')
    ordering = ('-updated_date',)
    
    
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(PositionHistory, PositionHistoryAdmin)
admin.site.register(Salary, SalaryAdmin)
admin.site.register(SalaryHistory, SalaryHistoryAdmin)
admin.site.register(Bonus, BonusAdmin)
admin.site.register(BonusHistory, BonusHistoryAdmin)
admin.site.register(DisciplinaryAction, DisciplinaryActionAdmin)
admin.site.register(DisciplinaryActionHistory, DisciplinaryActionHistoryAdmin)
