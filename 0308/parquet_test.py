import pandas as pd
import boto3
from io import BytesIO



AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY


data1 = {
    'a' : [1,2,3],
    'b' : [2,3,4],
    'c' : [5,6, None]
}

data2 = {
    'b' : [20,30],
    'c' : [50,60],
    'd' : [10,20]
}

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

file1 = BytesIO()
file2 = BytesIO()

df1.to_parquet(file1)
df2.to_parquet(file2)

file1.seek(0)
file2.seek(0)

s3 = boto3.client('s3')
bucket = 'with-datalab'

s3.upload_fileobj(file1, bucket, 'datamart/l1/montly_metrics/test1.parquet')
s3.upload_fileobj(file2, bucket, 'datamart/l1/montly_metrics/test2.parquet')