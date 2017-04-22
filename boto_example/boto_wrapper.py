#!/usr/bin/env python

## (c) 2017 by Kwan Lowe
## License: GPL 3.0 or later

import sys
import os
import optparse
import boto3
import ast

from botocore.exceptions import ClientError

from buildAws import awsFuncs
from buildAws import kllFuncs

programName =  os.path.basename(sys.argv[0])

###  Set up the command line parsing
parser = optparse.OptionParser()
parser.add_option('-c', '--config', action="store", dest="configfile", help="Global environment configuration file.", default='kll.cfg')
parser.add_option('-s', '--server', action="store", dest="node", help="Node name from node data file." )
parser.add_option('-y', '--yes', action="store_false", dest="dryrun", help="Yes, create the instance.", default=True )

options, args = parser.parse_args()

# Set the global parameters (environment, puppet, etc)
configFile    = options.configfile
dryRun        = options.dryrun
node          = options.node

if not node:
    print "Node is mandatary. Please set using -n/--node."
    print "Usage: " + programName + " -h for help. \n"
    sys.exit(1)

nodeConfig    = kllFuncs.readNodeConfig(configFile, node)

# Substitute custom entries into the template
userData      = kllFuncs.substituteValues( nodeConfig['udtemplate'], nodeConfig )

nodeConfig['userdata']  = userData

# Setup the EC2 Session
boto3.setup_default_session(
    profile_name = nodeConfig['awsprofile'],
    region_name  = nodeConfig['awsregion']
    )

ec2 = boto3.resource('ec2')

try:
    instanceList    = awsFuncs.createInstances(ec2, nodeConfig, dryRun)
except SystemExit as detail:
    if detail.code == 1:
        print "Override the DryRun flag with -y or --yes.\n"
    raise
except:
    print("Unexpected error when calling awsFuncs.createInstances:\n", sys.exc_info()[0])
    sys.exit(1)

instance = instanceList[0]

print "[", node, "]"
print "InstanceId    :", instance.instance_id
print "InstanceType  :", instance.instance_type
print "PrivateIp     :", instance.private_ip_address
print "Subnet        :", instance.subnet
print "ImageId       :", instance.image_id
print "VpcId         :", instance.vpc_id
print
