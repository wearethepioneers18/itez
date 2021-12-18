import time
import os
import sys
import json

from datetime import datetime
from django.conf import settings

from config import celery_app

from .resources import BeneficiaryResource
from celery import shared_task


@shared_task(bind=True, name="itez")
def generate_export_file(self):
    """
    This task generates a file containing all Beneficiary data for export, stores for file temporary, and return
    the filename to be used to construct a full download URL for the file on the client.
    """
    beneficiary_resource = BeneficiaryResource()
    dataset = beneficiary_resource.export()
    filename = save_exported_data(data=dataset.xlsx, file_ext=".xlsx")
    return filename


def save_exported_data(data=None, file_ext=None):
    timestamp = datetime.now().strftime("%H_%M_%S_%f")
    file_export_path = f"{settings.MEDIA_ROOT}/exports"

    filename = f"all_beneficiaries_export_{timestamp}{file_ext}"

    if not os.path.exists(file_export_path):
        os.mkdir(file_export_path)

    with open(f"{file_export_path}/{filename}", "wb") as f:
        f.write(data)
        return filename
