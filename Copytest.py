import boto3
wks_destination = boto3.client('workspaces', region_name='us-west-2')
wks_source = boto3.client('workspaces', region_name='us-east-1')

def collect_source_images():
    all_images = wks_source.describe_workspace_images()
    list_of_images = []
    for img in all_images['Images']:
        # Keeping a dict of Name and ImageId for copy purposes.
        DetailedImages = {
            'Name': img['Name'],
            'ImageId': img['ImageId']
        }
        list_of_images.append(DetailedImages)    
    return(list_of_images)


def collect_destination_images():
    all_images = wks_destination.describe_workspace_images()
    list_of_images = []
    for img in all_images['Images']:
        # We only keep the image names in a list because that's all we need.
        list_of_images.append(img['Name'])    
    return(list_of_images)


def copy_wks_image(name, imgId):
    try:
        wks_destination.copy_workspace_image(Name=name, Description='Copied with Lambda', SourceImageId=imgId, SourceRegion='us-east-1')
        print('Copying {} to us-west-2...'.format(imgId))
    except Exception as error:
        print('Copy Failed', error)

source_images = collect_source_images()
destination_images = collect_destination_images()

# Loop through all source images.
for source_img in source_images:
    # Check if the image exists in the destination region.
    if source_img['Name'] not in destination_images:
        # Copy the image!
        copy_wks_image(source_img['Name'], source_img['ImageId'])
    else:
        print("Nothing to copy.")