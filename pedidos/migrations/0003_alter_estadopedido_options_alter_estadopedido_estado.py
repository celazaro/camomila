# Generated by Django 4.2.5 on 2023-10-08 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0002_estadopedido'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='estadopedido',
            options={'ordering': ['id'], 'verbose_name': 'Estado Pedido', 'verbose_name_plural': 'Estados Pedidos'},
        ),
        migrations.AlterField(
            model_name='estadopedido',
            name='estado',
            field=models.CharField(max_length=100),
        ),
    ]