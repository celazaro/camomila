# Generated by Django 4.2.5 on 2023-10-11 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0002_pedido_importe_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='estado',
            field=models.CharField(blank=True, choices=[('opcion1', 'PEDIDO RECIBIDO'), ('opcion2', 'CONFIRMACION PAGO'), ('opcion3', 'PEDIDO EN PREPARACIÓN'), ('opcion4', 'PEDIDO EN REPARTO'), ('opcion5', 'PEDIDO ENTREGADO'), ('opcion6', 'PEDIDO CANCELADO')], default='opcion1', max_length=100),
        ),
    ]
