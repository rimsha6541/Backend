# Generated by Django 4.2.4 on 2023-08-28 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_details', '0014_rename_memory_mobilephones_mobile_memory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='sub_category',
        ),
        migrations.AlterField(
            model_name='product',
            name='p_status',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.DeleteModel(
            name='SubCategory',
        ),
    ]
