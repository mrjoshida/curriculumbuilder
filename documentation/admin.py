from django.contrib import admin
from django.db import models
from django.forms import Textarea, ModelForm
from mezzanine.core.admin import StackedDynamicInlineAdmin, TabularDynamicInlineAdmin
from mezzanine.pages.admin import PageAdmin

from documentation.models import Block, IDE, Category, Parameter, Example


class CategoryInline(TabularDynamicInlineAdmin):
    model = Category
    verbose_name = "Category"
    verbose_name_plural = "Categories"
    extra = 3


class ParameterInline(StackedDynamicInlineAdmin):
    model = Parameter
    extra = 3


class ExampleInline(StackedDynamicInlineAdmin):
    model = Example
    extra = 3


class IDEAdmin(PageAdmin):
    model = IDE

    inlines = [CategoryInline, ]

    fieldsets = (
        (None, {
            'fields': ['title', 'slug', 'keywords', ('description', 'gen_description')],
        }),
        ('Documentation', {
            'fields': ['url', 'content'],
        }),
    )


class BlockForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BlockForm, self).__init__(*args, **kwargs)

        if self.instance.parent:
            categories_queryset = Category.objects.filter(IDE=self.instance.parent.ide)
        else:
            categories_queryset = Category.objects.all()

        self.fields['category'].queryset = categories_queryset


class BlockAdmin(PageAdmin):
    form = BlockForm

    inlines = [ParameterInline, ExampleInline]

    fieldsets = (
        (None, {
            'fields': ['title', 'slug', 'keywords', ('description', 'gen_description')],
        }),
        ('Documentation', {
            'fields': ['proxy', 'ext_doc', 'category', 'content'],
        }),
        ('Details', {
            'fields': ['syntax', 'return_value'],
            'classes': ['collapse-closed'],
        }),
        ('Tips', {
            'fields': ['tips', ],
            'classes': ['collapse-closed'],
        }),
    )

    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows': 2})},
    }


class MultiBlockForm(ModelForm):
    class Meta:
        model = Block
        fields = ['IDE', 'title', 'category', 'ext_doc', 'proxy']


class MultiBlock(Block):
    class Meta:
        proxy = True


class MultiBlockAdmin(admin.ModelAdmin):
    list_display = ('IDE', 'title', 'category', 'ext_doc')
    list_editable = ('title', 'category', 'ext_doc')
    list_filter = ('IDE',)

    def get_changelist_form(self, request, **kwargs):
        return MultiBlockForm


admin.site.register(Block, BlockAdmin)
admin.site.register(IDE, IDEAdmin)
admin.site.register(MultiBlock, MultiBlockAdmin)
