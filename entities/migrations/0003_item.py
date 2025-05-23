# Generated by Django 5.1.6 on 2025-04-03 16:15

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0002_subsite'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True, null=True)),
                ('type', models.CharField(max_length=150)),
                ('identification', models.CharField(blank=True, max_length=150, null=True)),
                ('item_date', models.JSONField(blank=True, null=True)),
                ('family', models.CharField(blank=True, max_length=150, null=True)),
                ('scient_name', models.CharField(blank=True, max_length=150, null=True)),
                ('material', models.CharField(blank=True, max_length=150, null=True)),
                ('current_location', models.CharField(blank=True, max_length=150, null=True)),
                ('references', models.TextField(blank=True, null=True)),
                ('citation', models.TextField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('site', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='entities.site')),
                ('subsite', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subsite', to='entities.subsite')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
