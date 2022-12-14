# Generated by Django 2.2.4 on 2020-04-13 11:25

from django.db import migrations, models
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_auto_20200121_0854'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='status',
            field=models.CharField(choices=[('draft', 'DRAFT'), ('inreview', 'INREVIEW'), ('published', 'PUBLISHED')], default='draft', max_length=25),
        ),
        migrations.AlterField(
            model_name='article',
            name='body',
            field=markdownx.models.MarkdownxField(),
        ),
    ]
