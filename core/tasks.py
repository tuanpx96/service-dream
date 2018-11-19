import boto3
from botocore.exceptions import ClientError
from celery import shared_task, Task
from celery.utils.log import get_task_logger
from django.conf import settings

_logger = get_task_logger(__name__)


class AWSSESTask(Task):
    """AWS Simple Email Service Task"""
    _client = None

    @property
    def client(self):
        if self._client is None:
            self._client = boto3.client(
                'ses',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION)
            return self._client


@shared_task(base=AWSSESTask, bind=True)
def send_email(self, subject, body_html, from_email, recipient_list, body_text=None):
    CHARSET = 'UTF-8'
    message = {
        'Body': {
            'Html': {
                'Charset': CHARSET,
                'Data': body_html,
            },
        },
        'Subject': {
            'Charset': CHARSET,
            'Data': subject,
        },
    }
    if body_text:
        message['Body']['Text'] = {
            'Charset': CHARSET,
            'Data': body_text,
        }

    try:
        self.client.send_email(
            Destination={'ToAddresses': recipient_list},
            Message=message,
            Source=from_email,
        )
    except ClientError as e:
        _logger.error(e.response['Error']['Message'])


