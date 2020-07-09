"""

                                                                                                                    dddddddd
                    iiii                   NNNNNNNN        NNNNNNNN                                                 d::::::d
                   i::::i                  N:::::::N       N::::::N                                                 d::::::d
                    iiii                   N::::::::N      N::::::N                                                 d::::::d
                                           N:::::::::N     N::::::N                                                 d:::::d
  aaaaaaaaaaaaa   iiiiiii    ooooooooooo   N::::::::::N    N::::::N   ooooooooooo   rrrrr   rrrrrrrrr       ddddddddd:::::d
  a::::::::::::a  i:::::i  oo:::::::::::oo N:::::::::::N   N::::::N oo:::::::::::oo r::::rrr:::::::::r    dd::::::::::::::d
  aaaaaaaaa:::::a  i::::i o:::::::::::::::oN:::::::N::::N  N::::::No:::::::::::::::or:::::::::::::::::r  d::::::::::::::::d
           a::::a  i::::i o:::::ooooo:::::oN::::::N N::::N N::::::No:::::ooooo:::::orr::::::rrrrr::::::rd:::::::ddddd:::::d
    aaaaaaa:::::a  i::::i o::::o     o::::oN::::::N  N::::N:::::::No::::o     o::::o r:::::r     r:::::rd::::::d    d:::::d
  aa::::::::::::a  i::::i o::::o     o::::oN::::::N   N:::::::::::No::::o     o::::o r:::::r     rrrrrrrd:::::d     d:::::d
 a::::aaaa::::::a  i::::i o::::o     o::::oN::::::N    N::::::::::No::::o     o::::o r:::::r            d:::::d     d:::::d
a::::a    a:::::a  i::::i o::::o     o::::oN::::::N     N:::::::::No::::o     o::::o r:::::r            d:::::d     d:::::d
a::::a    a:::::a i::::::io:::::ooooo:::::oN::::::N      N::::::::No:::::ooooo:::::o r:::::r            d::::::ddddd::::::dd
a:::::aaaa::::::a i::::::io:::::::::::::::oN::::::N       N:::::::No:::::::::::::::o r:::::r             d:::::::::::::::::d
 a::::::::::aa:::ai::::::i oo:::::::::::oo N::::::N        N::::::N oo:::::::::::oo  r:::::r              d:::::::::ddd::::d
  aaaaaaaaaa  aaaaiiiiiiii   ooooooooooo   NNNNNNNN         NNNNNNN   ooooooooooo    rrrrrrr               ddddddddd   ddddd


            Usage:

            # 1
            from aionord import AioNord
            client = AioNord(username, password)

            # 2
            r = await client.get('https://httpbin.org/ip')
            body = await r.read()

            # 3 - to use another server:
            session._servers.pop(0)
            # go to 2

            after about 4 servers changes you will notice immediately when you hit the limits.
                you can use await session.get_best_servers() and go back to # 1 and contnue


"""

import logging
from pprint import pformat

import aiohttp
from aiohttp_socks import ProxyConnector, ProxyType


logging.getLogger(__name__).addHandler(logging.NullHandler())

TYPE_PROXY = 'proxy'
TYPE_SSL_RROXY = 'proxy_ssl'
TYPE_SOCKS_PROXY = 'socks'


class AioNord(aiohttp.ClientSession):
    """
    AioNord Main class
    """
    API_URL = 'https://api.nordvpn.com/v1'
    MAX_CLIENT_CONNECTIONS = 5


    def __init__(self, username, password, **kw):
        """Creates a new instance of Nord

        :param str username:
        :param str password:
        :key **kw: directly passed to aiohttp.ClientSession

        """
        self.username = username
        self.password = password
        self._servers = list()
        self._session = None
        self._current = None
        super(AioNord, self).__init__(**kw)


    async def get_servers(self):
        async with aiohttp.ClientSession() as session:
            r = await session.get(self.API_URL + '/servers')
            return map(Server, await r.json())


    async def get_best_servers(self):
        servers = await self.get_servers()
        for server in servers:
            for technology in server.technologies:
                if technology.identifier in (TYPE_PROXY, TYPE_SOCKS_PROXY, TYPE_SSL_RROXY):
                    if server not in self._servers:
                        self._servers.append(server)
                        self._servers = sorted(self._servers, key=lambda x: x.load)


    async def _request(self, method, url, **kw):
        if not self._servers:
            await self.get_best_servers()
        best5 = self._servers[0:5]
        for server in best5:
            self._current = server

            logging.getLogger(__name__).warning('using {}'.format(server.hostname))
            try:
                connector = ProxyConnector(
                    proxy_type=ProxyType.HTTP,
                    host=server.hostname,
                    password=self.password,
                    username=self.username,
                    port=80,
                    verify_ssl=False)

                self._connector = connector
                return await super()._request(method, url, **kw)
            except Exception as e:
                logging.getLogger(__name__).exception(e, exc_info=True)
                continue


class Struct(object):


    def __init__(self, data):
        for name, value in data.items():
            setattr(self, name, self._wrap(value))


    def _wrap(self, value):
        if isinstance(value, (tuple, list, set, frozenset)):
            return type(value)([self._wrap(v) for v in value])
        else:
            return Struct(value) if isinstance(value, dict) else value


    def __repr__(self):
        return pformat(
            {k: v for k, v in self.__dict__.items()
             if k[0] != '_'}, depth=4, indent=20, sort_dicts=True
        )


class Server(Struct):


    @property
    def load(self):
        return self._load


    @load.setter
    def load(self, val):
        self._load = val


    @property
    def hostname(self):
        return self._hostname


    @hostname.setter
    def hostname(self, value):
        self._hostname = value


    @property
    def locations(self):
        return self._locations


    @locations.setter
    def locations(self, value):
        self._locations = value


    @property
    def technologies(self):
        return self._technologies


    @technologies.setter
    def technologies(self, value):
        self._technologies = value


    @property
    def station(self):
        return self._station


    @station.setter
    def station(self, value):
        self._station = value
