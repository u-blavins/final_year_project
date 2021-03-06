import json


class Governance:
    """ Class for applying governance to CloudFormation Templates """

    def __init__(self, template={}):
        """ Instantiate Object """
        self.resource_types = {
            'AWS::S3::Bucket': 'S3',
            'AWS::S3::BucketPolicy': 'S3'
        }
        self.template = template
        self.resources = {}

    def set_template(self, template):
        """ Set the CloudFormation Template """
        self.template = template
        self.get_all_resources()

    def get_template(self):
        """ Getter for the CloudFormation Template """
        return self.template

    def get_resources(self):
        """ Getter for resources within a CloudFormation Template """
        return self.resources

    def get_all_resources(self):
        """ Get all the resources within a CloudFormation Template """
        if 'Resources' in self.template:
            resources = self.template['Resources']
            for resource in resources:
                if 'Type' in resources[resource]:
                    self.set_resources(
                        resources[resource]['Type'],
                        resources[resource]['Properties'])
    
    def set_resources(self, resource_type, res_property):
        """ Validates if resource type is valid """
        if resource_type in self.resource_types:
            if resource_type not in self.resources:
                self.resources[resource_type] = res_property
            
    def validate(self):
        """ Handles reources to perform governance checks """
        for resource in self.resources.keys():
            if self.resource_types[resource] == 'S3':
                s3_governance = S3_Governance(
                    resource, self.resources[resource])
                s3_governance.s3_handler()


class S3_Governance:
    """ Class that governs S3 resource types """
    
    def __init__(self, res_type, res_property):
        self.res_type = res_type
        self.res_property = res_property
        self.rules = self.load_rules()

    def s3_handler(self):
        """ Handles S3 resource types for applying governance to """
        if self.res_type == 'AWS::S3::Bucket':
            self.s3_bucket_governance()

    def load_rules(self):
        """ Load Governance policies """
        rules = {}
        with open('governance/rules.json') as file:
            rules = json.load(file)
        return rules
    
    def get_rules(self):
        """ Getter for governance rules """
        return self.rules

    def s3_bucket_governance(self):
        """ Govern S3 Bucket properties """
        for rule in self.rules.keys():
            props = self.rules[rule]
            if rule == 'BucketEncryption':
                self.bucket_encryption(rule, props)
            if rule == 'VersioningConfiguration':
                self.version_configuration(rule, props)
            if rule == 'PublicAccessBlockConfiguration':
                self.public_access(rule, props)
            if rule == 'AccessControl':
                self.access_control(rule, props)

    def bucket_encryption(self, config, props):
        """ Method that governs bucket encryption configuration 
        
        Args:
            config (str): configuration option
            props (dict): governance properties
        """
        encryption_rule = \
            props['ServerSideEncryptionConfiguration'][0]\
            ['ServerSideEncryptionByDefault']
        
        mandatory = encryption_rule['Mandatory']
        accepted = encryption_rule['Accepted']
        
        if 'BucketEncryption' in self.res_property:
            encryption = \
                self.res_property[config]\
                ['ServerSideEncryptionConfiguration'][0]\
                ['ServerSideEncryptionByDefault']

            if encryption != mandatory and encryption != accepted:
                self.res_property[config] = {
                    'ServerSideEncryptionConfiguration': [
                        {'ServerSideEncryptionByDefault': mandatory}]}
        else:
            self.res_property[config] = {
                'ServerSideEncryptionConfiguration': [
                    {'ServerSideEncryptionByDefault': mandatory}]}

    def version_configuration(self, config, props):
        """ Method that governs version configuration on a bucket

        Args:
            config (str): configuration option
            props (dict): governance properties
        """
        if 'VersioningConfiguration' in self.res_property:
            versioning = self.res_property[config]
            if versioning != props:
                self.res_property[config] = props
        else:
            self.res_property[config] = props

    def public_access(self, config, props):
        """ Method that governs public access configuration on
        a bucket

        Args:
            config (str): configuration option
            props (dict): governance properties
        """
        mandatory = props['Mandatory']
        accepted = props['Accepted']


        if 'PublicAccessBlockConfiguration' in self.res_property:
            public_block = self.res_property[config]

            if public_block != mandatory and public_block != accepted:
                self.res_property[config] = mandatory
        else:
            self.res_property[config] = mandatory

    def access_control(self, config, props):
        """ Method that governs access control on a bucket

        Args:
            config (str): configuration option
            props (dict): governance properties
        """
        mandatory = props['Mandatory']
        accepted = props['Accepted']
        allowed = []
        allowed.extend(mandatory)
        allowed.extend(accepted)

        if 'AccessControl' in self.res_property:
            access_control = self.res_property[config]

            if access_control not in allowed:
                self.res_property[config] = mandatory
        else:
            self.res_property[config] = mandatory
