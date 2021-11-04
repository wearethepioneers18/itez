from django.test import TestCase
import uuid

from utils import generate_uuid_and_agent_code


class UuidTest(TestCase):
    def test_uuid_function(self):
        uuid_one = generate_uuid_and_agent_code()[0]
        agent_code = generate_uuid_and_agent_code()[1]

        self.assertEquals(str(uuid_one)[1:8].upper(), str(
            agent_code).upper().len())

        self.assertEquals(len(str(uuid_one)[1:8].upper()), len(str(
            agent_code).upper()))
