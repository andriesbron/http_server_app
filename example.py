#!/usr/bin/env python3

#! you might need:
# import os
# import sys
# sys.path.append(os.getcwd())

from http_server_app.http_server_app import *

class testapp(base_app):
    def sayHi(self, data):
        print("Hi!", data)
        self.set_content('Hi!'+str(data))

        return True

if __name__=='__main__':

    exapp = testapp()
    
    #exapp.do_json_response()
    exapp.do_html_response()

    sapp = http_server_app()
    sapp.set_application(exapp)
    sapp.serve_forever()
