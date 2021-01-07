"""
Helper module for Amazon Workspaces
"""
import boto3


class WorkspaceHelper():
    """ Class to conglomerate available info for workspaces """
    def __init__(self,region):
        """ Init attributes for info collection """
        self.region = region
        self.client = boto3.client(
            'workspaces',
            region_name= self.region
        )

    def get_info(self, workspaceid):
        """ Gather info  for a single workspace """
        workspaces = self.client.describe_workspaces(WorkspaceIds=[workspaceid])['Workspaces'][0]
        workspace = {
            'WorkspaceId': workspaces['WorkspaceId'],
            'UserName': workspaces['UserName'],
            'BundleId' : workspaces['BundleId'],
            'DirectoryId' : workspaces['DirectoryId'],
            'State' : workspaces['State'],
            'ComputeTypeName': workspaces['WorkspaceProperties']['ComputeTypeName'],
            'RootVolumeSizeGib' : workspaces['WorkspaceProperties']['RootVolumeSizeGib'],
            'RunningMode' : workspaces['WorkspaceProperties']['RunningMode'],
            'UserVolumeSizeGib' : workspaces['WorkspaceProperties']['UserVolumeSizeGib'],
        }
        if workspace['State'] == 'AVAILABLE' :
            workspace['IpAddress'] = workspaces['IpAddress']
            workspace['ComputerName'] = workspaces['ComputerName']
        else:
            workspace['IpAddress'] = None
            workspace['ComputerName'] = None
        return workspace

    def get_wks_page(self,directoryId,nextToken):
        """ Retrieve the next page of 25 workspaces """
        if nextToken == 'None' :
                workspaces = self.client.describe_workspaces(
                    DirectoryId = directoryId,
                )
        else:
            workspaces = self.client.describe_workspaces(
                DirectoryId = directoryId,
                NextToken = nextToken
            )
        return workspaces

    def get_dir_wks(self,directoryId):
        """ Retrieve all workspaces in a directory """
        data = []
        firstRun = True
        NextToken = 'None'
        while firstRun == True or NextToken != 'None':
            result = self.get_wks_page(
                directoryId = directoryId,
                nextToken = NextToken
            )
            for wks in result['Workspaces']:
                data.append(wks)
            try: NextToken = result['NextToken']
            except: NextToken = 'None'
            firstRun = False
        return data
