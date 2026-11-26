from django.db import migrations


def consolidate(apps, schema_editor):
    Group = apps.get_model("tasks", "TaskGroup")
    List = apps.get_model("tasks", "TaskList")
    Task = apps.get_model("tasks", "task")
    db = schema_editor.connection.alias
    for group in Group.objects.using(db).all():
        project = List.objects.using(db).create(name=group.name, owner_id=group.owner_id)
        project.members.add(*group.members.using(db).exclude(pk=group.owner_id).values_list("pk", flat=True))
        Task.objects.using(db).filter(group_id=group.pk, task_list__isnull=True).update(task_list_id=project.pk)


class Migration(migrations.Migration):
    dependencies = [("tasks", "0003_taskgroup_task_group"), ("tasks", "0003_tasklist_task_task_list")]
    operations = [
        migrations.RunPython(consolidate),
        migrations.RemoveField(model_name="task", name="group"),
        migrations.DeleteModel(name="TaskGroup"),
    ]
