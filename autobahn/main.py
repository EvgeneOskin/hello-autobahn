import os
import asyncio
import txaio
from autobahn.wamp.types import RegisterOptions
from autobahn import wamp
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner


class HelloComponent(ApplicationSession):

    def onConnect(self):
        self.log.info("Client connected to {}.".format(self.config.realm))
        self.join(self.config.realm, ['anonymous'])

    async def onJoin(self, defaults):
        self.log.info('client session joined {}'.format(defaults))

        self._ident = defaults.authid
        self._type = 'Python'

        results = await self.register(self)

        for res in results:
            if isinstance(res, wamp.protocol.Registration):
                # res is an Registration instance
                self.log.warning(
                    "Ok, registered procedure with registration ID {}"
                    .format(res.id)
                )
            else:
                # res is an Failure instance
                self.log.warning(
                    "Failed to register procedure: {}".format(res)
                )

    def onLeave(self, defaults):
        self.log.info('Router session closed')
        self.disconnect()

    def onDisconnect(self):
        self.log.info('Router disconnected')
        try:
            asyncio.get_event_loop().stop()
        except:
            pass

    @wamp.register('com.eoskin.hello')
    def hello(self, name):
        return ("Hello {}".format(name),)


if __name__ == "__main__":
    router_url = os.getenv('ROUTER_URL')
    realm = os.getenv('REALM')

    txaio.use_asyncio()
    txaio.start_logging(level='debug')

    runner = ApplicationRunner(url=router_url, realm=realm)
    runner.run(HelloComponent)
