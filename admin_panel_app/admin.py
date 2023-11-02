from django.contrib import admin
from admin_panel_app.models import EmployeeModel, MoreDetailsEmployeeModel, GroupDepartmentModel, CityDepModel, \
    CommandNumberModel, JobTitleModel, CanEditEmployee


class EmployeeAdmin(admin.ModelAdmin):
    # list_display = ("author", "text_task")
    ordering = ["last_name", "first_name", "middle_name"]
    search_fields = ["last_name", "first_name", "middle_name", "personnel_number", "user_phone"]
    list_filter = ("department_group", "department")


class MoreDetailsEmployeeAdmin(admin.ModelAdmin):
    # list_display = ("author", "text_task")
    ordering = ["emp"]
    search_fields = ["emp__last_name"]
    list_filter = ("emp__department_group", "emp__department")
    # list_filter = ("author", "task_number")


class CommandNumberAdmin(admin.ModelAdmin):
    ordering = ["command_number"]
    list_filter = ("department",)

class GroupDepartmentAdmin(admin.ModelAdmin):
    ordering = ["group_dep_abr"]

class JobTitleAdmin(admin.ModelAdmin):
    ordering = ["job_title"]

admin.site.register(EmployeeModel, EmployeeAdmin)
admin.site.register(MoreDetailsEmployeeModel, MoreDetailsEmployeeAdmin)
admin.site.register(GroupDepartmentModel, GroupDepartmentAdmin)
admin.site.register(CityDepModel)
admin.site.register(CommandNumberModel, CommandNumberAdmin)
admin.site.register(JobTitleModel, JobTitleAdmin)
admin.site.register(CanEditEmployee)

# Register your models here.
