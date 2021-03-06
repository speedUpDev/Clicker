# Generated by Django 4.0.4 on 2022-06-08 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0004_alter_boost_level_alter_boost_type_alter_core_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('power', models.IntegerField()),
                ('image', models.ImageField(upload_to='dmc_ranks')),
                ('music', models.FileField(upload_to='static/music')),
            ],
        ),
        migrations.AlterField(
            model_name='boost',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(0, 'casual'), (1, 'auto')], default=0),
        ),
    ]
