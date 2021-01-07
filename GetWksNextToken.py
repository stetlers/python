"""
Perform lookups on my AWS Account using a module
"""

import helpermodule_amazonworkspaces

DIRECTORY = 'd-9067615ecb'
INFO = helpermodule_amazonworkspaces.WorkspaceHelper('us-east-1')
print(INFO.get_dir_wks(DIRECTORY))