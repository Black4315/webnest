from http.server import ThreadingHTTPServer
import socket
import contextlib
from webnest.requestHandler import RequestHandler 
import argparse
from webnest.db.treks import Handel_treks
import sys

######## http server
class CustomThreading(ThreadingHTTPServer):
    def server_bind(self):
        # Suppress exception when protocol is IPv4
        with contextlib.suppress(Exception):
            self.socket.setsockopt(
                socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        return super().server_bind()

def _get_best_family(bind, port):
    infos = socket.getaddrinfo(
        bind, port,
        type=socket.SOCK_STREAM,
        flags=socket.AI_PASSIVE,
    )
    family, type, proto, canonname, sockaddr = next(iter(infos))
    return family, sockaddr

runningMessage = """-----------------------------------
Server started on port 8000...
Starting development server at : http://127.0.0.1:8000
CTRL-C to quit the server
-----------------------------------"""
def run_server(
        HandlerClass=RequestHandler,
        ServerClass=CustomThreading,
        protocol="HTTP/1.0",port = 8000,
        bind='0.0.0.0'):
    """This runs an HTTP server on port 8000 (or the port argument)."""
    ServerClass.address_family, address = _get_best_family(bind, port)
    HandlerClass.protocol_version = protocol
    try:
        with ServerClass(address,HandlerClass)as httpd:
            host,port = httpd.socket.getsockname()[:2]
            try:
                print(runningMessage)
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nKeyboard interrupt received, exiting..") #logging
                sys.exit(0)
    except Exception as error:
        print('Error:', error) #logging
######## http server

def execute_from_args():
    """Args for handling application"""
    commands = {
        'runserver': {'help': 'Run the server for your application.','func':run_server},
        'rendertreks': {'help': 'Handling the database and migrating models.','func':Handel_treks().make_delete_trks},
        'trek': {'help': 'Handling the database and migrating models.','func':Handel_treks().trek},
    }
    parser = argparse.ArgumentParser(description='Commands for handling application')
    subparsers = parser.add_subparsers(dest='command', help='handling application')

    for choice, obj in commands.items():
          subparsers.add_parser(choice, help= obj['help'])
 
    args = parser.parse_args()

    is_command = False
    for key,value in commands.items():
        if args.command == key:
            value['func']()
            is_command = True
            break
    if not is_command:parser.print_usage()


