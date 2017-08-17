import importlib
import json
import time
import traceback
import sys
import os
import threading

from satori.rtm.client import Client, SubscriptionMode
import satori.rtm.auth as auth
import RPi.GPIO as GPIO

class Controller(object):
    def __init__(self, config_path):
        self.config = self.read_config(config_path)
        self.client = None
        self.GPIO = None
        self.skills = {}

    def connect(self):
        config = self.config
        self.GPIO = GPIO
        self.GPIO.setmode(self.GPIO.BCM)

        should_authenticate = 'role' in config['satori'] and 'role_secret_key' in config['satori']
        auth_delegate = None if not should_authenticate else auth.RoleSecretAuthDelegate(
            config['satori']['role'],
            config['satori']['role_secret_key']
        )

        client = Client(
            endpoint=config['satori']['endpoint'],
            appkey=config['satori']['appkey'],)
        ready_event = threading.Event()

        class Observer:
            def on_enter_connected(self):
                ready_event.set()

            def on_enter_stopped(self):
                ready_event.set()

        client.observer = Observer()
        client.start()
        if not ready_event.wait(70):
            if client.last_connecting_error():
                client.dispose()
                raise RuntimeError(
                    "Client connection timeout, last connection error: {0}".format(
                        client.last_connecting_error()))
            else:
                raise RuntimeError("Client connection timeout")
        ready_event.clear()
        if not client.is_connected():
            client.dispose()
            raise RuntimeError(
                "Client connection error: {0}".format(
                    client.last_connecting_error()))

        auth_mailbox = []

        def auth_callback(auth_result):
            auth_mailbox.append(auth_result)
            ready_event.set()

        if auth_delegate:
            client.authenticate(auth_delegate, callback=auth_callback)

            if not ready_event.wait(20):
                client.dispose()
                print('[FAIL] Authentication process has timed out')
                raise Exception('Authentication process has timed out')

            auth_result = auth_mailbox[0]

            if type(auth_result) == auth.Error:
                raise Exception(auth_result.message)

            print('[OK] Auth success in make_client')

        print("[OK] Connected to Satori RTM")
        client.subscribe(config['channels']['in'], SubscriptionMode.SIMPLE, self)

        self.client = client
    
    def skill(self, skill):
        if not self.activate_skill(skill):
            return False

        return self.skills[skill]

    def wait_messages(self):
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.client.publish(self.config['channels']['out'], '{"state": "disconnected"}')
            self.cleanup()
            os._exit(0)
    
    def cleanup(self):
        self.GPIO.cleanup()

    def is_dev(self):
        return 'dev_mode' in self.config and self.config['dev_mode']

    def read_config(self, path):
        with open(path) as config_file:
            return json.load(config_file)

    def activate_skill(self, skill):
        try:
            if skill not in self.skills:
                self.skills[skill] = importlib.import_module(
                    self.config['skills'][skill]['package']
                ).Skill(self.GPIO, self.client, self.config['channels']['out'])
                self.skills[skill].name = skill
        except:
            err = sys.exc_info()[0]
            print("[FAIL] Error '{}' in module '{}'".format(err, skill))
            print(traceback.format_exc())
            self.client.publish(
                self.config['channels']['out'],
                {"error": err}
            )
            return False

        return True

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

        if 'skill' not in message or 'api' not in message:
            log_message = "no 'skill' or 'action' field in message: " + json.dumps(message)
            print("[FAIL] " + log_message)
            self.client.publish(
                self.config['channels']['out'],
                {"error": log_message}
            )
            return False

        skill = message['skill']
        api = message['api']

        if skill not in self.config['skills']:
            log_message = "Skill '{}' was not found in registered skills".format(skill)
            print("[FAIL] " + log_message)
            self.client.publish(
                self.config['channels']['out'],
                {"error": log_message}
            )
            return False

        if api not in self.config['skills'][skill]['api']:
            log_message = "Skill '{}' has no '{}' api action".format(skill, api)
            print("[FAIL] " + log_message)
            self.client.publish(
                self.config['channels']['out'],
                {"error": log_message}
            )
            return False

        
        if not self.activate_skill(skill):
            return False

        try:    
            getattr(self.skills[skill], api)(message)
        except:
            err = sys.exc_info()[0]
            print("[FAIL] Error '{}' in module '{}'".format(err, skill))
            print(traceback.format_exc())
            self.client.publish(
                self.config['channels']['out'],
                {"error": err}
            )
            return False

        return True
