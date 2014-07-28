"""
Post performance stats to DataDog

Example usage:

    export DATADOG_API_KEY=xxxx
    python metrics.perf_stats testeng.foo '{"percentile99":4552,"errorPercentage":0}'

This will post the following metrics to datadog, with the current timestamp:

testeng.foo.percentile99 ==> 4552
testeng.foo.errorPercentage ==> 0

See http://docs.datadoghq.com/api/#metrics for API details.
"""
import sys
import time
import json
from dogapi import dog_http_api
from helpers import configure_datadog


USAGE = u"USAGE: {prog} PREFIX_STRING METRICS_JSON"

def report_metrics(prefix, metrics):
    """
    Send metrics to DataDog for each item in the metrics dict.

    :Args:
     - prefix: String to prepend to the metric name
     - metrics: JSON-encoded dict of stats
    """
    series = []

    now = time.time()
    for key, value in metrics.iteritems():
        metric = '{prefix}.{key}'.format(prefix=prefix, key=key)
        point = [(now, value)]
        series.append({'metric':metric, 'points':point})

    if len(series) > 0:
        print u"Sending {}".format(series)
        dog_http_api.metrics(series)


def main():
    """
    Report performance metrics to DataDog.

    Use positional arguments as this will be kicked off
    with a Jenkins Post build task.

    See https://wiki.jenkins-ci.org/display/JENKINS/Post+build+task
    """
    if len(sys.argv) != 3:
        print USAGE.format(prog=sys.argv[0])
        sys.exit(1)

    prefix = sys.argv[1]
    metrics = sys.argv[2]

    print "PREFIX: '{}'".format(prefix)
    print "METRICS: '{}'".format(metrics)

    try:
        metrics_dict = json.loads(metrics)
    except ValueError:
        print "Could not parse metrics '{}' as JSON".format(metrics)
        sys.exit(1)

    print "Configuring DataDog..."
    dog_http_api.api_key = configure_datadog()

    print "Reporting metrics to DataDog..."
    report_metrics(prefix=prefix, metrics=metrics_dict)

    print "Done."


if __name__ == "__main__":
    main()
