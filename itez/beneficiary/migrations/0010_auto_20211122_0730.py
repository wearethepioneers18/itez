# Generated by Django 3.1.13 on 2021-11-22 07:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("beneficiary", "0009_auto_20211118_1207"),
    ]

    operations = [
        migrations.RenameField(
            model_name="agentdetail",
            old_name="agend_ID",
            new_name="agend_id",
        ),
        migrations.RenameField(
            model_name="beneficiary",
            old_name="agent_ID",
            new_name="agent",
        ),
        migrations.RenameField(
            model_name="beneficiary",
            old_name="beneficiary_ID",
            new_name="beneficiary_id",
        ),
    ]
