# Generated by Django 2.2.4 on 2019-09-26 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tagtable', '0005_auto_20190925_1313_squashed_0007_remove_tag_branch_old'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='broken',
            field=models.BooleanField(default=False),
        ),
    ]
