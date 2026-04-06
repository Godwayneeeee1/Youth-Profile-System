from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0001_initial'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.AddField(
                    model_name='youth',
                    name='is_unemployed',
                    field=models.BooleanField(default=False, verbose_name='Unemployed Youth'),
                ),
            ],
        ),
    ]