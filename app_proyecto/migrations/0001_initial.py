# Generated by Django 2.0.2 on 2018-03-17 04:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AreasTrabajo',
            fields=[
                ('Id_Area', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('Nombre', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='DireccionPersonas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Calle', models.CharField(max_length=200)),
                ('Colonia', models.CharField(max_length=200)),
                ('Num_Interior', models.CharField(max_length=30)),
                ('Num_Exterior', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Empleados',
            fields=[
                ('No_Empleado', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Examen',
            fields=[
                ('Id_Examen', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('Nombre', models.CharField(max_length=150)),
                ('Id_Area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_proyecto.AreasTrabajo')),
            ],
        ),
        migrations.CreateModel(
            name='ExamenPersona',
            fields=[
                ('Num_Examen', models.AutoField(primary_key=True, serialize=False)),
                ('Fecha_Elaborado', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Personas',
            fields=[
                ('Curp', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('Nombres', models.CharField(max_length=150)),
                ('Ap_Paterno', models.CharField(max_length=100)),
                ('Ap_Materno', models.CharField(max_length=100)),
                ('NSS', models.CharField(max_length=40)),
                ('RFC', models.CharField(max_length=40)),
                ('Fecha_Nacimiento', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='PuestoEmpleado',
            fields=[
                ('IdPuesto', models.AutoField(primary_key=True, serialize=False)),
                ('Nombre', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='ResultadoExamen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Aciertos', models.IntegerField()),
                ('Errores', models.IntegerField()),
                ('Cant_Preguntas', models.IntegerField()),
                ('Num_Examen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_proyecto.ExamenPersona')),
            ],
        ),
        migrations.AddField(
            model_name='examenpersona',
            name='Curp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_proyecto.Personas'),
        ),
        migrations.AddField(
            model_name='examenpersona',
            name='Id_Examen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_proyecto.Examen'),
        ),
        migrations.AddField(
            model_name='empleados',
            name='Curp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_proyecto.Personas'),
        ),
        migrations.AddField(
            model_name='empleados',
            name='Id_Puesto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_proyecto.PuestoEmpleado'),
        ),
        migrations.AddField(
            model_name='direccionpersonas',
            name='Curp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_proyecto.Personas'),
        ),
        migrations.AddField(
            model_name='areastrabajo',
            name='Encargado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_proyecto.Empleados'),
        ),
    ]