from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import os
from requests import get, put
import urllib.parse
import json


def run(handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


class HttpGetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        def fname2html(fname, uploaded):
            if not uploaded:
                return f"""
                    <li onclick="fetch('/upload', {{'method': 'POST', 'body': '{fname}'}})">
                        {fname}
                    </li>
                """
            else:
                return f"""
                    <li style="background-color: rgba(0, 200, 0, 0.25)" onclick="fetch('/upload', {{'method': 'POST', 'body': '{fname}'}})">
                        {fname}
                    </li>
                """


        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        uploaded = self.read_dir_stat()
        files = "\n".join([fname2html(f, f in uploaded) for f in os.listdir("pdfs")])
        self.wfile.write("""
            <html>
                <head>
                    <meta charset="UTF-8">
                </head>
                <body>
                    <ul>
                      {files}
                    </ul>
                </body>
            </html>
        """.format(files=files).encode())

    def read_dir_stat(self):
        resp = get(f"https://cloud-api.yandex.net/v1/disk/resources?path=TestDir%2F",
                   headers={"Authorization": ""})
        data = json.loads(resp.text)
        names = [item["name"] for item in data["_embedded"]["items"]]
        return set(names)


    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        fname = self.rfile.read(content_len).decode("utf-8")
        local_path = f"pdfs/{fname}"
        ya_path = f"TestDir/{urllib.parse.quote(fname)}"
        resp = get(f"https://cloud-api.yandex.net/v1/disk/resources/upload?path={ya_path}",
                   headers={"Authorization": ""})
        print(resp.text)
        upload_url = json.loads(resp.text)["href"]
        print(upload_url)
        resp = put(upload_url, files={'file': (fname, open(local_path, 'rb'))})
        print(resp.status_code)
        self.send_response(200)
        self.end_headers()


run(handler_class=HttpGetHandler)
