## (c) 2017 by Kwan Lowe

def createInstances(ec2, nodeConfig, dryRun):
    """ Accepts ec2 connection handle, premise and node dicts, returns InstanceId """
    import sys
    import boto3
    from botocore.exceptions import ClientError
    import pprint
    import ast
  
    try:
        instanceId = ec2.create_instances(
            DryRun           = dryRun,
            ImageId          = nodeConfig['awsami'], 
	    UserData         = nodeConfig['userdata'],
	    MinCount         = 1, 
	    MaxCount         = 1,
	    KeyName          = nodeConfig['accesskey'],
	    SubnetId         = nodeConfig['subnet'],
	    SecurityGroupIds = nodeConfig['secgroups'],
	    InstanceType     = nodeConfig['instancetype'],
        )
        return instanceId

    except ClientError as e:
        if e.response['Error']['Code'] == 'DryRunOperation':
            print "Request would have succeeded but DryRun flag is set."
            sys.exit(1)
        else:
            print "Unexpected error in create_instances: %s" % e
            sys.exit(1)

