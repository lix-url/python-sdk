import json as json_module
from typing import Any, Dict, List, Optional


class MockResponse:
    def __init__(self, status_code: int, body: str = ''):
        self.status_code = status_code
        self._body = body

    def json(self) -> Any:
        return json_module.loads(self._body) if self._body else {}


class MockSession:
    def __init__(self):
        self._requests: List[Dict] = []
        self._responses: List[MockResponse] = []
        self._chain_inited = False

    def request(self, method: str, url: str, headers: Optional[Dict] = None, json: Any = None, **kwargs) -> MockResponse:
        self._requests.append({
            'method': method,
            'url': url,
            'headers': headers or {},
            'json': json,
        })
        if self._chain_inited and not self._responses:
            raise RuntimeError('No responses in the chain')
        if self._chain_inited:
            return self._responses.pop(0)
        return MockResponse(200, '')

    def add_response(self, status_code: int, body: str = '') -> 'MockSession':
        self._chain_inited = True
        self._responses.append(MockResponse(status_code, body))
        return self

    def get_requests(self) -> List[Dict]:
        return self._requests

    def clear(self) -> 'MockSession':
        self._requests = []
        self._responses = []
        self._chain_inited = False
        return self
