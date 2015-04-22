# encoding: utf-8
"""Mimamori

Usage: mimamori.py [--use_dogstatsd=<use_dd> --statsd_host=<host> --statsd_port=<port>\
                    --dd_api_key=<api_key> --dd_app_key=<app_key> --host_name=<host_name>] (ADDRESS NAME)...
       mimamori.py -h | --help

options:
    -h, --help  show this help message and exit.
    --use_dogstatsd=<use_dd>  Use Dogstasd [default: 1].
    --statsd_host=<host>      Dogstasd host [default: localhost].
    --statsd_port=<port>      Dogstasd port [default: 8125].
    --dd_api_key=<api_key>    Api key.
    --app-key=<app_key>       App key.
    --host_name=<host_name>   Host name [default: dev_mimamori].

"""

from docopt import docopt
from gattlib import DiscoveryService
from datadog import initialize
from datadog import api as dd_api
from datadog import statsd

targets = {'00:1B:DC:44:15:75': u'papa',
           '00': u'kosuke'}

use_dogstatsd = False
statsd_host = 'localhost'
statsd_port = 8125
dd_api_key = ''
dd_app_key = ''
host_name = 'dev_mimamori'


def _dict2list(tags={}):
    return [u"{k}:{v}".format(k=k, v=v) for k, v in tags.items()]


def metric_datadog(metric_name, value=1.0, tags={}):
    """
    post to Datadog service
    :param metric_name:
    :param value:
    :param tags:
    :return:
    """

    if metric_name:
        dd_tags = _dict2list(tags)
        if int(use_dogstatsd):
            initialize(statsd_host=statsd_host, statsd_port=statsd_port)
            statsd.gauge(metric=metric_name, value=value, tags=dd_tags)
        elif dd_api_key:
            keys = {
                'api_key': dd_api_key,
                'app_key': dd_app_key
            }
            initialize(**keys)
            dd_api.Metric.send(metric=metric_name, points=value, host=host_name, tags=dd_tags)


if __name__ == '__main__':

    metric_name = u'mimamori.home'

    args = docopt(__doc__)

    use_dogstatsd = args.get('--use_dogstatsd', True)
    statsd_host = args.get('--statsd_host', 'localhost')
    statsd_port = args.get('--statsd_port', 8125)
    dd_api_key = args.get('--dd_api_key', '')
    dd_app_key = args.get('--dd_app_key', '')
    host_name = args.get('--host_name', 'dev_mimamori')
    targets = dict(zip(args.get('ADDRESS'), args.get('NAME')))
    #Discover BLE Devices
    service = DiscoveryService("hci0")
    devices = service.discover(6)
    #Check Address and post metrics
    for x in targets.keys():
        tags = dict(user=targets[x])
        if x in [dk for dk in devices.keys() if dk]:
            value = 1.0
        else:
            value = -1.0
        metric_datadog(metric_name=metric_name, value=value, tags=tags)
