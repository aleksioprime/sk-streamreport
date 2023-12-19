from django.db.models import Prefetch
from datetime import datetime

from docx import Document
from docxtpl import DocxTemplate, RichText
from django.http.response import StreamingHttpResponse
import os
from io import BytesIO
from django.conf import settings
from bs4 import BeautifulSoup

from htmldocx import HtmlToDocx
parser = HtmlToDocx()
from docx import Document

from apps.report.models import (
    ReportPeriod,
    ReportCriterion,
    ReportCriterionLevel,
    ReportCriterionAchievement,
    ReportPrimaryTopic,
    ReportTeacher,
    ReportTeacherPrimary,
    ReportSecondaryCriterion,
    ReportSecondaryLevel,
    ReportTeacherSecondary,
    ReportTeacherHigh,
    ReportIbProfile,
    ReportMentor,
    ReportPrimaryUnit,
    ReportMentorPrimary,
    ReportExtra,
)

from general.models import (
    User
)

from apps.portfolio.models import (
    EventParticipation,
)

def get_report_period_queryset():
    return ReportPeriod.objects.all().select_related(
        'year',
        )

def get_report_criterion_queryset():
    return ReportCriterion.objects.all().select_related(
        'author',
        ).prefetch_related(
            'subjects',
            'years',
            'levels'
            )

def get_report_criterion_level_queryset():
    return ReportCriterionLevel.objects.all()

def get_report_criterion_achievement_queryset():
    return ReportCriterionAchievement.objects.all().select_related(
        'criterion',
        'achievement',
        )

def get_report_primary_achievement_queryset():
    return ReportPrimaryTopic.objects.all().select_related(
        'topic',
        )

def get_report_teacher_primary_queryset(group):
    return ReportTeacherPrimary.objects.all().select_related(
        'student',
        'author',
        'period',
        'period__year',
        'group',
        'group__year_academic',
        'group__year_study',
        'subject',
        ).prefetch_related(
            'extra_subjects',
            'criterion_achievements',
            'criterion_achievements__achievement',
            'criterion_achievements__criterion',
            'criterion_achievements__criterion__author',
            'criterion_achievements__criterion__subjects',
            'criterion_achievements__criterion__years',
            'criterion_achievements__criterion__levels',
            'topic_achievements',
            'topic_achievements__topic',
            Prefetch(
                    'student__student_events', 
                    queryset=EventParticipation.objects.filter(group=group)
                ),
            )



def get_report_secondary_criterion_queryset():
    return ReportSecondaryCriterion.objects.all().select_related(
        'criterion',
        )

def get_report_secondary_level_queryset():
    return ReportSecondaryLevel.objects.all().select_related(
        'strand',
        'level',
        ).prefetch_related(
            'strand',
            'strand__achieve_levels',
        )

def get_report_teacher_secondary_queryset(group, student):
    return ReportTeacherSecondary.objects.select_related(
        'student',
        'author',
        'period',
        'period__year',
        'group',
        'group__year_academic',
        'group__year_study',
        'subject',
        ).prefetch_related(
            'extra_subjects',
            'criterion_achievements',
            'criterion_achievements__achievement',
            'criterion_achievements__criterion',
            'criterion_achievements__criterion__author',
            'criterion_achievements__criterion__subjects',
            'criterion_achievements__criterion__years',
            'criterion_achievements__criterion__levels',
            'criterion_marks',
            'criterion_marks__criterion',
            'objective_levels',
            'objective_levels__strand',
            'objective_levels__strand__strand',
            'objective_levels__strand__strand__objective',
            'objective_levels__strand__achieve_levels',
            'objective_levels__level',
            Prefetch(
                    'student__student_events', 
                    queryset=EventParticipation.objects.filter(group=group)
                ),
            )

def get_report_teacher_high_queryset(group):
    return ReportTeacherHigh.objects.all().select_related(
        'student',
        'author',
        'period',
        'period__year',
        'group',
        'group__year_academic',
        'group__year_study',
        'subject',
        ).prefetch_related(
            'extra_subjects',
            'criterion_achievements',
            'criterion_achievements__criterion',
            Prefetch(
                    'student__student_events', 
                    queryset=EventParticipation.objects.filter(group=group)
                ),
            )

def get_report_ibprofile_queryset():
    return ReportIbProfile.objects.all().select_related(
        'profile',
        )

def get_report_mentor_queryset():
    return ReportMentor.objects.all().select_related(
        'student',
        'author',
        'period',
        'group',
        ).prefetch_related(
            'profiles',
            )

def get_report_primary_unit_queryset():
    return ReportPrimaryUnit.objects.all().select_related(
        'unit',
        )

def get_report_mentor_primary_queryset():
    return ReportMentorPrimary.objects.all().select_related(
        'student',
        'author',
        'period',
        'group',
        ).prefetch_related(
            'profiles',
            'pyp_units',
            )

