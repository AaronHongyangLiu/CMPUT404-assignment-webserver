#  coding: utf-8 
import SocketServer
import os
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        command = self.data.split('\n')[0] # first line of the self.data
        print(command+"\r\n")
        (status, path, mime) = self.validateCommand(command)
        self.send(status,path, mime)

    def validateCommand(self, command_line):
        """
        validate the first line, return a status code, a path, and a mime type
        - 404: path not found
        - 405: Method Not Allowed
        - 200: OK
        """
        tokens = command_line.split(' ')
        if tokens[0].upper() != "GET": # method not allowed
            return (405,None, None)
        else:
            if tokens[1] == "/":
                return (200, "./www/index.html", "text/html")
            else:
                path = "./www"
                if tokens[1][-1] == "/": # if token ends with /
                    path += tokens[1]+"index.html"
                    if os.path.isfile(path):
                        return (200, path, "text/html")
                    else:
                        return (404, None, None)

                elif tokens[1][-4:] == ".css":
                    path += tokens[1]
                    if os.path.isfile(path):
                        return (200, path, "text/css")
                    else:
                        return (404, None, None)

                elif tokens[1][-5:] == ".html":
                    path += tokens[1]
                    if os.path.isfile(path):
                        return (200, path, "text/html")
                    else:
                        return (404, None, None)

                else:
                    path += tokens[1]+"/index.html"
                    if os.path.isfile(path):
                        return (200, path, "text/html")
                    else:
                        return (404, None, None)

    def send(self,status_code,path,mimetype):
        if status_code == 404:
            header = "HTTP/1.1 404 Not Found\r\n"
            mime = "Content-Type: text/html\r\n\r\n"

            # this html content is written by wachowicz (http://blog.wachowicz.eu/?p=256)
            content = "<!DOCTYPE html>" \
                      "<html>" \
                      "<body>" \
                      "<p>" \
                      "Error 404: File not found" \
                      "</p>" \
                      "</body>" \
                      "</html>\r\n"

        elif status_code == 405:
            header = "HTTP/1.1 405 Method Not Allowed\r\n"
            mime=""
            content = ""
        elif status_code == 200:
            header = "HTTP/1.1 200 OK\r\n"
            mime = "Content-Type: %s\r\n\r\n" % mimetype
            file = open(path)
            content = file.read().strip()+"\r\n"
            file.close()

        print(header)
        self.request.send(header+mime+content)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
