from jinja2 import Environment, PackageLoader, select_autoescape,FileSystemLoader,nodes
from jinja2.ext import Extension


class Url(Extension):
    tags = {'url'} 

    def __init__(self, environment):
        super().__init__(environment)
    
    def parse(self, parser):
        lineno = next(parser.stream).lineno
        args = [parser.parse_expression()]
        return nodes.CallBlock(self.call_method('_url', args), [], [], []).set_lineno(lineno)
    
    def _url(self, name, caller):
        ###########pack modules
        import routes
        is_url = False
        for route in routes.urls:
            if route.name == name:
                if route.url_string == '':
                    self.url = '/'
                else: self.url = route.url_string
                is_url =True
                return self.url
        if not is_url:return ''

def renderTags(route,request):
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape= select_autoescape(['html','xml']),
        extensions=[Url]
    )
    try:
        _route = route.view(request)
    except:
        _route = route.view() 
    template = env.get_template(_route.templatePath)
    contextObj = _route.context
    __html_content__ = template.render(contextObj)

    return __html_content__


    