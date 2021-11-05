from django.test import TestCase

from itez.beneficiary.utils import generate_uuid_and_agent_code


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
