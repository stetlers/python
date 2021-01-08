"""
Perform lookups on my AWS Account using a module
"""

#import helpermodule_amazonworkspaces
import helpermodule_amznwksimagecopy
copy = helpermodule_amznwksimagecopy.ImageCopyHelper('us-east-1','eu-west-2')
print(copy.copy_images())

#DIRECTORY = 'd-9067615ecb'
#WORKSPACE = 'ws-hfk1xk03b'
#INFO = helpermodule_amazonworkspaces.WorkspaceHelper('us-east-1')
#print(INFO.get_dir_wks(DIRECTORY))

#print(INFO.get_info(WORKSPACE))