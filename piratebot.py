import sys
import botlib
import urllib
import urllib2
from cookielib import CookieJar
import json

if len(sys.argv) < 4:
	server = "irc.netsoc.tcd.ie"
	channel = "#piratebot"
	nick = "piratebot"
else:
	server = sys.argv[1]
	channel = "#" +  sys.argv[2]
	nick = sys.argv[3]

committee = []
todo = []
currentAcademicYear = 2013

with open('piratesURL.txt') as fURL:
	piratesAPIUrl = fURL.read().replace('\n', '')

mailmanUrl = "https://lists.netsoc.tcd.ie/cgi-bin/mailman/admin/pirates-announce/"

with open('password.txt') as fpass:
	mailmanPassword = fpass.read().replace('\n', '')
 
# Create a new class for our bot, extending the Bot class from botlib
class piratebot(botlib.Bot):
	def __init__(self, server, channel, nick, password=None):
		botlib.Bot.__init__(self, server, 6667, channel, nick)
 
		# Send nickserv password if availible
		if password != None:
			sel.protocol.privmsg("nickserv", "identify" % password)
 
	def __actions__(self):
		botlib.Bot.__actions__(self)

		if botlib.check_on_own(self.data, ">committee"):
			channel = self.get_channel()
			self.protocol.privmsg(channel, "Well")
			for i in range (len(committee)):
				self.protocol.privmsg(channel, committee[i])
 
		# >help command
		if botlib.check_on_own(self.data, ">help"):
			channel = self.get_channel()
			self.protocol.privmsg(channel, ">add argument - Adds argument to a todo list.")
			self.protocol.privmsg(channel, ">remove argument - Removes argument from the todo list.")
			self.protocol.privmsg(channel, ">done (int)index - Removes that index from the todo list.")
			self.protocol.privmsg(channel, ">todo - Lists everything in the todo list.")
			self.protocol.privmsg(channel, ">memberadd email name - Add user to VPN and mailing lists.")
			self.protocol.privmsg(channel, ">vpn - ;)")
 
		# >join command
		elif botlib.check_on_own(self.data, ">join"):
			username = self.get_username()
			channel = self.get_channel()
			new_channel = self.get_args();

			for i in range (len(committee)-1):
				if committee[i] == hostname:
					match = 1

			if match is 1:
				if channel[0] == "#":
					if len(new_channel) == 0:
						if channel[0] == "#":
							self.protocol.privmsg(channel, "Please specify a channel!")
						else:
							self.protocol.privmsg(username, "Please specify a channel!")
					elif new_channel[0][0] != "#":
						if channel[0] == "#":
							self.protocol.privmsg(channel, "That isn't a channel!")
						else:
							self.protocol.privmsg(username, "That isn't a channel!")
					else:
						self.protocol.join(new_channel[0])
			else:
				self.protocol.privmsg(channel, "You can't tell me what to do!")

		# >leave command
        elif botlib.check_on_own(self.data, ">leave"):
            self.protocol.leave(self.get_channel())

		# >say command
		elif botlib.check_on_own(self.data, ">say"):
			username = self.get_username()
			arguments = self.get_args()
			channel = arguments[0]
			if channel[0] == "#":
				message = ' '.join(arguments[1:])
				self.protocol.privmsg(channel, message)
			else:
				message = ' '.join(arguments[0:])
				self.protocol.privmsg("#pirates-com", message)
 
		# >add command
		elif botlib.check_on_own(self.data, ">add"):
			channel = self.get_channel()
			newItem = self.get_args()
			with open('todo.txt') as ftodo:
                                todo = ftodo.readlines()
                        for i in range (len(todo)):
                                todo[i] = todo[i][:len(todo[i])-1]

			if len(newItem) > 0:
				todo.append(' '.join(newItem[0:]))
				f = open('todo.txt', 'r+')
				f.truncate()
				for i in range (len(todo)):
					f.write(todo[i] + "\n")
				self.protocol.privmsg(channel, "Added!")
			else:
				self.protocol.privmsg(channel, "Tell me what to add!")
 
		# >remove command
		elif botlib.check_on_own(self.data, ">remove"):
			channel = self.get_channel()
			removeItem = self.get_args()

			with open('todo.txt') as ftodo:
                                todo = ftodo.readlines()
                        for i in range (len(todo)):
                                todo[i] = todo[i][:len(todo[i])-1]


			if len(removeItem) > 0:
				for i in range (len(todo)):
					if todo[i] == ' '.join(removeItem[0:]):
						todo.pop(i)
						f = open('todo.txt', 'r+')
						f.truncate()
						for i in range (len(todo)):
							f.write(todo[i] + "\n")
						self.protocol.privmsg(channel, "Removed")
						break
			else:
				self.protocol.privmsg(channel, "Tell me what to remove")

		# >done command
		elif botlib.check_on_own(self.data, ">done"):
			channel = self.get_channel()
			index = self.get_args()

			with open('todo.txt') as ftodo:
                                todo = ftodo.readlines()
                        for i in range (len(todo)):
                                todo[i] = todo[i][:len(todo[i])-1]


			if len(index) > 0:
				try:
					number = int(index[0])
					if len(todo) < number:
						self.protocol.privmsg(channel, "There aren't that many things on the list.")
					elif number <= 0:
						self.protocol.privmsg(channel, "That is an invalid entry.")
					else:
						todo.pop(number-1)
						f = open('todo.txt', 'r+')
                                                f.truncate()
						for i in range (len(todo)):
                                                        f.write(todo[i] + "\n")
						self.protocol.privmsg(channel, "Removed!")
				except ValueError:
					self.protocol.privmsg(channel, "That's not a number!")
			else:
				self.protocol.privmsg(channel, "You need to tell me what one I need to delete...")
 
		# >todo command
		elif botlib.check_on_own(self.data, ">todo"):
			channel = self.get_channel()
			with open('todo.txt') as ftodo:
	                	todo = ftodo.readlines()
        		for i in range (len(todo)):
	        	        todo[i] = todo[i][:len(todo[i])-1]
			if not todo:
				self.protocol.privmsg(channel, "There's nothing to do. Good job guys!")
			else:
				for i in range (len(todo)):
					self.protocol.privmsg(channel, "%s. %s" % (i+1, todo[i]))

		# >vpn command 
		elif botlib.check_on_own(self.data, ">vpn"):
			channel = self.get_channel()
			self.protocol.privmsg(channel, "Did you try running as admin?")
			
		# >memberadd command
		elif botlib.check_on_own(self.data, ">memberadd"):
			username = self.get_username()
			hostname = self.get_hostname().partition("@")[0]
			channel = self.get_channel()
			match = 0
			for i in range (len(committee)-1):
				if committee[i] == hostname:
					match = 1
			
			if match is 1:
				member_info = self.get_args()
				#channel = self.get_username()
				if len(member_info) >= 3:   # Check if both a valid email and name are provided
					
					# TODO - Need to do validate user email
			
					# Prepare request to send to pirates.ie for VPN signup
					member_values = {'name' : ' '.join(member_info[1:]),
						'email' :  member_info[0],
						'yearRegistered' : currentAcademicYear }
					apiRequest = urllib2.Request(piratesAPIUrl, urllib.urlencode(member_values))
					try:
						apiResponse = urllib2.urlopen(apiRequest) # Parse the response and provide message back to user
						apiResponseJson = json.loads(apiResponse.read())
						self.protocol.privmsg(channel, apiResponseJson['Message']+' ('+apiResponseJson['Value']+')')
					except UrlError, e:
					#except:
						e = sys.exc_info()[0]
						self.protocol.privmsg(channel, 'Could not add user to VPN list! Error: ' + str(e))
				
					# Prepare request to send to mailman for mailing list signup
					cj = CookieJar()
					urllib2opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
				
					# TODO - Need to do error checking on requests and HTTP responses
					mailmanLoginData = {'adminpw' : mailmanPassword }
					mailmanLoginResponse = urllib2opener.open(mailmanUrl, urllib.urlencode(mailmanLoginData))
				
					# Now authenticated, make POST request to add user to mailing list
					mailmanEntry = {'subscribe_or_invite' : 0,
						'send_welcome_msg_to_this_batch' :  1,
						'send_notifications_to_list_owner' : 0,
						'subscribees' : member_info[0] }
					mailmanLoginResponse = urllib2opener.open(mailmanUrl+'members/add', urllib.urlencode(mailmanEntry))
					self.protocol.privmsg(channel, "Member has been successfully added to the mailing list!")
				else:
					self.protocol.privmsg(channel, "Please enter a valid email and a name!")
			else:
				self.protocol.privmsg(channel, "You're not on committee...")
		
if __name__ == "__main__":
	print "Starting up piratebot"

	with open('committee.txt') as fcom:
		committee = fcom.readlines()
	for i in range (len(committee)):
		committee[i] = committee[i][:len(committee[i])-1]

	#with open('todo.txt') as ftodo:
	#	todo = ftodo.readlines()
	#for i in range (len(todo)):
	#	todo[i] = todo[i][:len(todo[i])-1]

	piratebot(server, channel, nick).run()
