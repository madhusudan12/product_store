from functools import wraps
from django.core.cache import cache
from django.conf import settings
from rest_framework.response import Response

CACHE_TTL = getattr(settings, 'CACHE_TTL', 15 * 60)


def cache_response(prefix):
    """
    Decorator that caches the response of a retrieve/list viewset methods.

    Args:
        prefix (str): The prefix for the cache key.

    Returns:
        function: The wrapped viewset method that caches its response.
    """
    def decorator(viewset_method):
        @wraps(viewset_method)
        def wrapped_viewset_method(self, request, *args, **kwargs):
            query_params = request.GET.urlencode()
            path_params = ":".join([str(kwargs.get(k)) for k in kwargs.keys()])
            # TODO: key can still be improved by sorting the query params
            cache_key = f"{prefix}:{path_params}:{query_params}"
            cached_data = cache.get(cache_key)
            if cached_data:
                return Response(cached_data)
            response = viewset_method(self, request, *args, **kwargs)
            cache.set(cache_key, response.data, CACHE_TTL)
            return response
        return wrapped_viewset_method
    return decorator


def str_to_bool(value):
    return value.lower() in ('true', '1', 'yes')
