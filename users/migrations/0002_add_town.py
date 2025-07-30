from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="town",
            field=models.CharField(
                max_length=35,
                verbose_name="город",
                blank=True,
                null=True,
                help_text="Введите название города",
            ),
        ),
    ]