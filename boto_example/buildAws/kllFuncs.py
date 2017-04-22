## (c) 2017 by Kwan Lowe

def readNodeConfig(nodeConfigFile, nodeName):
    """ Reads node configuration file, returns dictionary. """ 

    import ConfigParser
    import sys
    import os.path

    config = ConfigParser.RawConfigParser()
    nodeConfigFile = os.path.expanduser(nodeConfigFile)
    
    nodeConfig={}
    try:
        config.read(nodeConfigFile)
        nodeConfig['hostname']        = config.get(nodeName, 'Hostname')
        nodeConfig['instancetype']    = config.get(nodeName, 'InstanceType')
        nodeConfig['accesskey']       = config.get(nodeName, 'AccessKey')
        secGroups                     = config.get(nodeName, 'SecGroups') 
        nodeConfig['secgroups']       = secGroups.split(",")
        nodeConfig['subnet']          = config.get(nodeName, 'Subnet') 
        nodeConfig['awsprofile']      = config.get(nodeName, 'AWSProfile')
        nodeConfig['awsregion']       = config.get(nodeName, 'AWSRegion')
        nodeConfig['awsami']          = config.get(nodeName, 'AWSAMI')
        nodeConfig['awszone']         = config.get(nodeName, 'AWSZone')
        udTemplateFile                = config.get(nodeName, 'UDTemplate')
        udTemplateFile                = os.path.expanduser(udTemplateFile)
        userDataFile                  = open(udTemplateFile, 'r')
        userDataText                  = userDataFile.read()
        ### Substitute entries in UserData
        nodeConfig['udtemplate']      = userDataText


        return nodeConfig

    except IOError:
        print "Unable to locate node configuration file " + nodeConfigFile + '.\n'
        sys.exit(3)
        raise 
    except ConfigParser.NoSectionError:
         print "Unable to locate section [" + nodeName + "]" + " in " + nodeConfigFile + ".\n"
         sys.exit(3)
    else:
         print "Unexpected error in readNodeConfig: %s" % e
         sys.exit(1)


def substituteValues( udtemplate, nodeConfig ):
    """ Replaces values in template. """

    userData     = udtemplate.replace ('<<hostname>>', nodeConfig['hostname'] )
    return userData
