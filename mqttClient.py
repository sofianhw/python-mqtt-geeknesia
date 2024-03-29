from wiringx86 import GPIOEdison as GPIO
import paho.mqtt.client as paho, os, urlparse, time

gpio = GPIO(debug=False)
analogpin = 17 
gpio.pinMode(analogpin, gpio.ANALOG_INPUT)

# Define event callbacks
def on_connect(mosq, obj, rc):
    print("rc: " + str(rc))

def on_message(mosq, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mosq, obj, level, string):
    print(string)

mqttc = paho.Client()
# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

# Uncomment to enable debug messages
#mqttc.on_log = on_log

# Parse CLOUDMQTT_URL (or fallback to localhost)
url_str = os.environ.get('CLOUDMQTT_URL', 'mqtt://USERNAME:PASSWORD@geeknesia.com:1883')
url = urlparse.urlparse(url_str)

# Connect
mqttc.username_pw_set(url.username, url.password)
mqttc.connect(url.hostname, url.port)

# Start subscribe, with QoS level 0
mqttc.subscribe("hello/world", 0)

# Publish a message
mqttc.publish("iot/live", "DEVICE_ID")

# Continue the network loop, exit when an error occurs
rc = 0
while rc == 0:
    rc = mqttc.loop()
    value = gpio.analogRead(analogpin)
    mqttc.publish("iot/data", '{"code":"USERNAME:PASSWORD","attributes":{"LDR":"'+value+'"}}')
    time.sleep(60)
print("rc: " + str(rc))
