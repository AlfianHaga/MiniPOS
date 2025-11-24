"""Add image_url field to Product."""

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pos", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="image_url",
            field=models.URLField(blank=True),
        ),
    ]
