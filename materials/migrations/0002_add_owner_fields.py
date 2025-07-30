from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="owner",
            field=models.ForeignKey(
                to=settings.AUTH_USER_MODEL,
                on_delete=django.db.models.deletion.SET_NULL,
                null=True,
                blank=True,
                verbose_name="Владелец",
                help_text="Укажите владельца курса",
            ),
        ),
        migrations.AddField(
            model_name="lesson",
            name="owner",
            field=models.ForeignKey(
                to=settings.AUTH_USER_MODEL,
                on_delete=django.db.models.deletion.SET_NULL,
                null=True,
                blank=True,
                verbose_name="Владелец",
                help_text="Укажите владельца урока",
            ),
        ),
        migrations.AddField(
            model_name="lesson",
            name="course",
            field=models.ForeignKey(
                to="materials.course",
                on_delete=django.db.models.deletion.CASCADE,
                null=True,
                blank=True,
                related_name="lesson_set",
                verbose_name="курс",
                help_text="выберите курс",
            ),
        ),
    ]