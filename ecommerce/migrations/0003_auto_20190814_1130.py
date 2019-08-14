# Generated by Django 2.2.4 on 2019-08-14 05:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0002_auto_20190810_0907'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ecommerce.Product'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cart',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
