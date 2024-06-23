from werkzeug.wrappers import Request, Response
import os

class middleware():
    def __init__(self, app):
        self.app = app
        self._secret = os.environ.get('SERVICE_SECRET')

    def __call__(self, environ, start_response):
        request = Request(environ)
        secret = request.headers['secret']
        if secret == self._secret and secret is not None:
            return self.app(environ, start_response)

        res = Response(u'Authorization failed', mimetype= 'text/plain', status=401)
        return res(environ, start_response)