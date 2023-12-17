import paho.mqtt.client as mqtt

def send_mqtt_message(message, topic, qos=1):
    client = mqtt.Client()
    username = "wow0422796353"
    password = "123456"

    if username and password:
        client.username_pw_set(username, password)

    host = "140.131.115.152"
    port = 1883 
    client.connect(host, port)
    client.publish(topic, message, qos=qos)
    client.disconnect()


