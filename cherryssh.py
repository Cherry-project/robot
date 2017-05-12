import numpy
import os
import glob
import threading
import time
import requests
import json

from pypot.server.httpserver import HTTPRobotServer

from pypot.server.zmqserver import ZMQRobotServer

from pypot.creatures import AbstractPoppyCreature

from attach_primitive import attach_primitives

from pypot.robot import from_json

from pypot.primitive.move import MoveRecorder

from primitives.movePlayer import PlayMove

from primitives.speak import *

from primitives.voice import Voice


class Cherry(AbstractPoppyCreature):
         
    @classmethod
    def setupssh(cls):

        print "Robot setup started :"

        json_data = open('./config/conf.json')
        data = json.load(json_data)
        json_data.close()

        port = data['robot']['port']
        name = data['robot']['name']

        try:
            cls.robot = from_json('config/torso.json')
        except Exception as e:
            try:
                cls.robot = from_json('config/torso.json')
            except Exception as e:
                raise
            else:
                print "Robot configuration successful !"
            finally:
                pass
            raise
        else:
            print "Robot configuration successful !"

        # Attach Gtts
        try:
            cls.robot.attach_primitive(SayFR(cls.robot), 'say_fr')
            cls.robot.attach_primitive(SayEN(cls.robot), 'say_en')
            cls.robot.attach_primitive(SayES(cls.robot), 'say_es')
            cls.robot.attach_primitive(SayDE(cls.robot), 'say_de')

        except Exception as e:
            print "Something goes wrong with gTTS"
            raise
        else:
            print "gTTS attached successfully"

        print "Starting motors configuration"

        for m in cls.robot.motors:
            m.compliant_behavior = 'dummy'
            m.goto_behavior = 'minjerk'
            m.moving_speed = 80
        
        for m in cls.robot.motors:
            m.compliant = False
            m.goal_position = 0
            print m

        for m in cls.robot.head:
            m.compliant = True
        try:
            attach_primitives(cls.robot)
        except:
            print "Primitives not attached "
        else:
            print "Primitives attached successfully"       
        
        try:
            cls.robot.torso_idle_motion.start()
            cls.robot.upper_body_idle_motion.start()
            # cls.robot.head_idle_motion.start()
        except Exception as e:
            raise
        else:
            pass

        # Voice.silent(text="Setup done",lang='en')
        try:
            Voice.silent(text="Bonjour, je m'appelle "+name+", ravi de vous rencontrer.",lang='fr')
        except:
            print "WARNING : no response from google tts engine : Check internet connectivity"
        else:
            pass

        return cls.robot

    @classmethod
    def connectssh(cls):
        json_data = open('./config/conf.json')
        data = json.load(json_data)
        json_data.close()

        ip = data['server']['addr']
        port = data['server']['port']

        host = data['ssh']['host']
        remotePort = data['ssh']['port']

        name = data['robot']['name']

        print "Starting to ping the server"

        response = os.system("ping -c 1 " + str(ip))

        if response != 0:
            while response != 0:
                response = os.system("ping -c 1 " + str(ip))
                time.sleep(5)

        url = "http://"+str(ip)+"/ssh/setupssh?id="+str(name)

        # print url

        try: 
            r = requests.get(url)
        except:
            print "Request error"
        else:
            result = json.loads(r.text.split("\n")[0])
            if result['port'] > remotePort:
                remotePort = result['port']
            print "ssh -R "+ str(remotePort) +":localhost:"+ str(remotePort) +" "+ host + " &"
            os.system("ssh -R "+ str(remotePort) +":localhost:"+ str(remotePort) +" "+ host + " &")
            cls.port = remotePort
            pass
        return cls.port

    @classmethod
    def servessh(cls):
        json_data = open('./config/conf.json')
        data = json.load(json_data)
        json_data.close()
        
        ip = data['robot']['addr']
        print cls.port
        
        try:
            server = HTTPRobotServer(cls.robot, host=str(ip), port=str(cls.port))
        except:
            print "Unable to create server object"
        else:
            print "Server configuration done"
            try:
                threading.Thread(target=lambda: server.run()).start()
            except:
                print "Unable to start server"
            else:
                print "server started successfully"
                # Voice.silent(text="Server working",lang='en')





