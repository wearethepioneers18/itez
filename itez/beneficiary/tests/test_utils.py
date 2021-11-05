# from uuid import uuid4


from django.test import TestCase

from itez.beneficiary.utils import generate_uuid_and_agent_code

# import uuid
# from uuid import UUID

# class UuidTest(TestCase):
#     def test_uuid_function(self):
#         uuid_one = uuid.uuid4()

#         self.assertEquals(uuid_one, uuid.UUID().version == 4)

#     def test_uuid_length(self):
#         uuid_one = generate_uuid_and_agent_code()[0]
#         agent_code_length = len(str(uuid_one)[1:8].upper())
#         self.assertEquals(agent_code_length, 7)


class UUIDAndAgentCode(TestCase):
    @classmethod
    def setUp(self):
        self.uuid_code = generate_uuid_and_agent_code()[0]
        self.agent_code = generate_uuid_and_agent_code()[1]

        return super().setUp(self)

    def test_uuid_valid(self):
        assert len(str(self.uuid_code)) == 36

    def test_agent_code_length(self):
        assert len(str(self.agent_code)) == 7

    def test_agent_code_upper(self):
        assert self.agent_code == self.agent_code.upper()

    def tearDown(self) -> None:
        return super().tearDown()
