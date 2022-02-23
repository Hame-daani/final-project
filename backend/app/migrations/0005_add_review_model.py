from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_load_movies_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField()),
                ('text', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('movie', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='app.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 related_name='reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
