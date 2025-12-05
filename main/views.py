from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Project,DownloadRecord
# Create your views here.
def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')



def project_list(request):
    projects_list = Project.objects.all()
    
    # Pagination - 9 projects per page
    paginator = Paginator(projects_list, 9)
    page = request.GET.get('page')
    
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        projects = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page
        projects = paginator.page(paginator.num_pages)
    
    return render(request, 'project_list.html', {'projects': projects})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'project_detail.html', {'project': project})

def custom_404(request, exception):
    """Custom 404 error handler"""
    return render(request, '404.html', status=404)

def terms_view(request):
    """Terms and Conditions page"""
    return render(request, 'terms.html')

def privacy_view(request):
    """Privacy Policy page"""
    return render(request, 'privacy.html')

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT,TA_RIGHT
from io import BytesIO
import os
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


@csrf_exempt
@require_POST
def download_project_abstract(request):
    project_id = request.POST.get('project_id')
    project = get_object_or_404(Project, pk=project_id)
    
    # Get user details
    user_name = request.POST.get('name', '')
    user_email = request.POST.get('email', '')
    user_phone = request.POST.get('phone', '')
    user_college = request.POST.get('college', '')
    
    if user_phone:
        download_record, created = DownloadRecord.objects.get_or_create(
            phone=user_phone,
            defaults={
                'project': project,
                'name': user_name,
                'email': user_email,
                'college': user_college,
            }
        )
        
        # If record already exists, optionally update it with latest info
        if not created:
            download_record.project = project
            download_record.name = user_name
            download_record.email = user_email
            download_record.college = user_college
            download_record.save()
            print(f"Updated existing record for phone: {user_phone}")
        else:
            print(f"Created new record for phone: {user_phone}")
    
    # Create PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=A4,
        topMargin=0.5*inch,
        bottomMargin=0.75*inch,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch
    )
    
    # Container for PDF elements
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Custom styles with new color #17cfbc
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=26,
        textColor=colors.HexColor('#0e5068'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#17cfbc'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        leading=16
    )
    
    # Try multiple paths for logo
    logo_paths = [
        os.path.join(settings.STATIC_ROOT, 'images', 'l.png'),
        os.path.join(settings.BASE_DIR, 'static', 'images', 'l.png'),
    ]
    
    logo_path = None
    for path in logo_paths:
        if os.path.exists(path):
            logo_path = path
            break
    
    # Create logo element
    if logo_path:
        try:
            logo = Image(logo_path, width=2*inch, height=0.7*inch)
            print("Logo found at:", logo_path)
        except Exception as e:
            print(f"Error loading logo: {e}")
            logo = Paragraph('<font size=22 color="#0e5068"><b>ZERAZONE</b></font>', styles['Normal'])
    else:
        logo = Paragraph('<font size=22 color="#0e5068"><b>ZERAZONE</b></font>', styles['Normal'])
        print("Logo not found, using text fallback")

    # Header Section with logo
    header_data = [[
        logo,
        Paragraph(
            '<font size=10 color="#333333"><b>Final Year Projects & Training</b></font><br/>'
            '<font size=9 color="#555555">Contact: +91 9061643216</font><br/>'
            '<font size=9 color="#555555">Email: zerazone2025@gmail.com</font>', 
            ParagraphStyle('RightAlign', parent=styles['Normal'], alignment=TA_RIGHT, fontSize=9)
        )
    ]]
    
    # Calculate available width (page width minus margins)
    page_width = A4[0] - doc.leftMargin - doc.rightMargin
    
    header_table = Table(header_data, colWidths=[2.5*inch, page_width - 2.5*inch])
    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ('LINEBELOW', (0, 0), (-1, -1), 3, colors.HexColor('#17cfbc')),
    ]))
    
    elements.append(header_table)
    elements.append(Spacer(1, 0.35*inch))
    
    # Project Title
    elements.append(Paragraph(project.title, title_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Abstract Heading
    elements.append(Paragraph('PROJECT ABSTRACT', heading_style))
    elements.append(Spacer(1, 0.15*inch))
    
    # Project Description
    description_text = project.description.replace('\n', '<br/>')
    elements.append(Paragraph(description_text, body_style))
    elements.append(Spacer(1, 0.35*inch))
    
    # What You'll Get Section
    elements.append(Paragraph('WHAT YOU\'LL GET', heading_style))
    elements.append(Spacer(1, 0.1*inch))
    
    features = [
        'Complete Source Code',
        'Project Documentation Support',
        'PPT Presentation Support',
        'Project Report Support',
        'Installation Guide',
        'Viva Preparation Support'
    ]
    
    feature_style = ParagraphStyle(
        'FeatureStyle',
        parent=styles['BodyText'],
        fontSize=11,
        spaceAfter=8,
        leftIndent=15,
        bulletIndent=5
    )
    
    for feature in features:
        elements.append(Paragraph(f'<font color="#17cfbc">●</font> {feature}', feature_style))
    
    elements.append(Spacer(1, 0.4*inch))
    
    # Footer Section
    footer_left = Paragraph(
        '<font size=11 color="#0e5068"><b>Contact Us</b></font><br/>'
        '<font size=9 color="#333333">Phone: +91 9061643216</font><br/>'
        '<font size=9 color="#333333">Email: zerazone2025@gmail.com</font><br/>'
        '<font size=9 color="#333333">Website: www.zerazone.com</font>', 
        styles['Normal']
    )
    
    footer_right_text = f'<font size=10 color="#0e5068"><b>Download Details</b></font><br/>'
    if user_name:
        footer_right_text += f'<font size=9 color="#333333">Name: {user_name}</font><br/>'
    if user_email:
        footer_right_text += f'<font size=9 color="#333333">Email: {user_email}</font><br/>'
    if user_phone:
        footer_right_text += f'<font size=9 color="#333333">Phone: {user_phone}</font><br/>'
    if user_college:
        footer_right_text += f'<font size=9 color="#333333">College: {user_college}</font><br/>'
    footer_right_text += f'<font size=9 color="#333333">Date: {datetime.now().strftime("%d-%m-%Y")}</font>'
    
    footer_right = Paragraph(
        footer_right_text,
        ParagraphStyle('FooterRight', parent=styles['Normal'], alignment=TA_RIGHT, fontSize=9)
    )
    
    footer_data = [[footer_left, footer_right]]
    
    footer_table = Table(footer_data, colWidths=[page_width/2, page_width/2])
    footer_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 15),
        ('LINEABOVE', (0, 0), (-1, -1), 3, colors.HexColor('#17cfbc')),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f5f5f5')),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    
    elements.append(footer_table)
    
    # Build PDF
    doc.build(elements)
    
    # Get PDF value
    pdf = buffer.getvalue()
    buffer.close()
    
    # Create response
    response = HttpResponse(content_type='application/pdf')
    # Sanitize filename
    safe_title = "".join([c for c in project.title[:30] if c.isalnum() or c in (' ', '-', '_')]).strip()
    response['Content-Disposition'] = f'attachment; filename="Project_Abstract_{safe_title}.pdf"'
    response.write(pdf)
    
    return response




from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from .forms import LoginForm, ProjectForm
import csv

class CustomLoginView(LoginView):
    template_name = 'main/admin_login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('custom_dashboard')

@method_decorator(staff_member_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'main/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_projects'] = Project.objects.count()
        context['total_downloads'] = DownloadRecord.objects.count()
        # Keep recent items for the overview dashboard
        context['recent_projects'] = Project.objects.order_by('-created_at')[:5]
        context['recent_downloads'] = DownloadRecord.objects.order_by('-downloaded_at')[:5]
        return context

@method_decorator(staff_member_required, name='dispatch')
class AdminProjectListView(TemplateView):
    template_name = 'main/admin_projects.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.order_by('-created_at')
        return context

@method_decorator(staff_member_required, name='dispatch')
class AdminDownloadListView(TemplateView):
    template_name = 'main/admin_downloads.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['downloads'] = DownloadRecord.objects.order_by('-downloaded_at')
        return context

@method_decorator(staff_member_required, name='dispatch')
class CreateProjectView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'main/create_project.html'
    success_url = reverse_lazy('admin_projects') # Redirect to project list
    
    def form_valid(self, form):
        return super().form_valid(form)

@staff_member_required
def export_records_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="download_records.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Phone', 'College', 'Project', 'Date'])
    
    records = DownloadRecord.objects.all().select_related('project')
    for record in records:
        writer.writerow([
            record.name,
            record.email,
            record.phone,
            record.college,
            record.project.title,
            record.downloaded_at.strftime("%Y-%m-%d %H:%M:%S")
        ])
        
    return response
