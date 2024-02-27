from django.contrib import admin
from admin_panel_app.models import EmployeeModel, MoreDetailsEmployeeModel, GroupDepartmentModel, CityDepModel, \
    CommandNumberModel, JobTitleModel, CanEditEmployee, StatsEmployeeModel


class EmployeeAdmin(admin.ModelAdmin):
    # list_display = ("author", "text_task")
    ordering = ["last_name", "first_name", "middle_name"]
    search_fields = ["last_name", "first_name", "middle_name", "personnel_number", "user_phone"]
    list_filter = ("department_group__city_dep__city", "department_group__group_dep_abr", "department__command_number")


class MoreDetailsEmployeeAdmin(admin.ModelAdmin):
    ordering = ["emp__last_name", "emp__first_name", "emp__middle_name"]
    search_fields = ["emp__last_name", "emp__first_name", "emp__middle_name"]
    list_filter = ("emp__department_group__city_dep__city", "emp__department_group__group_dep_abr", "emp__department__command_number")
    # list_filter = ("author", "task_number")


class CommandNumberAdmin(admin.ModelAdmin):
    ordering = ["command_number"]
    list_filter = ("department__group_dep_abr", "department__city_dep__city")

class GroupDepartmentAdmin(admin.ModelAdmin):
    ordering = ["group_dep_abr"]
    list_filter = ("city_dep__city", "show")

class JobTitleAdmin(admin.ModelAdmin):
    ordering = ["job_title"]

class CanEditEmployeeAdmin(admin.ModelAdmin):
    ordering = ["emp__last_name", "emp__first_name", "emp__middle_name"]
    search_fields = ["emp__last_name", "emp__first_name", "emp__middle_name"]

admin.site.register(EmployeeModel, EmployeeAdmin)
admin.site.register(MoreDetailsEmployeeModel, MoreDetailsEmployeeAdmin)
admin.site.register(GroupDepartmentModel, GroupDepartmentAdmin)
admin.site.register(CityDepModel)
admin.site.register(CommandNumberModel, CommandNumberAdmin)
admin.site.register(JobTitleModel, JobTitleAdmin)
admin.site.register(CanEditEmployee, CanEditEmployeeAdmin)
admin.site.register(StatsEmployeeModel)

# Register your models here.
