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

from setuptools import setup


setup(
    name='AioNord',
    version='1.0.2',
    packages=['aionord'],
    url='https://github.com/ultrafunkamsterdam',
    license='MIT',
    author='UltrafunkAmsterdam',
    author_email='',
    install_requires=["aiohttp_socks","requests", "aiohttp"],
    description='Drop-in for either requests.Session and aiohttp.ClientSession, which directly uses the Nord VPN Network'
)
