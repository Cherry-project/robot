import requests
import json
from gtts import gTTS
import pygame
from HTMLParser import HTMLParser
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Voice(object):
	@classmethod
	def go(cls,text,lang):
		

		# Proceed special caracteres
		print HTMLParser().unescape(text).decode().encode('utf-8')
		text_encoded = HTMLParser().unescape(text).decode().encode('utf-8')

		if len(text_encoded) >= 100:
			text_split_list = text_encoded.split(" ")
			text_split = ""
			text_list = []

			for phrase_split in text_split_list:
				if len(phrase_split + " ") + len(text_split) < 100:
					text_split += phrase_split + " "
				else:
					text_list.append(text_split)
					text_split = ""
					if len(phrase_split + " ") + len(text_split) < 100:
						text_split += phrase_split + " "
			if len(text_split) != 0:
				text_list.append(text_split)
				
			for phrase in text_list:
				tts = gTTS(phrase,lang=lang)
				tts.save("./tmp/temp.mp3")		
				pygame.mixer.init()
				pygame.mixer.music.load("./tmp/temp.mp3")
				pygame.mixer.music.play()

				while pygame.mixer.music.get_busy():
					pass
		else:
			tts = gTTS(text_encoded,lang=lang)
			tts.save("./tmp/temp.mp3")		
			pygame.mixer.init()
			pygame.mixer.music.load("./tmp/temp.mp3")
			pygame.mixer.music.play()

			while pygame.mixer.music.get_busy():
				pass

		
		# load the configuration file that give the server addr and port for requests 
		json_data = open('./config/conf.json')
		data = json.load(json_data)
		json_data.close()

		# we need the server addr+port and the robot name so the server know which robot has ended his move
		ip = data['server']['addr']
		port = data['server']['port']
		name = data['robot']['name']

		# create the url for the request
		url = "http://"+str(ip)+":"+str(port)+"/robot/speakfinished/"

		# send the post with the robot name request to the server
		try: 
			requests.post(url, data = {'id':str(name)})
		except:
			# print "Request error"
			pass
		else:
			pass
			# print "Request sent !"

	@classmethod
	def silent(cls,text,lang):
		tts = gTTS(text, lang=lang)
		tts.save("./tmp/temp.mp3")

		pygame.mixer.init()
		pygame.mixer.music.load("./tmp/temp.mp3")
		pygame.mixer.music.play()

		while pygame.mixer.music.get_busy():
			pass


