from typing import Callable

class Url:
    def __init__(self, 
                 url_string,
                 view: Callable[..., object],
                 name: str = ...):
        self.url_string = url_string
        self.view = view
        self.name = name

def route(url_string: str,
         view: Callable[..., object],
         name: str = ...,) -> Url :
    return Url(url_string,view,name)


