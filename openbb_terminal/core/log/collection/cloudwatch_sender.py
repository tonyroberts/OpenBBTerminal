import boto3
from watchtower import CloudWatchLogHandler

from openbb_terminal.core.log.constants import LOG_GROUP_NAME
from openbb_terminal.core.log.generation.settings import AWSSettings


def log_stream_exists(client, log_group, log_stream):
    response = client.describe_log_streams(
        logGroupName=log_group, logStreamNamePrefix=log_stream
    )
    log_streams = response.get("logStreams", [])
    return any(stream["logStreamName"] == log_stream for stream in log_streams)


def create_cloudwatch_handler(
    aws_settings: AWSSettings,
    log_stream: str,
) -> CloudWatchLogHandler:
    """
    Create a CloudWatch handler for the logger.

    This function creates a CloudWatch Logs client and a log stream if
    they do not already exist. The Python logger is then configured to send logs
    to AWS CloudWatch Logs.

    Parameters
    ----------
    aws_settings : AWSSettings
        Stores credentials for AWS access
    log_stream : str
        Name of the log stream

    Returns
    -------
    CloudWatchLogHandler
        A logging handler for sending logs to CloudWatch
    """
    # Set up the AWS SDK
    session = boto3.session.Session(
        aws_access_key_id=aws_settings.aws_access_key_id,
        aws_secret_access_key=aws_settings.aws_secret_access_key,
        region_name=aws_settings.aws_default_region,
    )

    # Create a CloudWatch Logs client
    logs_client = session.client(service_name="logs")

    # Create a log group and log stream if they don't already exist
    if not log_stream_exists(logs_client, LOG_GROUP_NAME, log_stream):
        logs_client.create_log_stream(
            logGroupName=LOG_GROUP_NAME, logStreamName=log_stream
        )

    # Configure the Python logger to send logs to AWS CloudWatch Logs
    handler = CloudWatchLogHandler(
        boto3_client=logs_client,
        log_group=LOG_GROUP_NAME,
        stream_name=log_stream,
        create_log_group=False,
        create_log_stream=False,
    )
    return handler
