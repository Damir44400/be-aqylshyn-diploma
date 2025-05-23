# Generated by Django 5.1.7 on 2025-04-23 18:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ielts', '0011_alter_ieltslistening_test'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ieltslistening',
            options={'verbose_name_plural': 'Listening | Audio File'},
        ),
        migrations.RemoveField(
            model_name='ieltslistening',
            name='part',
        ),
        migrations.RemoveField(
            model_name='ieltslisteningquestion',
            name='listening',
        ),
        migrations.AlterField(
            model_name='ieltslistening',
            name='test',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='listening', to='ielts.ieltstest'),
        ),
        migrations.AlterField(
            model_name='ieltslistening',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.CreateModel(
            name='IeltsListeningPart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part', models.PositiveSmallIntegerField(choices=[(1, 'Part 1'), (2, 'Part 2'), (3, 'Part 3'), (4, 'Part 4')], default=1, verbose_name='Бөлім (Part)')),
                ('listening', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listening_parts', to='ielts.ieltslistening')),
            ],
            options={
                'verbose_name_plural': 'Listening | Parts',
                'unique_together': {('part', 'listening')},
            },
        ),
        migrations.AddField(
            model_name='ieltslisteningquestion',
            name='listening_part',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='ielts.ieltslisteningpart'),
        ),
    ]
