# Generated by Django 4.0 on 2022-11-23 06:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_rename_transaction_id_payment_transactionid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wishlist',
            old_name='product1',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='wishlist',
            old_name='user1',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='is_active1',
        ),
    ]