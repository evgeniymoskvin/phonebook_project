from django.contrib import admin
from admin_panel_app.models import EmployeeModel,MoreDetailsEmployeeModel,GroupDepartmentModel,CityDepModel, CommandNumberModel,JobTitleModel,CanEditEmployee

class EmployeeAdmin(admin.ModelAdmin):
    # list_display = ("author", "text_task")
    ordering = ["last_name"]
    search_fields = ["user"]
    # list_filter = ("author", "task_number")

class MoreDetailsEmployeeAdmin(admin.ModelAdmin):
    # list_display = ("author", "text_task")
    ordering = ["emp"]
    search_fields = ["emp"]
    # list_filter = ("author", "task_number")

class CommandNumberAdmin(admin.ModelAdmin):
    ordering = ["command_number"]

admin.site.register(EmployeeModel, EmployeeAdmin)
admin.site.register(MoreDetailsEmployeeModel, MoreDetailsEmployeeAdmin)
admin.site.register(GroupDepartmentModel)
admin.site.register(CityDepModel)
admin.site.register(CommandNumberModel, CommandNumberAdmin)
admin.site.register(JobTitleModel)
admin.site.register(CanEditEmployee)

# Register your models here.
