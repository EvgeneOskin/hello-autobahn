import os
from autobahn import wamp
from autobahn.wamp.exception import ApplicationError
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner


users = {
    "john": {
        "ticket": "some-random-string-for-the-user",
        'role': 'frontend'
    }
}

class AuthComponent(ApplicationSession):

    def onConnect(self):
        self.log.info("Client connected to {}.".format(self.config.realm))
        self.join(self.config.realm, ['ticket'], 'authenticator')

    def onChallenge(self, challenge):
        print('challenge', os.getenv('SECRET_TICKET'))
        if challenge.method == 'ticket':
            return os.getenv('SECRET_TICKET')
        else:
            raise Exception("Invalid auth method")

    async def onJoin(self, details):
        try:
            await self.register(self)
        except:
            self.log.error('Fail to register authenticator')

    def onLeave(self, defaults):
        self.log.info(f'Router session closed:\n${defaults}')
        self.disconnect()

    def onDisconnect(self):
        self.log.info('Router disconnected')
        try:
            asyncio.get_event_loop().stop()
        except:
            pass

    @wamp.register('com.eoskin.authenticate')
    def authenticate(self, realm, authid, details):
        if authid in users:
            user = users[authid]
            ticket = details['ticket']
            if ticket == user['ticket']:
                return user['role']
            else:
                raise ApplicationError('com.invalid_ticket', "Invalid ticket")
        else:
            raise ApplicationError('com.no_such_user', 'Invalid authid')


if __name__ == '__main__':
    router_url = os.getenv("ROUTER_URL")
    realm = os.getenv('REALM')

    runner = ApplicationRunner(url=router_url, realm=realm)
    runner.run(AuthComponent)
