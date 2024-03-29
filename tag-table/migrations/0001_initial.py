# Generated by Django 2.2.1 on 2019-06-04 12:10

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Commit',
            fields=[
                ('git_hash', models.CharField(max_length=40, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator('$[a-z0-9]{40}$')])),
                ('svn_revision', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('subject', models.CharField(max_length=255)),
                ('author_name', models.CharField(max_length=100)),
                ('author_email', models.CharField(max_length=100, validators=[django.core.validators.EmailValidator()])),
                ('author_time', models.DateTimeField()),
                ('committer_name', models.CharField(max_length=100)),
                ('committer_email', models.CharField(max_length=100, validators=[django.core.validators.EmailValidator()])),
                ('committer_time', models.DateTimeField()),
            ],
            options={
                'ordering': ['svn_revision'],
            },
        ),
        migrations.CreateModel(
            name='ReleaseNoteData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codes', models.CharField(max_length=10)),
                ('issue_id', models.CharField(max_length=30)),
                ('comment', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'ordering': ['commit'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('based_on', models.CharField(max_length=100)),
                ('branch', models.CharField(max_length=100)),
                ('dependency1_version', models.CharField(max_length=100)),
                ('dependency2_version', models.CharField(max_length=50)),
                ('dependency3_version', models.CharField(max_length=50)),
                ('release_time', models.DateTimeField()),
            ],
            options={
                'get_latest_by': ['release_time', 'name'],
            },
        ),
        migrations.AddIndex(
            model_name='tag',
            index=models.Index(fields=['release_time', 'name'], name='tagtable_t_release_995518_idx'),
        ),
        migrations.AddField(
            model_name='releasenotedata',
            name='commit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tagtable.Commit'),
        ),
        migrations.AddField(
            model_name='commit',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tagtable.Tag'),
        ),
        migrations.AddIndex(
            model_name='releasenotedata',
            index=models.Index(fields=['commit'], name='tagtable_r_commit__48e696_idx'),
        ),
        migrations.AddIndex(
            model_name='commit',
            index=models.Index(fields=['tag'], name='tagtable_c_tag_id_81e691_idx'),
        ),
    ]
