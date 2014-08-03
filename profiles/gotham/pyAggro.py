from urlparse import urlparse, parse_qs
from IPython.display import HTML
from py4j.java_gateway import JavaGateway

_realmId, _aggro, _gateway, load_objects, search_objects = None, None, None, None, None

def _load_objects():
    return _aggro.search(_realmId, "*").getResults()

def _search_objects(query):
    return _aggro.search(_realmId, query)

def init_gotham1():
    # Assign working url retrieved from javascript to a python variable
    script = """
        <script>
            (function() {
                kernel = IPython.notebook.kernel;
                kernel.execute("url = '" + document.URL + "'");
            })();
        </script>
    """
    return HTML(script)

def init_gotham2():
    global _aggro, _realmId, _gateway, load_objects, search_objects

    # Parse url to get session info
    _params = parse_qs(urlparse(url).query)

    # Initialize Aggro service
    _gateway = JavaGateway()
    _aggro = _gateway.entry_point
    _aggro.setUserSessionToken(_params["userName"][0], int(_params["userId"][0]), _params["sessionId"][0])
    _realmId = _params["realmId"][0]

    load_objects, search_objects = _load_objects, _search_objects

