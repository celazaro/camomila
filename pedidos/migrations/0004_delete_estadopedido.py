# Generated by Django 4.2.5 on 2023-10-09 04:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0003_alter_estadopedido_options_alter_estadopedido_estado'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EstadoPedido',
        ),
    ]
