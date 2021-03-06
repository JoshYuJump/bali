from pydantic import BaseModel
from typing import List, Optional

from bali.decorators import action
from bali.resource import Resource
from bali.schemas import GetRequest, ListRequest


GREETERS = [{'id': i, 'content': 'Hi, number %s' % i} for i in range(10)]


class Greeter(BaseModel):
    id: int
    content: str


class GreeterFilter(BaseModel):
    ids: List[int]


class GreeterResource(Resource):

    schema = Greeter

    @action()
    def get(self, pk=None):
        return [g for g in GREETERS if g.get('id') == pk][0]

    @action()
    def list(self, schema_in: ListRequest):
        return GREETERS[:schema_in.limit]

    @action()
    def create(self, schema_in: schema):
        return {'id': schema_in.id, 'content': schema_in.content}

    @action()
    def update(self, schema_in: schema, pk=None):
        return {'id': pk, 'content': schema_in.content}

    @action()
    def delete(self, pk=None):
        return {'result': True}

    @action(detail=False)
    def recents(self):
        return GREETERS[:2]

    @action(detail=True)
    def items_recents(self, pk=None):
        return [g for g in GREETERS if g.get('id') == pk]

    @action(detail=False, methods=['post'])
    def custom_create(self, schema_in: GreeterFilter):
        processed = schema_in
        return GREETERS[0]
