from django.contrib import admin
from .models import Product, ReviewRating, ProductGallery
import admin_thumbnails
from django.http import HttpResponse
from weasyprint import HTML, CSS
from django.template.loader import get_template
from django.contrib.admin.models import LogEntry


def generar_pdf(modeladmin, request, queryset):

    context = {
        'queryset': queryset,
    }

    template = get_template('adminTemplate/productspdf.html')
    html = template.render(context)
    css = './bodegon/static/css/bootstrap.css'
    pdf = HTML(string=html).write_pdf(stylesheets=[CSS(css)])

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=productos.pdf'
    response.write(pdf)

    return response

generar_pdf.short_description = "Generar PDF seleccionado(s)"

def generar_auditoria(modeladmin, request, queryset):
    logs = LogEntry.objects.filter(content_type_id = 8)
    context = {
        'logs': logs,
        'titulo': 'Productos'
    }
    template = get_template('adminTemplate/auditoriapdf.html')
    html = template.render(context)
    css = './bodegon/static/css/bootstrap.css'
    pdf = HTML(string=html).write_pdf(stylesheets=[CSS(css)])

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=productos_auditoria.pdf'
    response.write(pdf)
    return response
generar_auditoria.short_description = 'Generar auditoria'

@admin_thumbnails.thumbnail('image')
class ProductGalleryInLine(admin.TabularInline):
    model = ProductGallery
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [ProductGalleryInLine]
    actions = [generar_pdf, generar_auditoria]

admin.site.register(Product, ProductAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)