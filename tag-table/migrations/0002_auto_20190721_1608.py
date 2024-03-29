# Generated by Django 2.2.1 on 2019-07-21 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tagtable', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commit',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commits', to='tagtable.Tag'),
        ),
        migrations.AlterField(
            model_name='releasenotedata',
            name='commit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rn_data', to='tagtable.Commit'),
        ),
    ]
