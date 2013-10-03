# -*- coding=utf -*-

import json

try:
    from werkzeug.exceptions import HTTPException
except:
    # No need to bind objects here to dependency-sink, as the user
    # will be notified when he tries to use Slicer or run_server about
    # the missing package
    HTTPException = object


class ServerError(HTTPException):
    code = 500
    error_type = "default"
    def __init__(self, message=None, exception=None, **details):
        super(ServerError, self).__init__()
        self.message = message
        self.exception = exception
        self.details = details
        self.help = None

    def get_body(self, environ):
        error = {
            "message": self.message,
            "type": self.__class__.error_type
        }

        if self.exception:
            error["reason"] = str(self.exception)

        if self.details:
            error.update(self.details)

        string = json.dumps({"error": error}, indent=4)
        return string

    def get_headers(self, environ):
        """Get a list of headers."""
        return [('Content-Type', 'application/json')]


class RequestError(ServerError):
    error_type = "request"
    code = 400


class NotFoundError(ServerError):
    code = 404
    error_type = "not_found"
    def __init__(self, obj, objtype=None, message=None):
        super(NotFoundError, self).__init__(message)
        self.details = { "object": obj }

        if objtype:
            self.details["object_type"] = objtype

        if not message:
            self.message = "Object '%s' of type '%s' was not found" % (obj, objtype)
        else:
            self.message = message


class AggregationError(ServerError):
    code = 400