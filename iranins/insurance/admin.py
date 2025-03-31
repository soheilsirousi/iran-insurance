from django.contrib import admin
from insurance.models import InsuredAttributeValue, Insurance, Category, Insured, Attribute


class InsuredAttributeValueInline(admin.TabularInline):
    model = InsuredAttributeValue
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Insured)
class InsuredAdmin(admin.ModelAdmin):
    list_display = ('owner', 'category', 'name')
    inlines = (InsuredAttributeValueInline, )


@admin.register(Insurance)
class InsuranceAdmin(admin.ModelAdmin):
    list_display = ('insurance_number', 'insurer', 'insured', 'insurance_type', 'start_at', 'end_at', 'amount')


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name', )





