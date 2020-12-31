import boto3
wksDestination = boto3.client('workspaces', region_name='us-west-2')

def collect_sourceImages():
    wksSource = boto3.client('workspaces', region_name='us-east-1')
    allImages = wksSource.describe_workspace_images()
    listofImages = []
    for img in allImages['Images']:
        DetailedImages = {
            'Name': img['Name'],
            'ImageId': img['ImageId']
        }
        listofImages.append(DetailedImages.copy())
    return(listofImages)


def collect_destinationImages():
    allImages = wksDestination.describe_workspace_images()
    listofImages = []
    for img in allImages['Images']:
        DetailedImages = {
            'Name': img['Name']
        }
        listofImages.append(DetailedImages.copy())
    return(listofImages)


def copy_wksImage(name, imgId):
    try:
        wksDestination.copy_workspace_image(Name=name, Description='Copied with Lambda', SourceImageId=imgId, SourceRegion='us-east-1')
        print(f'Copying {imgId} to us-west-2...')
    except:
        print('Copy Failed')


i = 0 # Total iterations of Destination Images
j = 0 # Total iterations of Source Images
source_Images = collect_sourceImages()
destination_Images = collect_destinationImages()
total_srcimages = len(source_Images)
total_desimages = len(destination_Images)

while j < total_srcimages:   
    while i < total_desimages:
        in_Test = False
        in_Test = list(destination_Images)[i].get('Name') in list(source_Images)[j].get('Name') # Using 'in' will determine a boolean value that is easier to calculate than a loop
        if in_Test == False:
            print(f"Copying {list(source_Images)[j].get('Name')}...")
            copy_wksImage(list(source_Images)[j].get('Name'),list(source_Images)[j].get('ImageId'))
        i += 1
    j += 1
    i = 0
