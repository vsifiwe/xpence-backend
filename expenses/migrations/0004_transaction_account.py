# Generated by Django 4.0 on 2021-12-25 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0003_alter_category_type_alter_transaction_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='account',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='expenses.account'),
            preserve_default=False,
        ),
    ]