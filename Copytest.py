import boto3
wksDestination = boto3.client('workspaces', region_name='us-west-2')
wksSource = boto3.client('workspaces', region_name='us-east-1')

def collect_sourceImages():
    allImages = wksSource.describe_workspace_images()
    listofImages = []
    
    for img in allImages['Images']:
        # Keeping a dict of Name and ImageId for copy purposes.
        DetailedImages = {
            'Name': img['Name'],
            'ImageId': img['ImageId']
        }
        
        listofImages.append(DetailedImages)
        
    return(listofImages)


def collect_destinationImages():
    allImages = wksDestination.describe_workspace_images()
    listofImages = []
    
    for img in allImages['Images']:
        # We only keep the image names in a list because that's all we need.
        listofImages.append(img['Name'])
        
    return(listofImages)


def copy_wksImage(name, imgId):
    try:
        wksDestination.copy_workspace_image(Name=name, Description='Copied with Lambda', SourceImageId=imgId, SourceRegion='us-east-1')
        print('Copying {} to us-west-2...'.format(imgId))
    except Exception as error:
        print('Copy Failed', error)

source_Images = collect_sourceImages()
destination_Images = collect_destinationImages()

# Loop through all source images.
for source_img in source_Images:
    # Check if the image exists in the destination region.
    if source_img['Name'] not in destination_Images:
        # Copy the image!
        print("Copying {}...".format(source_img['Name'])
        copy_wksImage(source_img['Name'], source_img['ImageId'])
              
