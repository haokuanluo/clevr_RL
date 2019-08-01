import boto3

cos = boto3.resource(
            service_name="s3",
            aws_access_key_id="e40b956720ad494f82db225b0980b984",
            aws_secret_access_key="468361dddc271d9222c50f5f25824057262d7c08927340a7",
            endpoint_url="https://s3-api.us-geo.objectstorage.softlayer.net"
        )
for bucket in cos.buckets.all():
   if bucket.name in 'tdw':
       tdw_bucket = bucket
       print("Bucket found. Deleting port tracking file")
       tdw_bucket.delete_objects(  Delete={
            'Objects': [
                {
                    'Key': 'tracker.csv'
                },
            ],
            'Quiet': True |False
        },
            MFA='string',
            RequestPayer='requester',
            BypassGovernanceRetention=True |False)
       break