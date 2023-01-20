#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import uuid
from urllib.parse import urlparse, parse_qs
import json

class base_app:
    def __init__(self) -> None:
        self._headers = {'Content-Type':'text/html'}
        self._call_backs = {}
        self.reset_call()
        
    def do_json_response(self):
        self._headers = {'Content-Type':'application/json'}

    def do_html_response(self):
        self._headers = {'Content-Type':'text/html'}

    def set_header(self, name, value):
        self._headers[name] = value

    def get_headers(self):
        return self._headers

    def register_call_back(self, reference):
        id=uuid.uuid4()
        self._call_backs[str(id)] = {'url':reference}
        
        return id

    def get_call_backs(self):
        return self._call_backs

    def set_content(self, content):
        self._content = content

    def get_content(self):
        return self._content

    def error(self, err):
        if not err in self._errors:
            self._errors.append(err)

    def get_errors(self):
        return self._errors

    def set_title(self, title):
        self._title=title

    def get_title(self):
        return self._title

    def get_output_for_content_type(self, content_type):
        return "No output generator for Content-Type "+str(content_type)

    def get_HTML(self):
        alert_errors='<div class="alert alert-error">'+"<br>".join(self.get_errors())+'</div>'
        content = '<div>'+str(self.get_content())+'</div>'
        return '''<html><head><title>{title}</title>
        <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
        </head><body><h1>{title}</h1>{alerts}{container}<form method="post" action="#"><button name="submit" value="1">Post something</button></form></body></html>'''.format(title=self.get_title(), alerts=alert_errors, container=content )

    def index(self, call_data):
        self._content="index is the root application method. If you want to see other data than this, overload the function in your own application. "
        self._content+="call_data:"+str(call_data)
        return "success"

    def reset_call(self):
        self._content = False
        self._title = 'HTTP Server Application'
        self._errors = []


class server_base_handle(BaseHTTPRequestHandler):
    def write_headers(self):
        for header_name in self.application.get_headers().keys():
            self.send_header(header_name, self.application.get_headers()[header_name])

        self.end_headers()

    def respond_by_content_type(self, application_result):
        self.write_headers()
        if self.application.get_headers()['Content-Type'] == 'application/json':
            self.wfile.write(bytes(json.dumps({'data':self.application.get_content(), 'result':application_result, 'errors':self.application.get_errors()}),"utf8"))

        elif self.application.get_headers()['Content-Type'] == 'text/html':
            self.wfile.write(bytes(self.application.get_HTML(),"utf8"))
        
        else:
            self.wfile.write(bytes(self.application.get_output_for_content_type(self.application.get_headers()['Content-Type'])),"utf8")
        
        self.application.reset_call()

    def run_application_method(self, post_data=False):
        parsed_path=urlparse(self.path)
        if parsed_path.path != '/':
            path_items=parsed_path.path.split('/')
            method_name=path_items[1] #! There is always at least 1 /

        else:
            method_name='index'
            path_items=False
        
        try:
            application_method=getattr(self.application, method_name)
            call_data={
                'address_string':self.address_string(),
                'post_data':post_data,
                'query_parameters':parse_qs(parsed_path.query)
            }
            if path_items is not False:
                call_data['sub_path']=path_items[2:]
            
            method_result=application_method(call_data)
 
        except Exception as e:
            method_result=False
            self.application.error("Application method "+str(method_name)+" might not exist. This is what Python says: ")
            self.application.error(str(e))
            
        return method_result

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body_content=self.rfile.read(length).decode('utf8')
        if self.headers['Content-Type'] == 'application/x-www-form-urlencoded':
            app_result=self.run_application_method(post_data=parse_qs(body_content))
        elif self.headers['Content-Type'] == 'application/json':
            app_result=self.run_application_method(post_data=parse_qs(json.loads(body_content)))
        else:
            app_result=self.run_application_method(body_content)

        self.send_response(200)
        self.respond_by_content_type(app_result)

    def do_GET(self):
        app_result=self.run_application_method()
        self.send_response(200)
        self.respond_by_content_type(app_result)

class server_handle(server_base_handle):
    application=None

class http_server_app:
    '''Makes use of the Python built-in server to provide an api over a network to your application.
    Basic server class, does nothing else than checking that an application has been provided and runs the forever instance.'''
    def __init__(self) -> None:
        self._port=8800

    def set_listening_port(self, port):
        self._port=port

    def set_application(self, app):
        server_handle.application=app

    def serve_forever(self):
        if server_handle.application == None:
            print("Could not start up server, application not set, use http_server_app.set_application to set an application")
        else:
            httpd=HTTPServer(('localhost',self._port), server_handle)
            httpd.serve_forever()
