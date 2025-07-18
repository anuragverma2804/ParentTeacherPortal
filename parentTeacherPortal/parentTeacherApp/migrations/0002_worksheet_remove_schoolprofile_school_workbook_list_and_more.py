# Generated by Django 5.2 on 2025-07-09 13:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parentTeacherApp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Worksheet',
            fields=[
                ('worksheet_id', models.AutoField(primary_key=True, serialize=False)),
                ('worksheet_name', models.CharField(blank=True, max_length=50)),
                ('standard', models.CharField(max_length=5)),
                ('subject', models.CharField(blank=True, max_length=50)),
                ('chapter', models.CharField(blank=True, max_length=50)),
                ('uploaded_document', models.FileField(upload_to='Uploaded Document')),
            ],
        ),
        migrations.RemoveField(
            model_name='schoolprofile',
            name='school_workbook_list',
        ),
        migrations.RemoveField(
            model_name='teacherprofile',
            name='teacher_workbook_list',
        ),
        migrations.AddField(
            model_name='schoolprofile',
            name='students',
            field=models.ManyToManyField(blank=True, default=None, related_name='student', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='schoolprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='SchoolProfile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='standard',
            field=models.CharField(max_length=5),
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='student_assignment_list',
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='student_school',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Student_School', to='parentTeacherApp.schoolprofile'),
        ),
        migrations.AlterField(
            model_name='teacherprofile',
            name='teacher_school',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Teacher_School', to='parentTeacherApp.schoolprofile'),
        ),
        migrations.AlterField(
            model_name='teacherprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='TeacherProfile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('assignment_id', models.AutoField(primary_key=True, serialize=False)),
                ('standard', models.CharField(max_length=5)),
                ('subject', models.CharField(blank=True, max_length=50)),
                ('due_date', models.DateTimeField()),
                ('assigned_by', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_by', to=settings.AUTH_USER_MODEL)),
                ('assigned_student', models.ManyToManyField(related_name='assigned_student', to=settings.AUTH_USER_MODEL)),
                ('submit_status', models.ManyToManyField(related_name='submit_status', to=settings.AUTH_USER_MODEL)),
                ('worksheet', models.ManyToManyField(related_name='Worksheet', to='parentTeacherApp.worksheet')),
            ],
        ),
        migrations.AddField(
            model_name='schoolprofile',
            name='school_workbooks',
            field=models.ManyToManyField(blank=True, default=None, related_name='school_workbooks', to='parentTeacherApp.worksheet'),
        ),
        migrations.AddField(
            model_name='teacherprofile',
            name='teacher_workbooks',
            field=models.ManyToManyField(blank=True, default=None, related_name='teacher_workbooks', to='parentTeacherApp.worksheet'),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='student_assignment_list',
            field=models.ManyToManyField(blank=True, default=None, related_name='student_assignment_list', to='parentTeacherApp.assignment'),
        ),
    ]
