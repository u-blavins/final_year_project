import pytest
from mock import MagicMock, patch

from governance.governance import Governance as Gov
from governance.governance import S3_Governance as S3_Gov


class TestGovernance:
    """ Test Suite for the Governance Class """

    def setup_method(self):
        """ Initialise Test Suite """
        self.mock_template = {
            'Resources': {'Bucket': {
                'Type': 'AWS::S3::Bucket',
                'Properties': {'BucketName': 'test-bucket-name'}}
            }}
        self.mock_governance = Gov()

    def test_template_empty_if_not_set(self):
        """ Test Success: Template is empty if not set """
        sut = self.mock_governance.get_template()
        assert sut == {}

    def test_resources_empty_if_not_set(self):
        """ Test Success: Resources is empty if not set """
        test_template = {}
        expected = {}
        self.mock_governance.set_template(template=test_template)
        sut = self.mock_governance.get_resources()
        assert sut == expected

    def test_resources_empty_if_type_not_valid(self):
        """ Test Failure: Resources is empty if type is not valid """
        test_template = {
            'Resources': {'Bucket': {
                'Type': 'AWS::IAM::Role',
                'Properties': {'RoleName': 'test-iam-role'}
            }}
        }
        expected = {}
        self.mock_governance.set_template(template=test_template)
        sut = self.mock_governance.get_resources()
        assert sut == expected

    def test_set_get_template(self):
        """ Test Success: Set and get template """
        self.mock_governance.set_template(template=self.mock_template)
        sut = self.mock_governance.get_template()
        assert sut == self.mock_template

    def test_set_get_template_sets_resources(self):
        """ Test Success: Setting template sets resources correctly """
        expected_resources = {'AWS::S3::Bucket': {'BucketName': 'test-bucket-name'}}
        self.mock_governance.set_template(template=self.mock_template)
        sut = self.mock_governance.get_resources()
        assert sut == expected_resources

    def test_validate_does_not_change_template_with_invalid_type(self):
        """ Test Failure: Validate does not change original template if 
        type is invalid  
        """
        expected_template = {
            'Resources': {'Bucket': {
                'Type': 'AWS::IAM::Role',
                'Properties': {'RoleName': 'test-iam-role'}
            }}
        }
        self.mock_governance.set_template(template=expected_template)
        self.mock_governance.validate()
        sut = self.mock_governance.get_template()
        assert sut == expected_template

    def test_validate_does_change_template_with_valid_type(self):
        """ Test Success: Validate changes original template if type valid """
        expected_template = {
            'Resources': {'Bucket': {
                'Type': 'AWS::S3::Bucket',
                'Properties': {'BucketName': 'test-bucket-name'}}
            }}
        self.mock_governance.set_template(template=self.mock_template)
        self.mock_governance.get_resources()
        self.mock_governance.validate()
        sut = self.mock_governance.get_template()
        assert sut != expected_template


class TestS3_Gov:
    """ Test Suite for the S3 Governance Class """

    def setup_method(self):
        """ Initialise Test Suite """
        