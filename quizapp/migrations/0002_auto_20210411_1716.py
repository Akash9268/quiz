# Generated by Django 3.1.5 on 2021-04-11 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='quizzes',
            field=models.ManyToManyField(through='quizapp.Result', to='quizapp.Quiz'),
        ),
        migrations.DeleteModel(
            name='TakenQuiz',
        ),
    ]
