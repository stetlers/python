import boto3
import json

REGION = 'us-east-1'
CLIENT = boto3.client('workspaces', region_name=REGION)
PAGE_SIZE = 1
LIST_OF_WORKSPACES = []
PAGINATOR = CLIENT.get_paginator('describe_workspaces')

def collect_workspaces():
    is_more = False
    while is_more: 
        responder = PAGINATOR.paginate(PaginationConfig={ 'PageSize': PAGE_SIZE, 'NextToken': next_token })
        for result in responder:
            if 'Workspaces' not in result:
                # If nothing is found in the page, iterate to evaluate the next set
                continue
            for workspace in result['Workspaces']:
                # Keep adding the WorkSpaces so many at a time to the function
                LIST_OF_WORKSPACES.append(workspace)
            if responder.get('NextToken'):
                next_token = responder.get('NextToken')
            else:
                is_more = False
    else:
        responder = PAGINATOR.paginate(PaginationConfig={ 'PageSize': PAGE_SIZE })
        for result in responder:
            if 'Workspaces' not in result:
                # If nothing is found in the page, iterate to evaluate the next set
                continue
            for workspace in result['Workspaces']:
                # Keep adding the WorkSpaces so many at a time to the function
                LIST_OF_WORKSPACES.append(workspace)
            if responder.get('NextToken'):
                    next_token = responder.get('NextToken')
            else:
                is_more = False
    return LIST_OF_WORKSPACES


if __name__ == "__main__":
    for wks in collect_workspaces():
        print(wks)