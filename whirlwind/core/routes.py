class RouteLoader(object):
    
    @staticmethod
    def load(package_name,include_routes_file=True):
        loader = RouteLoader()
        return loader.init_routes(package_name,include_routes_file)
        
    def init_routes(self,package_name,include_routes_file=True):
        import pkgutil,sys
        from whirlwind.view.decorators import route
        
        package = __import__(package_name)
        controllers_module = sys.modules[package_name]
        
        prefix = controllers_module.__name__ + "."
        
        for importer, modname, ispkg in pkgutil.iter_modules(controllers_module.__path__, prefix):
            module = __import__(modname)
        
        #grab the routes defined via the route decorator
        url_routes = route.get_routes()
        
        #add the routes from our route file
        if include_routes_file:
            from config.routes import route_list #@UnresolvedImport
            url_routes.extend(route_list)


        return url_routes