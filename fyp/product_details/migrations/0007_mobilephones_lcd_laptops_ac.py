# Generated by Django 4.1.7 on 2023-07-12 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product_details', '0006_remove_lcd_category_remove_lcd_product_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MobilePhones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('processor', models.CharField(max_length=500)),
                ('battery', models.CharField(max_length=500)),
                ('memory', models.CharField(max_length=500)),
                ('display', models.CharField(max_length=500)),
                ('camera', models.CharField(max_length=500)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_details.category')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_details.product')),
                ('sub_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_details.subcategory')),
            ],
        ),
        migrations.CreateModel(
            name='LCD',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display', models.CharField(max_length=500)),
                ('power_consumption', models.CharField(max_length=500)),
                ('audio', models.CharField(max_length=500)),
                ('chip', models.CharField(max_length=500)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_details.category')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_details.product')),
                ('sub_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_details.subcategory')),
            ],
        ),
        migrations.CreateModel(
            name='Laptops',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('processor', models.CharField(max_length=500)),
                ('battery', models.CharField(max_length=500)),
                ('memory', models.CharField(max_length=500)),
                ('display', models.CharField(max_length=500)),
                ('generation', models.IntegerField(max_length=2)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_details.category')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_details.product')),
                ('sub_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_details.subcategory')),
            ],
        ),
        migrations.CreateModel(
            name='AC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capacity', models.CharField(max_length=500)),
                ('type', models.CharField(max_length=500)),
                ('inverter', models.BooleanField(default=True)),
                ('warranty', models.IntegerField(max_length=3)),
                ('energy_efficiency', models.IntegerField(max_length=2)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_details.category')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_details.product')),
                ('sub_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_details.subcategory')),
            ],
        ),
    ]
