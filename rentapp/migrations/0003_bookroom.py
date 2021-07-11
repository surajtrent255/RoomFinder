# Generated by Django 3.2.5 on 2021-07-11 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rentapp', '0002_delete_bookroom'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('citizenship_front', models.ImageField(upload_to='BookRoom')),
                ('citizenship_back', models.ImageField(upload_to='BookRoom')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rentapp.customer')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rentapp.room')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
