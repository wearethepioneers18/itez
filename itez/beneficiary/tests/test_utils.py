from django.test import TestCase

from itez.beneficiary.utils import generate_uuid_and_agent_code


class TestUUIDAndAgentCode(TestCase):
    def setUp(self):
        """
        This method is called for every test that runs and
        helps with variable declaration.
        """
        self.beneficiary_code = generate_uuid_and_agent_code()[0]
        self.agent_code = generate_uuid_and_agent_code()[1]

    def test_uuid_valid(self):
        """
        This method tests for the validity of generated uuid.
        """
        self.assertEqual(len(str(self.beneficiary_code)), 19)

    def test_agent_code_length(self):
        """
        This method tests for length of agent code.
        """
        self.assertEqual(len(self.agent_code), 13)

    def test_beneficiary_code_upper(self):
        """
        This method tests for capitalization of the last 7 unique characters
        of the beneficiary code.
        """
        self.assertEquals((self.beneficiary_code[-7:]).isupper(), True)

    def test_agent_code_upper(self):
        """
        This method tests for capitalization of the last 7 unique characters of
        the agent code.
        """
        self.assertEquals((self.agent_code[-7:]).isupper(), True)
