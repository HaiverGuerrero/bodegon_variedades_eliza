from django.contrib import admin
from .models import Category
from django.http import HttpResponse
from weasyprint import HTML, CSS
from django.template.loader import get_template
from django.contrib.admin.models import LogEntry

# Register your models here.

def generar_pdf(modeladmin, request, queryset):

    context = {
        'queryset': queryset,
    }

    template = get_template('adminTemplate/categoriespdf.html')
    html = template.render(context)
    css = './bodegon/static/css/bootstrap.css'
    pdf = HTML(string=html).write_pdf(stylesheets=[CSS(css)])

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=categorias.pdf'
    response.write(pdf)

    return response

generar_pdf.short_description = "Generar PDF seleccionado(s)"

def generar_auditoria(modeladmin, request, queryset):
    logs = LogEntry.objects.filter(content_type_id = 1)
    context = {
        'logs': logs,
        'titulo': 'Categorias'
    }
    template = get_template('adminTemplate/auditoriapdf.html')
    html = template.render(context)
    css = './bodegon/static/css/bootstrap.css'
    pdf = HTML(string=html).write_pdf(stylesheets=[CSS(css)])

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=categorias_auditoria.pdf'
    response.write(pdf)
    return response
generar_auditoria.short_description = 'Generar auditoria'

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug')
    list_filter = ('category_name',)
    actions = [generar_pdf, generar_auditoria]

admin.site.register(Category, CategoryAdmin)