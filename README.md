
# http_server_app

THIS IS A DEMONSTRATION APPLICATION MEANT TO SUPPORT DEVELOPMENTS, NO GUARANTEE AND NEVER USE THIS IN PRODUCTION SITES -> MAKES USE OF HTTP SIMPLE PYTHON SERVER

Make use of python http.server to access a python application through the network (simple way)
Because it is so simple, the documentation is the code.
And maybe it is so utterly stupid that there are better solutions.
However, since, stupid solutions come from stupid minds, it is what it is.

@attention your application is referenced as a static variable, meaning, you can only use it for one application, otherwise you need to define your own classes and extend server_base_handle and define static variable application. 

after running, open a browser and point to http://localhost:8800
next point to 
http://localhost:8800/sayHi 
or 
http://localhost:8800/sayHi/to/you
Spice it up by
http://localhost:8800/sayHi/to/you/?var1=1&var2=2

Then click the submit button and see all the data appearing.
You can also post json as application/json

