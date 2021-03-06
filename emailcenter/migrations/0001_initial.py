# Generated by Django 3.2.9 on 2021-12-01 22:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('school', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Emailinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_title', models.CharField(blank=True, max_length=120, null=True)),
                ('email_content', models.TextField(blank=True, null=True)),
                ('email_receiver', models.CharField(max_length=120, null=True)),
                ('email_sendtime', models.DateTimeField(blank=True, null=True)),
                ('email_school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.schoolinfo')),
            ],
        ),
        migrations.CreateModel(
            name='EmailFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_file', models.FileField(blank=True, null=True, upload_to='email_file/email_tempfiles/')),
                ('emailkey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emailcenter.emailinfo')),
            ],
        ),
    ]
