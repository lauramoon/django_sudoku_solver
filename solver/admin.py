from django.contrib import admin
from .models import BoxValue, Parent

# Register your models here.


@admin.register(BoxValue)
class BoxValueAdmin(admin.ModelAdmin):
    ordering = ('parent', 'box_index', 'box_value')


class BoxValueInstanceInline(admin.TabularInline):
    model = BoxValue
    extra = 0
    max_num = 81
    fields = ('box_value',)


@admin.register(Parent)
class BookAdmin(admin.ModelAdmin):
    inlines = [BoxValueInstanceInline]
    readonly_fields = ('puzzle_string', 'puzzle_solution', 'solved')
    list_display = ('name',)

