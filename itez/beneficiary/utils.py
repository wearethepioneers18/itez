import uuid
import os
import shutil

from django.conf import settings
from django.forms.models import model_to_dict

from itez.beneficiary.resources import BeneficiaryResource


def generate_uuid():
    """
    Generates a seven digit agent ID and a unique ID.
    """
    unique_id = uuid.uuid4()
    agent_code = f"Agent-{str(unique_id)[1:8].upper()}"
    beneficiary_code = f"Beneficiary-{str(unique_id)[1:8].upper()}"

    return beneficiary_code, agent_code


def zip_directory(archive_name=None, format=None, directory=None):
    shutil.make_archive(archive_name, format, directory)


def handle_upload(f, destination_directory=None):
        fullpath = f"{settings.MEDIA_ROOT}/supporting_documents/{destination_directory}"
        if not os.path.exists(fullpath):
            os.makedirs(fullpath)

        with open(f"{fullpath}/{f.name}", "wb+") as file:
            for chunk in f.chunks():
                file.write(chunk)


def create_files_dict(directory=None, filenames=[]):
    d = {}
    d["directory"] = directory
    d["filenames"] = filenames
    return d
