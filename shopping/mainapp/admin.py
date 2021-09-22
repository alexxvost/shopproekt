from django import forms
from django.forms import ModelForm, ModelChoiceField
from django.contrib import admin
from .models import *


class BookAdminForm(ModelForm):

    MIN_RESOLUTION = (500, 500)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].help_text = " Минимальное разрешение {} x {}".format(
            *self.MIN_RESOLUTION
        )


class BookCategoryChoiceField(forms.ModelChoiceField):
    pass


class BookAdmin(admin.ModelAdmin):

    form = BookAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            return BookCategoryChoiceField(Category.objects.filter(slug="Book"))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class PenCategoryChoiceField(forms.ModelChoiceField):
    pass


class PenAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            return PenCategoryChoiceField(Category.objects.filter(slug="Pen"))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SketchCategoryChoiceField(forms.ModelChoiceField):
    pass


class SketchAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            return PenCategoryChoiceField(Category.objects.filter(slug="Sketch"))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Sketch, SketchAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Pen, PenAdmin)
