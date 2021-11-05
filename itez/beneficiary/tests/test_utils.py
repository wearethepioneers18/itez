from django.test import TestCase

from itez.beneficiary.utils import generate_uuid_and_agent_code


class TestUUIDAndAgentCode(TestCase):

    def setUp(self):
        """
         This method is called for every test that runs and 
         helps with variable declaration.
        """
        self.uuid_code = generate_uuid_and_agent_code()[0]
        self.agent_code = generate_uuid_and_agent_code()[1]

    def test_uuid_valid(self):
        """
         This method tests for the validity of generated uuid.
        """
        self.assertEqual(len(str(self.uuid_code)), 36)

    def test_agent_code_length(self):
        """
         This method tests for length of agent code.
        """
        self.assertEqual(len(self.agent_code), 7)

    def test_agent_code_upper(self):
        """
         This method tests for capitalization of agent code.
        """
        self.assertEquals((self.agent_code).isupper(), True)
