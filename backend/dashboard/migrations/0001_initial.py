from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Venture",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("pod", models.CharField(max_length=100)),
                ("stage", models.CharField(max_length=50)),
                ("founder", models.CharField(max_length=100)),
                ("metrics", models.JSONField(default=dict)),
                ("status", models.CharField(max_length=50)),
                ("last_update", models.DateField()),
            ],
        ),
    ]
