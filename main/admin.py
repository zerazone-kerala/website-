from django.contrib import admin
from .models import Project, DownloadRecord
from django.http import HttpResponse
from django.utils.html import format_html
import csv

# Custom Action for CSV Export
def export_as_csv(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={meta}.csv'
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        row = writer.writerow([getattr(obj, field) for field in field_names])

    return response

export_as_csv.short_description = "Export Selected to CSV"

# Register your models here.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description_preview', 'created_at', 'download_count')
    search_fields = ('title', 'description')
    list_per_page = 20
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'download_count_display')
    
    fieldsets = (
        ('Project Information', {
            'fields': ('title', 'description')
        }),
        ('Metadata', {
            'fields': ('created_at', 'download_count_display'),
            'classes': ('collapse',)
        }),
    )
    
    def description_preview(self, obj):
        """Show truncated description in list view"""
        if obj.description:
            return obj.description[:100] + '...' if len(obj.description) > 100 else obj.description
        return '-'
    description_preview.short_description = 'Description'
    
    def download_count(self, obj):
        """Show download count with badge"""
        count = DownloadRecord.objects.filter(project=obj).count()
        if count > 0:
            return format_html(
                '<span style="background: #17cfbc; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: 600;">{}</span>',
                count
            )
        return format_html('<span style="color: #94a3b8;">0</span>')
    download_count.short_description = 'Downloads'
    
    def download_count_display(self, obj):
        """Show download count in detail view"""
        return DownloadRecord.objects.filter(project=obj).count()
    download_count_display.short_description = 'Total Downloads'

@admin.register(DownloadRecord)
class DownloadRecordAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'college', 'project_link', 'downloaded_at')
    list_filter = ('project', 'downloaded_at', 'college')
    search_fields = ('name', 'email', 'phone', 'project__title', 'college')
    actions = [export_as_csv]
    list_per_page = 50
    date_hierarchy = 'downloaded_at'
    readonly_fields = ('downloaded_at',)
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'college')
        }),
        ('Project Details', {
            'fields': ('project',)
        }),
        ('Metadata', {
            'fields': ('downloaded_at',),
            'classes': ('collapse',)
        }),
    )
    
    def project_link(self, obj):
        """Show project as clickable link"""
        if obj.project:
            return format_html(
                '<a href="/admin/main/project/{}/change/" style="color: #0e5068; font-weight: 500;">{}</a>',
                obj.project.id,
                obj.project.title[:50] + '...' if len(obj.project.title) > 50 else obj.project.title
            )
        return '-'
    project_link.short_description = 'Project'
    project_link.admin_order_field = 'project__title'

# Admin Site Customization
admin.site.site_header = "Zerazone Administration"
admin.site.site_title = "Zerazone Admin Portal"
admin.site.index_title = "Welcome to Zerazone Project Management"