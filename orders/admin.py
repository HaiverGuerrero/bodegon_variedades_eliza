from django.contrib import admin
from .models import Payment, Order, OrderProduct
from django.http import HttpResponse
from weasyprint import HTML, CSS
from django.template.loader import get_template
from django.contrib.admin.models import LogEntry



def generar_pdf(modeladmin, request, queryset):
    context = {
        'queryset': queryset,
    }

    template = get_template('adminTemplate/orderspdf.html')
    html = template.render(context)
    css = './bodegon/static/css/bootstrap.css'
    pdf = HTML(string=html).write_pdf(stylesheets=[CSS(css)])

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=ordenes.pdf'
    response.write(pdf)

    return response

generar_pdf.short_description = "Generar PDF seleccionado(s)"

def generar_auditoria(modeladmin, request, queryset):
    logs = LogEntry.objects.filter(content_type_id = 13)
    context = {
        'logs': logs,
        'titulo': 'Ordenes'
    }
    template = get_template('adminTemplate/auditoriapdf.html')
    html = template.render(context)
    css = './bodegon/static/css/bootstrap.css'
    pdf = HTML(string=html).write_pdf(stylesheets=[CSS(css)])

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=ordenes_auditoria.pdf'
    response.write(pdf)
    return response
generar_auditoria.short_description = 'Generar auditoria'

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ['payment', 'user', 'product', 'quantity', 'product_price', 'ordered']
    extra = 0
    can_delete = False

class OrderAdmin(admin.ModelAdmin):
    list_display =['order_number', 'full_name', 'phone', 'email', 'city', 'order_total', 'tax', 'status', 'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    list_per_page = 20
    inlines = [OrderProductInline]
    actions = [generar_pdf, generar_auditoria]

admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
