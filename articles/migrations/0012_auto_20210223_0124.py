# Generated by Django 3.1.3 on 2021-02-22 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0011_reporttoarticle_reporttocomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporttocomment',
            name='extra_comment',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='reporttocomment',
            name='type_of_report',
            field=models.IntegerField(blank=True, choices=[(1, 'This Is Spam'), (2, 'This Reporting'), (3, 'This 18 Plus')], default=1, null=True),
        ),
    ]
