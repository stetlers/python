"""
Helper module for Amazon Workspaces Custom Image Copy Across AWS Regions
Author: Stephen K Stetler
"""
import boto3

class ImageCopyHelper():
    """ Class to copy custom images created by administrator using the private API between AWS Regions """
    def __init__(self,src_region,dst_region):
        """ Init attributes for info collection """
        self.src_region = src_region
        self.dst_region = dst_region
        self.src_client = boto3.client(
            'workspaces',
            src_region_name = self.src_region
        )
        self.dst_client = boto3.client(
            'workspaces',
            dst_region_name = self.dst_region
        )
    
    def copy_images(self):
        """ Gather lists for all source and destination Custom Images """
        all_src_images = self.src_client.describe_workspace_images()
        all_dst_images = self.dst_client.describe_workspace_images()
        for src_img in all_src_images:
            """ Check if the image exists in the destination region. """
            if src_img not in all_dst_images:
                """ Copy the image to the destination """
                try:
                    self.dst_client.copy_workspace_image(
                        Name=src_img[Name], 
                        Description='Copied through automation', 
                        SourceImageId=src_img[ImageId], 
                        SourceRegion=self.src_region
                    )
                    output += f'Copying {} to {}...'.format(
                        scr_img[ImageId], 
                        self.src_region
                    )
                except Exception as error:
                    output += f'Copy failed for {}'.format(
                        src_img[ImageId]
                    )
            else:
                output += f'Nothing to copy from {} to {}'.format(
                    self.src_region,
                    self.dst_region
                )
    return output
 