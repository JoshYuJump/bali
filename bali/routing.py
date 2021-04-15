import functools
import inspect

from fastapi import APIRouter as FastAPIRouter, HTTPException

from bali.core import db
from .application import GzipRoute
from typing import Any, Callable, Generic, List, Optional, Type


class APIRoute(GzipRoute):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # inject sqlalchemy scope session remove to endpoint
        if not inspect.iscoroutinefunction(self.dependant.call):
            self.dependant.call = self._inject_scoped_session_clear(self.dependant.call)

    @staticmethod
    def _inject_scoped_session_clear(endpoint: callable):
        @functools.wraps(endpoint)
        def injected_endpoint(*args, **kwargs):
            try:
                return endpoint(*args, **kwargs)
            finally:
                db.remove()

        return injected_endpoint


class APIRouter(FastAPIRouter):
    def add_api_route(self, *args, **kwargs):
        kwargs.update(route_class_override=APIRoute)
        return super().add_api_route(*args, **kwargs)

    def get(self, path, *args, **kwargs):
        self.remove_api_route(path, ['GET'])
        return super().get(path, *args, **kwargs)

    def post(self, path, *args, **kwargs):
        self.remove_api_route(path, ['POST'])
        return super().post(path, *args, **kwargs)

    def patch(self, path, *args, **kwargs):
        self.remove_api_route(path, ['PATCH'])
        return super().patch(path, *args, **kwargs)

    def delete(self, path, *args, **kwargs):
        self.remove_api_route(path, ['DELETE'])
        return super().delete(path, *args, **kwargs)

    def remove_api_route(self, path: str, methods: List[str]):
        methods = set(methods)

        for r in self.routes:
            if r.path == f'{self.prefix}{path}' and r.methods == methods:
                self.routes.remove(r)

