from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("application", "0006_remove_stage_promotion_remove_stage_themes_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="stage",
            name="rapport_texte",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="stage",
            name="presentation_texte",
            field=models.TextField(blank=True, default=""),
        ),
    ]
