from django.db import migrations, models
import alvorada.models

class Migration(migrations.Migration):

    dependencies = [
        ('alvorada', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leitura',
            name='foto_relogio',
            field=models.ImageField(blank=True, null=True, upload_to=alvorada.models.get_upload_path),
        ),
    ] 