# Generated by Django 5.2.1 on 2025-05-26 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_pais_users_pais'),
    ]

    operations = [
        migrations.CreateModel(
            name='Beneficio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
            ],
            options={
                'db_table': 'beneficios',
            },
        ),
    ]
