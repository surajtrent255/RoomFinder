# Generated by Django 3.2.5 on 2021-07-11 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rentapp', '0004_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookroom',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rentapp.client'),
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
    ]