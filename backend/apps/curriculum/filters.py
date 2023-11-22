from admin_auto_filters.filters import AutocompleteFilter

class SubjectFilter(AutocompleteFilter):
    title = 'Предмет'
    field_name = 'subject'