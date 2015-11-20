

def contextualise_resource(resource_class, supervisor):

    class ContextualisedResource(resource_class):

        def __init__(self, *args, **kwargs):
            super().__init__(supervisor, *args, **kwargs)

    # We must prevent name collision in flask_restful
    ContextualisedResource.__name__ += '_{0}'.format(resource_class.__name__)
    return ContextualisedResource
