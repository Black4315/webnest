from http.server import BaseHTTPRequestHandler
import os
from urllib.parse import urlparse, parse_qs
import urllib.parse as parse
import json

###########pack modules
import routes
from settings import ALLOWED_HOSTS,STATIC_DIR
localhosts = ['127.0.0.1','localhost']


mime_types = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.json': 'application/json',
    '.xml': 'application/xml',
    '.txt': 'text/plain',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.woff': 'font/woff',
    '.woff2':'font/woff2',
    '.ttf': 'font/ttf',
    '.otf': 'font/otf',
    '.pdf': 'application/pdf',
    '.zip': 'application/zip',
    '.mp4': 'video/mp4',
    '.mp3': 'audio/mpeg',
    '.wav': 'audio/wav',
    '.ico': 'image/x-icon',
    '.bmp': 'image/bmp',
    '.tiff': 'image/tiff',
    '.csv': 'text/csv',
    '.md': 'text/markdown',
    '.webp': 'image/webp',
}

class HttpRequest:
    """HTTP request."""

    def __init__(self, method, path, headers,POST):
        self.method = method
        self.path = path
        self.headers = headers
        self.FILES = {}
        self.GET = self._parse_query_params()
        self.POST = POST
        self.COOKIES = {}
        self.META = {}
        self.path_info = urlparse(self.path)

    def _parse_query_params(self):
        parsed_path = urlparse(self.path)
        return parse_qs(parsed_path.query)
    
    def __repr__(self) -> str:
        return f'<HttpRequest {self.method} {repr(self.path)}>'


class RequestHandler(BaseHTTPRequestHandler):
    Request = {}
    POST= {}

    def _handle_request(self):
        self.host = self.headers.get('HOST')
        if self._is_host_allowed():
            from webnest.tags import renderTags
            
            parsed_path = urlparse(self.path)
            query_params = parse_qs(parsed_path.query)
            self.Request = HttpRequest(
                method=self.command,
                path=self.path,
                headers=self.headers,
                POST=self.POST
            )

            if self.path.startswith('/static/'):
                _, ext = os.path.splitext(self.path)
                file_dir = STATIC_DIR+self.path[1:].replace('static','')
                mime_type = mime_types.get(ext, 'application/octet-stream')

                with open(file_dir, 'rb') as file:
                    self._send_responses(       
                        status=200,
                        content_type=mime_type, 
                        responeText=file.read())
                return
                
            is_routed = False
            for route in routes.urls: 
                if self.path == f'/{route.url_string}'or self.path == f'/{route.url_string}?{parsed_path.query}':
                    self._send_responses(
                        status=200,
                        content_type='text/html', 
                        responeText=renderTags(route,self.Request).encode('utf-8'))

                    is_routed = True
                    break

            if not is_routed:
                self._send_responses(
                    status=404,
                    content_type='text/html', 
                    responeText=b'<h1>404 Not Found</h1>')
        else:
            self._send_responses(
                    status=403,
                    content_type='text/html', 
                    responeText=f"<h1>403 Access forbidden using `{self.host}` it look like it's not in ALLOWED_HOSTS in settings</h1>".encode())
            
    def do_GET(self): 
        self._handle_request()

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            parsed_data = parse_qs(post_data)
            self.POST=parsed_data
            self._handle_request()
            # self._init_request()
            # self.Request.session['form_data'] = {k: v[0] for k, v in parsed_data.items()}
            
            # # Redirect to the same page (GET request) after processing POST data
            # self.send_response(303)  # 303 See Other
            # self.send_header('Location', self.path)  # Redirect to the same path
            # self.send_header('Set-Cookie', f'sessionid={self.Request.COOKIES.get("sessionid")}; Path=/')  # Maintain session cookie
            # self.end_headers()

        except Exception as e:
            error_message = json.dumps({'error': str(e)})
            self._send_responses(
                status=400,content_type='application/json', responeText=error_message.encode('utf-8'))

    def _is_host_allowed(self):
        return self.host[:self.host.find(':')] in localhosts or self.host[:self.host.find(':')] in ALLOWED_HOSTS
    
    def _send_responses(self ,status:int,content_type:str, responeText:...):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()
        self.wfile.write(responeText)
