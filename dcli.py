#!/usr/bin/env python
from lib.Joke_api import joke
import click
import boto3
import time

# LOGGING
import logging.config

client = boto3.client("logs")

LOG_GROUP = "cloudwatch_customlog"
LOG_STREAM = "{}-{}".format(time.strftime("%Y-%m-%d"), "logstream")

try:
    client.create_log_group(logGroupName=LOG_GROUP)
except client.exceptions.ResourceAlreadyExistsException:
    pass

try:
    client.create_log_stream(logGroupName=LOG_GROUP, logStreamName=LOG_STREAM)
except client.exceptions.ResourceAlreadyExistsException:
    pass


logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

LOGGER = logging.getLogger("simpleExample")


@click.command()
@click.option(
    "--time_s",
    default=2,
    help="How long to sleep",
)
@click.option(
    "--category",
    default="Any",
    help="Select category for joke",
)
@click.option(
    "--level",
    default=30,
    help="Sets log level",
)
def run(time_s, category, level):
    click.echo(click.style(f"Log Level {level}", fg="blue"))
    click.echo(click.style(f"category {category}", fg="green"))
    click.echo(click.style(f"Sleep {time_s}", fg="red"))
    LOGGER.setLevel(level)
    while True:
        LOGGER.debug("Debug level")
        LOGGER.info(joke(time_s, category))
        response = client.describe_log_streams(
            logGroupName=LOG_GROUP, logStreamNamePrefix=LOG_STREAM
        )

        event_log = {
            "logGroupName": "cloudwatch_customlog",
            "logStreamName": "2022-02-20-logstream",
            "logEvents": [
                {
                    "timestamp": int(round(time.time() * 1000)),
                    "message": str(joke(time_s, category)),
                }
            ],
        }

        if "uploadSequenceToken" in response["logStreams"][0]:
            event_log.update(
                {"sequenceToken": response["logStreams"][0]["uploadSequenceToken"]}
            )

        response = client.put_log_events(**event_log)


if __name__ == "__main__":
    run()
