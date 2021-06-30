# Generated by Django 3.1.5 on 2021-04-11 07:08

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('topic', models.CharField(choices=[('Physics', 'Physics'), ('Mathematics', 'Mathematics'), ('Chemistry', 'Chemistry'), ('Computer Science', 'Computer Science'), ('Networking', 'Networking')], max_length=100)),
                ('number_of_questions', models.IntegerField()),
                ('time', models.IntegerField(help_text='Duration of the test in mins')),
                ('required_score', models.IntegerField(help_text='required score to pass')),
                ('difficulty', models.CharField(choices=[('1', 'Easy'), ('2', 'Medium'), ('3', 'Hard')], max_length=1)),
            ],
            options={
                'verbose_name_plural': 'Quizes',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='name', max_length=100)),
                ('password', models.CharField(default='password', max_length=100)),
                ('confirm_password', models.CharField(default='confirm_password', max_length=100)),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='TakenQuiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taken_quizzes', to='quizapp.quiz')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taken_quizzes', to='quizapp.student')),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='quizzes',
            field=models.ManyToManyField(through='quizapp.TakenQuiz', to='quizapp.Quiz'),
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizapp.quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizapp.student')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, verbose_name='Question')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='quizapp.quiz')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, verbose_name='Answer')),
                ('is_correct', models.BooleanField(default=False, verbose_name='Correct answer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='quizapp.question')),
            ],
        ),
    ]
