from django.test import TestCase

from itez.beneficiary.utils import generate_uuid_and_agent_code


class UUIDAndAgentCode(TestCase):
    @classmethod
    def setUp(self):
        """
         This method is called for every test that runs and helps with variable declaration
        """
        self.uuid_code = generate_uuid_and_agent_code()[0]
        self.agent_code = generate_uuid_and_agent_code()[1]

        return super().setUp(self)

    def tearDown(self):
        """
         This method is called for every test as well
        """
        return super().tearDown()

    def test_uuid_valid(self):
        """
         This function tests for the validity of generated uuid.
        """
        self.assertEqual(len(str(self.uuid_code)), 36)

    def test_agent_code_length(self):
        """
         This function tests for length of agent code.
        """
        self.assertEqual(len(str(self.agent_code)), 7)

    def test_agent_code_upper(self):
        """
         This function tests for capitalization of agent code.
        """
        self.assertEqual((self.agent_code), self.agent_code.upper())
