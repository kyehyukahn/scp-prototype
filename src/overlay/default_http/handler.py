import json

from message import TXEnvelop, SCPEnvelop


def not_found_handler(handler, parsed):
    if parsed.path[1:] == '':
        return handle_ping(handler, parsed)

    message = '"%s" not found' % parsed.path
    handler.response(404, message)

    return


def handle_status(handler, parsed):
    if handler.command not in ('GET',):
        handler.response(405, None)
        return

    info = json.dumps({
        'version': handler.server.version,
        'blockchain': handler.server.blockchain.to_dict(),
    }, indent=True)
    handler.response(200, info)

    return


def handle_ping(handler, parsed):
    if handler.command not in ('GET',):
        handler.response(405, None)
        return

    handler.response(200, None)

    return


def handle_get_node(handler, parsed):
    if handler.command not in ('GET',):
        handler.response(405, None)
        return

    return handler.json_response(200, handler.server.blockchain.node.to_dict())


def handle_tx_envelop(handler, parsed):
    print("handle_tx_envelop")
    if handler.command not in ('POST',):
        handler.response(405, None)
        return

    length = int(handler.headers['Content-Length'])
    data = handler.rfile.read(length).decode('utf-8')

    txEnvelop = TXEnvelop.from_string(data)
    handler.server.sequence_executor('receive_tx_envelop', txEnvelop)

    return handler.response(200, None)


def handle_scp_envelop(handler, parsed):
    if handler.command not in ('POST',):
        handler.response(405, None)
        return

    length = int(handler.headers['Content-Length'])
    scpEnvelop = SCPEnvelop.from_string(handler.rfile.read(length).decode('utf-8'))
    handler.server.sequence_executor('receive_scp_envelop', scpEnvelop)

    return handler.response(200, None)


HTTP_HANDLERS = dict(
    status=handle_status,
    ping=handle_ping,
    get_node=handle_get_node,
    tx_envelop=handle_tx_envelop,
    scp_envelop=handle_scp_envelop,
)
