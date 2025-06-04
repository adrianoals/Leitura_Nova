from django.db import migrations, models
import imperial.models

class Migration(migrations.Migration):

    dependencies = [
        ('imperial', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leitura',
            name='foto_relogio',
            field=models.ImageField(blank=True, null=True, upload_to=imperial.models.get_upload_path),
        ),
    ] 