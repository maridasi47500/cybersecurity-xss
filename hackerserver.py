#!/usr/bin/env python3
"""
License: MIT License
Copyright (c) 2023 Miel Donkers

Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
# my server
import time, socket, threading
from http.server import test as _test
from socketserver     import ThreadingMixIn
from pic import Pic
from http.cookies import SimpleCookie
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
                pass


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'image/*')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))

        mypic=Pic("virus").get_html()
        self._set_response()
        self.wfile.write(mypic.get_html())

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        mypic=Pic("virus").get_html()
        self._set_response()
        self.wfile.write(mypic.get_html())

def run(server_class=ThreadedHTTPServer, handler_class=S, port=8766,host="localhost"):
    logging.info('Starting httpd...\n'+str(port))
    _test(handler_class,server_class,port=port,bind=host)

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 3:
        run(port=int(argv[1]),host=argv[2])
    elif len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
