import SimpleHTTPServer
import SocketServer
from threading import Thread

PORT = 8999

def serve(port=PORT):
    handler = SimpleHTTPServer.SimpleHTTPRequestHandler

    class TestServer(SocketServer.TCPServer):
        allow_reuse_address = True

    httpd = TestServer(("", PORT), handler)
    print 'Serving test HTTP server at port', PORT

    httpd_thread = Thread(target=httpd.serve_forever)
    httpd_thread.setDaemon(True)
    httpd_thread.start()