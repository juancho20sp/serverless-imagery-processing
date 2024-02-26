import json
import boto3
import os
def lambda_handler(event, context):
    
    s3 = boto3.client("s3")
    outbucket = os.environ['OUTPUT_BUCKET']
    
    # This assumes the batch size is 1
    record = json.loads(event['Records'][0]['body'])
    
    x_offset = record['chip_info']['orig_x']
    y_offset = record['chip_info']['orig_y']
    
    # Get window size 
    x_window = record['chip_info']['x_window']
    y_window = record['chip_info']['y_window']
    
    chipname = record['chip_info']['chipname']
    
    out_file_name = os.path.splitext(chipname)[0]+'.json'
    
    # Project chip coords back to original image coords
    for label in record['Labels']:
        for instance in label['Instances']:
            bbox = instance['BoundingBox']
            width = bbox['Width']
            height = bbox['Height']
            left = bbox['Left']
            top = bbox['Top']
            
            # convert
            left = x_offset + (left * x_window)
            top = y_offset + (top * y_window)
            height = height * x_window
            width = width * y_window
            
            bbox['Width'] = width
            bbox['Height'] = height
            bbox['Left'] = left
            bbox['Top'] = top
            
    
    # Write to S3
    s3.put_object(Body=json.dumps(record), Bucket=outbucket,Key=out_file_name )  
        
    return event

