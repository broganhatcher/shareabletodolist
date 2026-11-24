from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0002_task_viewers"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.CreateModel(
            name="TaskList",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("owner", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="owned_lists", to=settings.AUTH_USER_MODEL)),
                ("members", models.ManyToManyField(blank=True, related_name="shared_lists", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name="task", name="task_list",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="tasks", to="tasks.tasklist"),
        ),
    ]
