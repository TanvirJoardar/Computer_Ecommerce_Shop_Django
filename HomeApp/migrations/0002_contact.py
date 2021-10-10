# Generated by Django 3.2 on 2021-04-16 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomeApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=50)),
                ('subject', models.CharField(blank=True, max_length=200)),
                ('message', models.TextField(blank=True, max_length=1000)),
                ('status', models.CharField(choices=[('New', 'New'), ('Read', 'Read'), ('Closed', 'Closed')], default='New', max_length=40)),
                ('ip', models.CharField(blank=True, max_length=100)),
                ('Note', models.CharField(blank=True, max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]