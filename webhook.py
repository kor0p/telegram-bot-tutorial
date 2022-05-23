import json
from time import sleep
from http.server import BaseHTTPRequestHandler, HTTPServer

from telebot import types

import config
from main import bot


class handler(BaseHTTPRequestHandler):
    server_version = 'WebhookHandler/1.0'

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        body = json.loads(post_data.decode())

        bot.process_new_updates([types.Update.de_json(body)])

        self.send_response(204)
        self.end_headers()


def run_server():
    httpd = HTTPServer(('', 5000), handler)
    print('Starting httpd...\n')
    sleep(1)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('Stopping httpd...\n')


if __name__ == '__main__':
    bot.set_webhook(url=config.WEBHOOK_URL)

    run_server()
