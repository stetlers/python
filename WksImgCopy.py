import boto3
wks_destination = boto3.client('workspaces', region_name='us-west-2')
wks_source = boto3.client('workspaces', region_name='us-east-1')

def collect_images():
    all_src_images = wks_source.describe_workspace_images()
    all_des_images = wks_destination.describe_workspace_images()
    list_of_src_images = []
    list_of_des_images = []
    for src_img in all_src_images['Images']:
        # Keeping a dict of Name and ImageId for copy from source purposes.
        detail_src_images = {
            'Name': src_img['Name'],
            'ImageId': src_img['ImageId']
        }
        list_of_src_images.append(detail_src_images)
    for des_img in all_des_images['Images']:
        # We only keep the images names in the destination list because that's all we need.
        list_of_des_images.append(des_img['Name'])
    return(list_of_src_images, list_of_des_images)


def copy_wks_image(name, imgId):
    try:
        wks_destination.copy_workspace_image(Name=name, Description='Copied with Lambda', SourceImageId=imgId, SourceRegion='us-east-1')
        print('Copying {} to us-west-2...'.format(imgId))
    except Exception as error:
        print('Copy Failed:', error)


source_images, destination_images = collect_images()

# Loop through all source images.
for source_img in source_images:
    # Check if the image exists in the destination region.
    if source_img['Name'] not in destination_images:
        # Copy the image!
        copy_wks_image(source_img['Name'], source_img['ImageId'])
    else:
        print("Nothing to copy.")