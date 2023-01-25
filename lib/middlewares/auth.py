from werkzeug.wrappers import Request, Response, ResponseStream

import os


class AuthMiddleware:
    """
    Authorization middleware. Handles API key validation
    """
    def __init__(self, app):
        self.app = app
        self.api_key = os.environ['API_KEY']

    def __call__(self, environ, start_response):
        request = Request(environ)
        api_key = request.args.get('api_key')

        if api_key == self.api_key:
            return self.app(environ, start_response)

        response = Response(
            '{"message": "Invalid api_key"}',
            mimetype='application/json',
            status=401
        )
        return response(environ, start_response)
