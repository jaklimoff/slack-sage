import aiohttp


class RequestsMixin:
    """
    Allow handlers to use async requests
    """
    session = aiohttp.ClientSession()

    async def _request(self, method, url, **kwargs):
        async with getattr(self.session, method)(url, **kwargs) as resp:
            return await resp.text()

    async def get(self, url, **kwargs):
        return await self._request("get", url, **kwargs)
