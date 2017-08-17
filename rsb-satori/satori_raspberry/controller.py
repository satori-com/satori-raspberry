import importlib
import json
import time


from satori.rtm.client import make_client, SubscriptionMode
import satori.rtm.auth as auth

class App(object):
    def __init__(self, config_path):
        self.config = self.read_config(config_path)
        self.client = None
        self.GPIO = None
        self.skills = {}

    def run(self):
        config = self.config
        self.GPIO = self.import_gpio()

        should_authenticate = 'role' in config['satori'] and 'role_secret_key' in config['satori']
        auth_delegate = None if not should_authenticate else auth.RoleSecretAuthDelegate(
            config['satori']['role'],
            config['satori']['role_secret_key']
        )

        with make_client(
            endpoint=config['satori']['endpoint'], appkey=config['satori']['appkey'],
            auth_delegate=auth_delegate) as client:
            print("[OK] Connected to Satori RTM")
            self.client = client
            client.subscribe(config['channels']['in'], SubscriptionMode.SIMPLE, self)

            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                client.publish(config['channels']['out'], '{"state": "disconnected"}')


    def read_config(self, path):
        with open(path) as config_file:
            return json.load(config_file)

    def import_gpio(self):
        if 'dev_mode' in self.config and self.config['dev_mode']:
            import FakeRPi.GPIO as GPIO
        else:
            import RPi.GPIO as GPIO

        return GPIO

    # Subscription handlers
    def on_enter_subscribed(self):
        print("[OK] Ready to react on external commands via {} channel".format(self.config['channels']['in']))

        def check_publish_access(pdu):
            if pdu['action'] != 'rtm/publish/ok':
                raise RuntimeError('Have no permissions to publish to ' +
                                   self.config['channels']['out'])
            else:
                print("[OK] Publish permissions are OK. Rasbpery output channel is {}".format(self.config['channels']['out']))

        self.client.publish(
            self.config['channels']['out'],
            '{"state": "connected"}',
            callback=check_publish_access
        )

    def on_subscription_data(self, pdu):
        for message in pdu['messages']:
            self.handleMessage(message)

    def on_enter_failed(self, reason):
        raise RuntimeError('Have no permissions to subscribe to {}. Reason: {}'
                            .format(self.config['channels']['in'], reason))

    def handleMessage(self, message):
        print("[debg]: RECV< " + json.dumps(message))

        if 'skill' not in message or 'action' not in message:
            log_message = "no 'skill' or 'action' field in message: " + json.dumps(message)
            print("[FAIL] " + log_message)
            self.client.publish(
                self.config['channels']['out'],
                {"error": log_message}
            )
            return False

        skill = message['skill']
        action = message['action']

        if skill not in self.config['skills']:
            log_message = "Skill '{}' was not found in registered skills".format(module)
            print("[FAIL] " + log_message)
            self.client.publish(
                self.config['channels']['out'],
                {"error": log_message}
            )
            return False

        if action not in self.config['skills'][skill]['actions']:
            log_message = "Skill '{}' has no '{}' action".format(skill, action)
            print("[FAIL] " + log_message)
            self.client.publish(
                self.config['channels']['out'],
                {"error": log_message}
            )
            return False

        if skill not in self.skills:
            try:
                self.skills[skill] = importlib.import_module(
                    self.config['skills'][skill]['package']
                ).Skill(self.GPIO, self.client)
                getattr(self.skills[skill], action)(message)
            except (AttributeError, ImportError, TypeError) as err:
                print("[FAIL] Error {} in module {}".format(err, skill))
        