def get_report_extra_queryset():
    return ReportExtra.objects.all().select_related(
        'student',
        'author',
        'period',
        'group',
        )

# Запрос на репорты сорудников класса
def get_user_report_extra_queryset(group=None, period=None):
    return User.objects.all().prefetch_related(
        Prefetch(
                'reportextra_student_reports', 
                queryset=ReportExtra.objects.filter(group=group, period=period).select_related(
                    'student',
                    'author',
                    'group',
                    'group__year_academic',
                    'group__year_study',
                ).prefetch_related(
                    'student__student_events',
                    'criterion_achievements',
                    'criterion_achievements__achievement',
                    'criterion_achievements__criterion',
                ), 
            ),
        )

def get_user_report_mentor_primary_queryset(group=None, period=None):
    return User.objects.all().prefetch_related(
        'reportmentor_student_reports',
        Prefetch(
                'reportmentor_student_reports', 
                queryset=ReportMentorPrimary.objects.filter(group=group, period=period), 
                to_attr='filtered_reports'
            ),
        'classes',
        )

def get_user_report_mentor_queryset(group=None, period=None):
    return User.objects.prefetch_related(
        Prefetch(
                'reportmentor_student_reports', 
                queryset=ReportMentor.objects.filter(group=group, period=period).select_related(
                    'author', 
                    'student',
                    'group',
                    'group__year_academic',
                    'group__year_study',
                    
                    ).prefetch_related(
                        'student__student_events',
                        'profiles',
                        'profiles__profile',
                        'reportmentorprimary__pyp_units',
                        'reportmentorprimary__pyp_units__unit',
                        'reportmentorprimary__pyp_units__unit__teachers',
                        'reportmentorprimary__pyp_units__unit__year',
                    ), 
            ),
        Prefetch(
                'reportteacher_student_reports', 
                queryset=ReportTeacherPrimary.objects.filter(group=group, period=period).select_related(
                    'author',
                    'subject',
                    ).prefetch_related(
                        'extra_subjects',
                        'criterion_achievements',
                        'criterion_achievements__achievement',
                        'criterion_achievements__criterion',
                        'topic_achievements',
                        'topic_achievements__topic',
                        ), 
                to_attr='filtered_teacher_primary_reports',
            ),
        Prefetch(
                'reportteacher_student_reports', 
                queryset=ReportTeacherSecondary.objects.filter(group=group, period=period).select_related(
                    'author',
                    'subject',
                    ).prefetch_related(
                        'extra_subjects',
                        'criterion_achievements',
                        'criterion_achievements__achievement',
                        'criterion_achievements__criterion',
                        'criterion_marks',
                        'criterion_marks__criterion',
                        'objective_levels',
                        'objective_levels__strand',
                        'objective_levels__level',
                    ),  
                to_attr='filtered_teacher_secondary_reports'
            ),
        Prefetch(
                'reportteacher_student_reports', 
                queryset=ReportTeacherHigh.objects.filter(group=group, period=period).select_related(
                    'author',
                    'subject',
                    ).prefetch_related(
                        'extra_subjects',
                        'criterion_achievements',
                        'criterion_achievements__criterion',
                        'criterion_achievements__achievement',
                        ), 
                to_attr='filtered_teacher_high_reports'
            ),
        Prefetch(
                'reportextra_student_reports', 
                queryset=ReportExtra.objects.filter(group=group, period=period).select_related(
                    'author',
                ).prefetch_related(
                    'criterion_achievements',
                )
            ),
        )

