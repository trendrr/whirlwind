import urllib
from tornado.web import HTTPError


def role_required(role):
    def wrap(view_func):
        def has_role(self, *args, **kwargs):
            if not self.current_user:
                if self.request.method == "GET":
                    url = self.get_login_url()
                    if "?" not in url:
                        url += "?" + urllib.urlencode(dict(next=self.request.uri))
                    self.redirect(url)
                    return
                raise HTTPError(403)
            else:
                if not self.current_user.has_role(role):
                    self.flash.error = "You do not have permissions to access the requested url"
                    self.redirect('/')
                    return

                return view_func(self, *args, **kwargs)

        return has_role
    return wrap


class route(object):
    """
    taken from http://gist.github.com/616347

    decorates RequestHandlers and builds up a list of routables handlers

    Tech Notes (or "What the *@# is really happening here?")
    --------------------------------------------------------

    Everytime @route('...') is called, we instantiate a new route object which
    saves off the passed in URI.  Then, since it's a decorator, the function is
    passed to the route.__call__ method as an argument.  We save a reference to
    that handler with our uri in our class level routes list then return that
    class to be instantiated as normal.

    Later, we can call the classmethod route.get_routes to return that list of
    tuples which can be handed directly to the tornado.web.Application
    instantiation.

    Example
    -------

    @route('/some/path')
    class SomeRequestHandler(RequestHandler):
        pass

    my_routes = route.get_routes()
    """
    _routes = []

    def __init__(self, uri):
        self._uri = uri

    def __call__(self, _handler):
        """gets called when we class decorate"""
        self._routes.append((self._uri, _handler))
        return _handler

    @classmethod
    def get_routes(self):
        return self._routes
