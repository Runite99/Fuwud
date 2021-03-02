from wsgiref.simple_server import make_server
from pyramid.config import Configurator
import os

REST_SERVER = os.environ['REST_SERVER']

if __name__ == '__main__':
#  config = Configurator()
    with Configurator() as config:

        config.include('pyramid_jinja2')
        config.add_jinja2_renderer('.html')
        config.add_route('main', '/')
        
        # --- Navbar Routes
        config.add_route('compliments', '/compliments')
        config.add_route('terminal', '/terminal')
        config.add_route('hosting', '/hosting')
        config.add_route('status', '/status')
        config.add_route('questions', '/questions')
        
        # --- Internal Routses
        config.add_route('directory', '/directory')
        config.add_static_view(name='/', path='./html_files/public', cache_max_age=3600)
        config.scan('views')
        app = config.make_wsgi_app()
    
    server = make_server('0.0.0.0', 5000, app)
    server.serve_forever()
