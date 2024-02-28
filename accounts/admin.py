from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserProfile
from django.contrib.admin.models import LogEntry
from django.utils.html import format_html

from django.http import HttpResponse
from weasyprint import HTML, CSS
from django.template.loader import get_template

def generar_pdf(modeladmin, request, queryset):
    context = {
        'queryset': queryset,
    }

    template = get_template('adminTemplate/accountspdf.html')
    html = template.render(context)
    css = './bodegon/static/css/bootstrap.css'
    pdf = HTML(string=html).write_pdf(stylesheets=[CSS(css)])

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=usuarios.pdf'
    response.write(pdf)

    return response
generar_pdf.short_description = "Generar PDF seleccionado(s)"

def generar_auditoria(modeladmin, request, queryset):
    logs = LogEntry.objects.filter(content_type_id = 2)
    context = {
        'logs': logs,
        'titulo': 'Usuarios'
    }
    template = get_template('adminTemplate/auditoriapdf.html')
    html = template.render(context)
    css = './bodegon/static/css/bootstrap.css'
    pdf = HTML(string=html).write_pdf(stylesheets=[CSS(css)])

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=usuarios_auditoria.pdf'
    response.write(pdf)
    return response
generar_auditoria.short_description = 'Generar auditoria'

class UserProfileInLine(admin.TabularInline):
    model = UserProfile
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_picture.url))
    
    thumbnail.short_description = 'Profile Picture'
    readonly_fields = ['thumbnail', 'profile_picture', 'city', 'state', 'country', 'address_line_1', 'address_line_2']
    extra = 0
    can_delete = False

class AccountAdmin(UserAdmin):
    list_display = ('email', 'full_name', 'username', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'full_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined', 'is_active')
    list_filter = ('is_active', 'username')
    inlines = [UserProfileInLine]
    filter_horizontal = ()
    fieldsets = ()
    actions = [generar_pdf, generar_auditoria]

class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_picture.url))
    
    thumbnail.short_description = 'Profile Picture'
    list_display = ('thumbnail', 'user', 'city', 'state', 'country')




admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)