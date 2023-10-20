from .models import EmployeeModel, MoreDetailsEmployeeModel, JobTitleModel, GroupDepartmentModel, CommandNumberModel, \
    CityDepModel
from django.forms import Form, ModelForm, ModelChoiceField, Select, CharField, TextInput


class FilterForm(Form):
    department_field = ModelChoiceField(widget=Select(attrs={"class": "form-select form-control-blue"}),
                                        queryset=GroupDepartmentModel.objects.filter(show=True).order_by('group_dep_abr'),
                                        empty_label="Управление",
                                        required=False)
    search_text_field = CharField(widget=TextInput(attrs={"class": "form-control form-control-blue",
                                                          "placeholder": "Поиск по имени"}), required=False)

