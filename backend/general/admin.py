from django.contrib.admin import register, site, ModelAdmin, TabularInline, StackedInline
from django.contrib.auth.models import Group
from import_export.admin import ImportExportModelAdmin, ImportExportMixin

from general.models import (
    User,
    Department,
    AcademicYear,
    StudyYearIb,
    StudyYear,
    ClassGroup,
    ClassGroupRole
)

from apps.curriculum.models import (
    TeachingLoad
)

from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from rangefilter.filters import DateRangeFilter

class CustomUserCreationForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email',)  # Use 'email' as the username

class CustomUserChangeForm(UserChangeForm):
    
    class Meta(UserChangeForm.Meta):
        model = User

site.unregister(Group)

class TeachingInline(TabularInline):  # StackedInline, TabularInline
    autocomplete_fields = (
        'subject',
    )
    # filter_horizontal = (
    #     'groups',
    # )
    model = TeachingLoad
    extra = 1

class CustomUserAdmin(BaseUserAdmin, ImportExportModelAdmin):
    inlines = [TeachingInline]
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "last_activity",
    )
    readonly_fields = (
        "date_joined",
        "last_login",
        "last_activity",
        "display_classes",
        "display_departments",
    )
    list_display_links = (
        "first_name",
        "last_name",
        "email",
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'password1', 'password2')}),
        (
            "Личные данные", {
                "fields": (
                    "last_name",
                    "first_name",
                    "middle_name",
                    "gender",
                    "photo",
                )
            }
        ),
        (
            "Связь с Дневник.РУ", {
                "fields": (
                    "dnevnik_token",
                    "dnevnik_id", 
                )
            }
        ),
    )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            "Личные данные", {
                "fields": (
                    "last_name",
                    "first_name",
                    "middle_name",
                    "gender",
                    "photo",
                    "display_classes",
                    "display_departments",
                    "groups",
                )
            }
        ),
        (
            "Связь с Дневник.РУ", {
                "fields": (
                    "dnevnik_token",
                    "dnevnik_id", 
                    "dnevnik_user_id",
                )
            }
        ),
        (
            "Статусы", {
                "classes": (
                    "collapse",
                ),
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "is_active",
                )
            }
        ),
        (
            "Даты", {
                "fields": (
                    "date_joined",
                    "last_login",
                    "last_activity",
                )
            }
        )
    )
    search_fields = (
        "last_name",
        "first_name",
        "email",
    )
    list_filter = (
        "is_active",
        "groups",
        ("last_activity", DateRangeFilter),
    )
    # Удалите ordering, если не используете сортировку
    ordering = ('email',)
    exclude = ('username',)
    def display_classes(self, obj):
        return ", ".join([f"{cl.name} ({cl.year_academic})" for cl in obj.classes.all()])
    display_classes.short_description = 'Классы'
    def display_departments(self, obj):
        return ", ".join([f"{dp.name}" for dp in obj.departments.all()])
    display_departments.short_description = 'Подразделение'

site.register(User, CustomUserAdmin)

@register(Group)
class UserModelAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "name",
    )
    list_display_links = (
        "name",
    )

@register(Department)
class DepartmentModelAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "name",
        "count",
    )
    list_display_links = (
        "name",
    )
    filter_horizontal = ('employees',)
    fields = (
        "name",
        "logo",
        "employees",
    )

@register(AcademicYear)
class AcademicYearModelAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "name",
        "date_start",
        "date_end",
    )
    list_display_links = (
        "name",
    )

@register(StudyYearIb)
class StudyYearIbModelAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "number",
        "name",
        "program_ib",
    )
    list_display_links = (
        "name",
    )

@register(StudyYear)
class StudyYearModelAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "number",
        "ib",
        "level",
    )
    list_display_links = (
        "number",
    )

class ClassGroupRoleInline(TabularInline):  # StackedInline, TabularInline
    model = ClassGroupRole
    extra = 1
    autocomplete_fields = ['user']


@register(ClassGroup)
class ClassGroupModelAdmin(ImportExportModelAdmin):
    inlines = [ClassGroupRoleInline]
    list_display = (
        "id",
        "year_academic",
        "name",
        "year_study",
        "year_study_ib",
        "mentor",
        "dnevnik_id",
        "curriculum",
        "count",
    )
    list_display_links = (
        "name",
    )
    filter_horizontal = ('students',)
    fields = (
        "year_academic",
        "year_study",
        "year_study_ib",
        "letter",
        "dnevnik_id",
        "mentor",
        "students",
        "curriculum",
    )
    autocomplete_fields = ['mentor']
    

@register(ClassGroupRole)
class ClassGroupRoleModelAdmin(ModelAdmin):
    list_display = (
        "user",
        "group",
        "role"
    )
    list_display_links = (
        "user",
    )
    fields = (
        "user",
        "group",
        "role"
    )