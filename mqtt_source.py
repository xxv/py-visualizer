from anim import Source
from mqtt_base import MQTTBase


class MQTTSource(MQTTBase, Source):
    """Event source from an MQTT topic"""

    def __init__(self, config_file, topic=None):
        MQTTBase.__init__(self, config_file=config_file)
        Source.__init__(self)
        self._topic = topic or self.mqtt_config['topic']

    def on_connect(self, client, userdata, flags, conn_result):
        self.mqtt.subscribe(self._topic)
        print("Connected to MQTT server.")

    def on_message(self, client, userdata, message):
        event = {
            'topic': message.topic,
            'payload': message.payload
            }
        self.trigger(event)

    def loop_forever(self):
        MQTTBase.loop_forever(self)

    def stop(self):
        self.mqtt.disconnect()
