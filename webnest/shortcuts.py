###########pack modules
from settings import *
from webnest.path import add_path,read_file

class RenderInfo:
    def __init__(self,
                 templatePath,
                 context= None,
                 content= str,
                 ):
        self.templatePath = templatePath
        self.context = context
        self.content = content

def render(templatePath,context= None)->RenderInfo:
    """Function to render template"""
    htmlfile_path = add_path(TEMPLATES_DIR,templatePath)
    __html_content__ = read_file(htmlfile_path)

    return RenderInfo(templatePath,context,__html_content__)

