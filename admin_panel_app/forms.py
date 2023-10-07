from .models import EmployeeModel, MoreDetailsEmployeeModel, User, CommandNumberModel, GroupDepartmentModel
from django.forms import ModelForm, TextInput, Textarea, CheckboxInput, Select, ChoiceField, Form, PasswordInput, \
    CharField, ModelChoiceField, modelformset_factory, ModelMultipleChoiceField, MultipleChoiceField, SelectMultiple, \
    FileField, ClearableFileInput, FileInput, DateTimeField, DateTimeInput, EmailInput, DateInput, NumberInput
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm


class EmployeeForm(ModelForm):
    class Meta:
        model = EmployeeModel
        # fields = '__all__'
        exclude = ['user', ]
        widgets = {'last_name': TextInput(attrs={"class": "form-control",
                                                 "aria-label": "Фамилия",
                                                 "placeholder": "Фамилия"}),
                   'first_name': TextInput(attrs={"class": "form-control",
                                                  "aria-label": "Имя",
                                                  "placeholder": "Имя"}),
                   'middle_name': TextInput(attrs={"class": "form-control",
                                                   "aria-label": "Отчество",
                                                   "placeholder": "Отчество"}),
                   'personnel_number': TextInput(attrs={"class": "form-control",
                                                        "aria-label": "Табельный номер",
                                                        "placeholder": "Табельный номер"}),
                   "job_title": Select(attrs={"class": "form-select",
                                              "aria-label": "Должность"}),
                   "department_group": Select(attrs={"class": "form-select",
                                                     "aria-label": "Управление"}),
                   "department": Select(attrs={"class": "form-select",
                                               "aria-label": "Управление"}),
                   'user_phone': NumberInput(attrs={"class": "form-control",
                                                    "aria-label": "Внутренний телефон",
                                                    "placeholder": "Внутренний телефон",
                                                    # 'type':"number",
                                                    }),
                   'right_to_sign': CheckboxInput(),
                   'check_edit': CheckboxInput(),
                   'can_make_task': CheckboxInput(),
                   'cpe_flag': CheckboxInput(),
                   'mailing_list_check': CheckboxInput(),
                   'work_status': CheckboxInput(),
                   }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].queryset = CommandNumberModel.objects.filter(show=True).order_by('command_number')
        self.fields['department_group'].queryset = GroupDepartmentModel.objects.filter(show=True).order_by(
            'group_dep_abr')


class DateInputNew(DateInput):
    input_type = 'date'


class MoreDetailsEmployeeForm(ModelForm):
    class Meta:
        model = MoreDetailsEmployeeModel
        # fields = '__all__'
        exclude = ['emp', ]
        widgets = {'mobile_phone': TextInput(attrs={"class": "form-control",
                                                    "aria-label": "Мобильный телефон",
                                                    "placeholder": "Мобильный телефон"}),
                   'city_dep': Select(attrs={"class": "form-select",
                                             "aria-label": "Город/Подразделение"}),
                   'date_birthday': DateInputNew(format='%Y-%m-%d',
                                                 attrs={"class": "form-control datepicker",
                                                        "aria-label": "День рождения"}),
                   'date_birthday_show': CheckboxInput(),
                   'photo': ClearableFileInput(attrs={"class": "form-control",
                                                      'placeholder': 'Фотография',
                                                      }),
                   'outside_email': EmailInput(attrs={"class": "form-control", "placeholder": "Внешняя почта"}),
                   'room': TextInput(attrs={"class": "form-control",
                                            "aria-label": "Кабинет",
                                            "placeholder": "Кабинет"}),
                   }


class UserRegistration(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']
        widgets = {"username": TextInput(attrs={"class": "form-control",
                                                "aria-label": "Имя пользователя",
                                                "placeholder": "Login"}),
                   'email': EmailInput(attrs={"class": "form-control", "placeholder": "Внутренняя почта"}),
                   "password1": PasswordInput(
                       attrs={"autocomplete": "current-password", "class": "form-control", 'placeholder': 'Пароль'}),
                   "password2": PasswordInput(
                       attrs={"autocomplete": "current-password", "class": "form-control",
                              'placeholder': 'Пароль подтверждение'}),
                   }

    def __init__(self, *args, **kwargs):
        super(UserRegistration, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class NewGroupDepForm(ModelForm):
    class Meta:
        model = GroupDepartmentModel
        fields = '__all__'
        widgets = {'group_dep_abr': TextInput(attrs={"class": "form-control",
                                                     "aria-label": "Сокращение",
                                                     "placeholder": "Сокращение"}),
                   'group_dep_name': TextInput(attrs={"class": "form-control",
                                                      "aria-label": "Полное наименование",
                                                      "placeholder": "Полное наименование"}),
                   'show': CheckboxInput()}


class NewCommandForm(ModelForm):
    class Meta:
        model = CommandNumberModel
        fields = '__all__'
        widgets = {'command_number': NumberInput(attrs={"class": "form-control",
                                                        "aria-label": "Номер отдела",
                                                        "placeholder": "Номер отдела"}),
                   'command_name': TextInput(attrs={"class": "form-control",
                                                    "aria-label": "Полное наименование",
                                                    "placeholder": "Полное наименование"}),
                   'department': Select(attrs={"class": "form-select",
                                               "aria-label": "Управление",
                                               "placeholder": "Выбрать управление"}),
                   'show': CheckboxInput()}

    #
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].queryset = GroupDepartmentModel.objects.filter(show=True).order_by(
            'group_dep_abr')
