"""
Helper module for Amazon Workspaces Custom Image Copy Across AWS Regions
Author: Stephen K Stetler
"""
import boto3

class ImageCopyHelper():
    # Class to copy custom images created by administrator using the private API between AWS Regions 
    def __init__(self,src_region,dst_region):
        # Init attributes for info collection 
        self.src_region=src_region
        self.dst_region=dst_region
        self.src_client=boto3.client(
            'workspaces',
            region_name = self.src_region
        )
        self.dst_client=boto3.client(
            'workspaces',
            region_name = self.dst_region
        )
    
    def copy_images(self):
        # Gather lists for all source and destination Custom Images 
        all_src_images = self.src_client.describe_workspace_images()
        all_dst_images = self.dst_client.describe_workspace_images()
        output = str('')
        # We only keep the images names in the destination list because that's all we need
        # and using a list is easier for the comparison
        list_of_dst_images = []
        for dst_img in all_dst_images['Images']:
            list_of_dst_images.append(dst_img['Name'])
        # Check source image names in the new list
        for src_img in all_src_images['Images']:
            # Check if the image exists in the destination list of names. 
            if src_img['Name'] not in list_of_dst_images:
                # Copy the image to the destination 
                try:
                    self.dst_client.copy_workspace_image(
                        Name=src_img['Name'], 
                        Description='Copied through automation', 
                        SourceImageId=src_img['ImageId'], 
                        SourceRegion=self.src_region
                    )
                    output += 'Copying {} to {}...\n'.format(
                        src_img['ImageId'], 
                        self.dst_region
                    )
                except Exception as error:
                    output += 'Copy failed for {}: {}\n'.format(
                        src_img['ImageId'],
                        error
                    )
            else:
                output += 'Nothing to copy from {} to {}\n'.format(
                    self.src_region,
                    self.dst_region
                )
        return output
 