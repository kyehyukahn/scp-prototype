import collections
import configparser
import importlib
import logging
import pathlib
import uuid

from main import Application
from overlay import Endpoint, get_network_module, BaseServer
from scp import SCP, Node, node_factory

from utils import (
    get_local_ipaddress,
    logger,
    ArgumentParserShowDefaults,
)


parser = ArgumentParserShowDefaults()
parser.add_argument('conf', help='ini config file for server node')
log = None

logger.set_argparse(parser)


# NETWORK_MODULE = get_network_module('default_http')
NETWORK_MODULE = importlib.import_module('.default_http', 'overlay')

def main(options):
    config = collections.namedtuple(
        'Config',
        ('node_name', 'port', 'threshold', 'validators', 'faulty_percent'),
    )(uuid.uuid1().hex, 8001, 51, [], 0)

    if not pathlib.Path(options.conf).exists():
        parser.error('conf file, `%s` does not exists.' % options.conf)

    if not pathlib.Path(options.conf).is_file():
        parser.error('conf file, `%s` is not valid file.' % options.conf)

    conf = configparser.ConfigParser()
    conf.read(options.conf)
    log.info('conf file, `%s` was loaded', options.conf)

    config = config._replace(node_name=conf['node']['name'])
    config = config._replace(port=int(conf['node']['port']))
    config = config._replace(threshold=int(conf['node']['threshold_percent']))

    if conf.has_option('faulty', 'faulty_percent'):
        config = config._replace(faulty_percent=int(conf['faulty']['faulty_percent']))

    log.debug('loaded conf: %s', config)

    validator_list = []
    for i in filter(lambda x: len(x.strip()) > 0, conf['node']['validator_list'].split(',')):
        validator_list.append(Endpoint.from_uri(i.strip()))

    config = config._replace(validators=validator_list)
    log.debug('Validators: %s' % config.validators)

    node = node_factory(
        config.node_name,
        Endpoint(NETWORK_MODULE.SCHEME, get_local_ipaddress(), config.port),
        config.faulty_percent
    )

    transport = NETWORK_MODULE.Transport(bind=('0.0.0.0', config.port))

    # consensus_module = get_fba_module('isaac')
    consensus = SCP(
        node,
        config.threshold,
        tuple(map(lambda x: Node(x.extras['name'], x), config.validators)),
        transport,
    )

    log.metric(node=node.name, data=node.to_dict())

    application = Application(consensus, transport)

    base_server = BaseServer(application)
    base_server.start()

    return


if __name__ == '__main__':
    options = parser.parse_args()
    logger.from_argparse(logger, options)

    log = logger.get_logger(__name__)
    logger.set_level(logging.FATAL, 'http')
    logger.set_level(logging.FATAL, 'ping')

    log.debug('options: %s', options)
    log.debug('log settings: %s', logger.info)

    main(options)
