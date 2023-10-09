# Generated by Django 4.2.5 on 2023-10-09 06:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('secciones', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaProd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.TextField()),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now_add=True)),
                ('estado', models.BooleanField(default=True)),
                ('seccion', models.ManyToManyField(to='secciones.secciones')),
            ],
            options={
                'verbose_name': 'CategoriaProductos',
                'verbose_name_plural': 'CategoriasProductos',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=80)),
                ('precio', models.FloatField()),
                ('descripcion', models.CharField(max_length=200)),
                ('informacion', models.TextField()),
                ('imagen', models.ImageField(default='producto_default.jpeg', upload_to='tienda/')),
                ('disponibilidad', models.BooleanField(default=True)),
                ('mas_vendido', models.BooleanField(default=False)),
                ('destacado', models.BooleanField(default=False)),
                ('oferta', models.BooleanField(default=False)),
                ('porcentaje_oferta', models.IntegerField(default=0)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now_add=True)),
                ('estado', models.BooleanField(default=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tienda.categoriaprod')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
            },
        ),
    ]
