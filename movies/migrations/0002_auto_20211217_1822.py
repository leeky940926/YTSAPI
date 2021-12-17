# Generated by Django 2.2 on 2021-12-17 18:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='genre',
        ),
        migrations.CreateModel(
            name='MovieGenre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Genre')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Movie')),
            ],
            options={
                'db_table': 'movies_genres',
            },
        ),
        migrations.AddField(
            model_name='movie',
            name='genre',
            field=models.ManyToManyField(through='movies.MovieGenre', to='movies.Genre'),
        ),
    ]
