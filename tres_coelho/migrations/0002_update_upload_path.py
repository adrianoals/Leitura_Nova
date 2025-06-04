from django.db import migrations, models
import tres_coelho.models

class Migration(migrations.Migration):

    dependencies = [
        ('tres_coelho', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leitura',
            name='foto_relogio',
            field=models.ImageField(blank=True, null=True, upload_to=tres_coelho.models.get_upload_path),
        ),
    ] 