# Функция для экспорта репортов наставника начальной школы
def export_report_noo_msword(student, period_id):
    document = DocxTemplate(os.path.join(settings.BASE_DIR, 'documents', 'reports', 'temp_report_pyp.docx'))
    period = ReportPeriod.objects.filter(id=period_id).first()
    report_period = {
        'name': period.name.capitalize(),
        'year': period.year
    }
    report_mentor = student.reportmentor_student_reports.first()
    report_teachers = []
    if (student.filtered_teacher_primary_reports):
        report_teachers = student.filtered_teacher_primary_reports
        for report in report_teachers:
            report.comment = parsing_html(report.comment)
    report_extras = student.reportextra_student_reports.all()
    for report in report_extras:
        report.comment = parsing_html(report.comment)
    report_units = report_mentor.reportmentorprimary.pyp_units.all()
    for report in report_units:
        report.unit.central_idea = parsing_html(report.unit.central_idea)
        report.unit.ongoing_assessment = parsing_html(report.unit.ongoing_assessment) or ''
        report.unit.action = parsing_html(report.unit.action) or ''
        report.unit.learning_goals = parsing_html(report.unit.learning_goals) or ''
        report.comment = report.comment or ''
    document.render({
        'report_period': report_period,
        'date_created_at': report_mentor.created_at.strftime("%d.%m.%Y"),
        'report_mentor': report_mentor,
        'report_teachers': report_teachers,
        'report_extras': report_extras,
        'report_units': report_units,
    })
    buffer = BytesIO()
    document.save(buffer)
    buffer.seek(0)
    response = StreamingHttpResponse(
        streaming_content=buffer,  # use the stream's content
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f'attachment;filename=test.docx'
    response["Content-Encoding"] = 'UTF-8'
    return response

# Функция для экспорта репортов наставника средней школы
def export_report_ooo_msword(student, period_id):
    document = DocxTemplate(os.path.join(settings.BASE_DIR, 'documents', 'reports', 'temp_report_myp.docx'))
    period = ReportPeriod.objects.filter(id=period_id).first()
    report_period = {
        'name': period.name.capitalize(),
        'year': period.year
    }
    report_mentor = student.reportmentor_student_reports.first()
    if report_mentor.comment:
        report_mentor.comment = parsing_html(report_mentor.comment)
    report_extras = student.reportextra_student_reports.all()
    for report in report_extras:
        report.comment = parsing_html(report.comment)
    report_teachers = []
    if (student.filtered_teacher_secondary_reports):
        report_teachers = student.filtered_teacher_secondary_reports
        for report in report_teachers:
            report.comment = parsing_html(report.comment)
            report.summ = sum(cm.mark for cm in report.criterion_marks.all())
            report.count = len(report.criterion_marks.all())
            report.mark = calculate_criterion(report.count, report.summ)
    document.render({
        'report_period': report_period,
        'report_mentor': report_mentor,
        'report_extras': report_extras,
        'report_teachers': report_teachers,
    })
    buffer = BytesIO()
    document.save(buffer)
    buffer.seek(0)
    response = StreamingHttpResponse(
        streaming_content=buffer,  # use the stream's content
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f'attachment;filename=test.docx'
    response["Content-Encoding"] = 'UTF-8'
    return response

def export_report_soo_msword(student, period_id):
    document = DocxTemplate(os.path.join(settings.BASE_DIR, 'documents', 'reports', 'temp_report_dp.docx'))
    context = {}

    period = ReportPeriod.objects.filter(id=period_id).first()
    report_period = {
        'name': period.name.capitalize(),
        'year': period.year
    }
    context['report_period'] = report_period

    report_mentor = student.reportmentor_student_reports.first()
    if report_mentor.comment:
        report_mentor.comment = parsing_html(report_mentor.comment)
    context['report_mentor'] = report_mentor

    report_extras = student.reportextra_student_reports.all()
    for report in report_extras:
        report.comment = parsing_html(report.comment)
    
    context['report_extras'] = report_extras
    if (student.filtered_teacher_high_reports):
        report_teachers = student.filtered_teacher_high_reports
        for report in report_teachers:
            report.comment = parsing_html(report.comment)
        context['report_teachers'] = report_teachers
            
    document.render(context)
    buffer = BytesIO()
    document.save(buffer)
    buffer.seek(0)
    response = StreamingHttpResponse(
        streaming_content=buffer,  # use the stream's content
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f'attachment;filename=test.docx'
    response["Content-Encoding"] = 'UTF-8'
    return response


def rgb_to_hex(rgb_str):
    # Функция для преобразования значения RGB в HEX (примерный код)
    rgb = rgb_str.replace('rgb', '').replace('(', '').replace(')', '').split(',')
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def parsing_html(html_text):
    if html_text is None:
        return ''
    # Парсинг HTML и преобразование в RichText
    soup = BeautifulSoup(html_text, 'html.parser')
    rich_text = RichText()
    for index, p in enumerate(soup.find_all('p')):
        for content in p.contents:
            if content.name == 'a':
                # Обработка гиперссылок
                url = content.get('href', '')
                text = content.text
                rich_text.add_hyperlink(url, text, color='0000FF', underline=True)
            else:
                text_style = {}
                if content.name == 'strong':
                    text_style['bold'] = True
                elif content.name == 'em':
                    text_style['italic'] = True
                elif content.name == 'span':
                    style = content.attrs.get('style', '')
                    if 'color' in style:
                        color = style.split('color:')[1].strip().replace(';', '')
                        text_style['color'] = rgb_to_hex(color)
                if content.string:
                    rich_text.add(content.string, **text_style)

        # Добавление переноса строки для каждого нового параграфа
        if index != len(soup.find_all('p')) - 1:
            rich_text.add('\n')

    return rich_text

def calculate_criterion(count, summ):
    GRADES = { 1: [3, 5, 7], 2: [6, 10, 14], 3: [8, 14, 20], 4: [11, 19, 28] }
    if count not in GRADES:
        return "N/A"
    if summ >= GRADES[count][2]:
        return 5
    elif summ < GRADES[count][2] and summ >= GRADES[count][1]:
        return 4
    elif summ < GRADES[count][1] and summ >= GRADES[count][0]:
        return 3
    elif summ < GRADES[count][0] and summ > 0:
        return 2
    else:
        return '-'