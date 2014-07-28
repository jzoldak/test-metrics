"""
Helper methods for metrics processing.
"""

import os
import sys

def configure_datadog():
    """
    Read API key from environment vars, exiting with an error
    if they are not set.
    """
    api_key = os.environ.get('DATADOG_API_KEY')

    if api_key is None:
        print u"Must specify DataDog API key with env var DATADOG_API_KEY"
        sys.exit(1)

    else:
        return api_key
