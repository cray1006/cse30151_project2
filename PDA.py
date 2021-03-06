#! /usr/bin/python -tt

#Christopher Ray
#Professor Blanton
#CSE 30151
#24 March 2015

#PDA.py
#declaration and implementation of PDA class for use in a DPDA

from stack import stack

class PDA(object):	#defining PDA class
	def __init__(self):	#defining __init__ function
		self.my_stack = stack()	#the stack
		self.Q = []	#list of states
		self.A = []	#list containing input alphabet
		self.Z = []	#list containing stack input alphabet
		self.T = []	#list containing transitions
		self.S = []	#list containing start state
		self.F = []	#list containing final accepting states
		self.current = self.S	#initializing the current state


	def debug(self):	#defining debug function for testing purposes 
		print self.my_stack.PRINT()
		print self.Q
		print self.A
		print self.Z
		print self.T
		print self.S
		print self.F
		print self.current


	def initialize(self, I):	#defining initialize function
		for line in I:	#read in lines from input file I
			line = line.rstrip('\n')	#remove the ending newline character from line
			line = line.replace(':', ' ').replace(',', ' ').split()	#tokenize the line
		
			i = 1
			
			if(line[0] == 'Q'):	#reading in inputs for the list of states
				while(i < len(line)):
					self.Q.append(line[i])	#adding elements to the list of states
					i = i + 1
			elif(line[0] == 'A'):	#reading in inputs for the input alphabet
				while(i < len(line)):
					self.A.append(line[i])	#adding elements to the input alphabet
					i = i + 1
			elif(line[0] == 'Z'):	#reading in inputs for the stack input alphabet
				while(i < len(line)):
					self.Z.append(line[i])	#adding elements to the stack input alphabet
					i = i + 1
			elif(line[0] == 'T'):	#reading in a transition
				#Each transition is stored as a dictionary with a current state(cs), input (i), stack input(s), next state(ns)
					#and item to push on the stack (p)
				self.T.append({'cs':  line[1], 'i':  line[2], 's':  line[3], 'ns':  line[4], 'p':  line[5]})
			elif(line[0] == 'S'):	#reading in inputs for the start state
				while(i < len(line)):
					self.S.append(line[i])	#adding elements to the start state list
					i = i + 1
			elif(line[0] == 'F'):	#reading in inputs for the final accept states
				while(i < len(line)):
					self.F.append(line[i])	#adding elements to the accept state list
					i = i + 1


	def transition(self, x, y):	#defining transition function
		if(y == 1):	
			top = self.my_stack.POP()	#popping an element off the stack
			if(top == None):	#print an error message if the stack is somehow empty
				print "Empty stack"
				return 0
		else:
			top = 'e'	#this is done when pushing the end of stack character on to the stack

		if((self.A.count(x) <= 0) and (x != 'e')):	#checking if the input x is a valid input 
			print "Character not in alphabet"	#print an error message if x is not recognized
			return 0
		
		t = 0
		while(t < len(self.T)):	#loop through and try to perform as many transitions as possible
			i = self.current[0]	#getting the current state of the pda
			#the following 4 sections all follow the same logic, the only execption being the existence of empty string inputs
			if([self.T[t]['cs'], self.T[t]['i'], self.T[t]['s']] == [i, x, top]):	#check if there is a matching transition
				if(self.T[t]['s'] == 'e'):	#put top back on the stack if nothing was actually read in form the stack
					self.my_stack.PUSH(top)
				self.my_stack.PUSH(self.T[t]['p'])	#push the specified element on to the stack

				#formatting the output string
				outputString = str(i) + '; ' + str(x) + '; ' + str(top) + '; ' + str(self.T[t]['ns']) + ';' + self.my_stack.PRINT()
				self.current = []	#updating the current state
				self.current.append(self.T[t]['ns'])

				t = 0	#start at the beginning of the transition list again
				x = 'e'	#we no longer need input x once a transition made with it is made
				top = self.my_stack.POP()	#getting the next element off the stack
				if(top == None):
					print "Empty stack"	#print this error message if the stack is somehow empty
					return 0
				print outputString
			elif([self.T[t]['cs'], self.T[t]['i'], self.T[t]['s']] == [i, x, 'e']):
				self.my_stack.PUSH(top)	
				self.my_stack.PUSH(self.T[t]['p'])

				outputString = str(i) + '; ' + str(x) + '; ' + 'e' + '; ' + str(self.T[t]['ns']) + ';' + self.my_stack.PRINT()

				self.current = []
				self.current.append(self.T[t]['ns'])

				t = 0
				x = 'e'
				top = self.my_stack.POP()
				if(top == None):
					print "Empty stack"
					return 0
				print outputString
			elif([self.T[t]['cs'], self.T[t]['i'], self.T[t]['s']] == [i, 'e', top]):
				if(self.T[t]['s'] == 'e'):
					self.my_stack.PUSH(top)
				self.my_stack.PUSH(self.T[t]['p'])

				outputString = str(i) + '; ' + 'e' + '; ' + str(top) + '; ' + str(self.T[t]['ns']) + ';' + self.my_stack.PRINT()

				self.current = []
				self.current.append(self.T[t]['ns'])

				t = 0
				x = 'e'
				top = self.my_stack.POP()
				if(top == None):
					print "Empty stack"
					return 0
				print outputString
			elif([self.T[t]['cs'], self.T[t]['i'], self.T[t]['s']] == [i, 'e', 'e']):
				self.my_stack.PUSH(top)	
				self.my_stack.PUSH(self.T[t]['p'])

				outputString = str(i) + '; ' + 'e' + '; ' + 'e' + '; ' + str(self.T[t]['ns']) + ';' + self.my_stack.PRINT()

				self.current = []
				self.current.append(self.T[t]['ns'])

				t = 0
				x = 'e'
				top = self.my_stack.POP()
				if(top == None):
					print "Empty stack"
					return 0
				print outputString
			else:
				t = t + 1
		self.my_stack.PUSH(top)	#put top back on the stack if no more transitions are to be made (prevents a double pop with the next input)
		return 1


	def is_det(self):	#defining is_det function
		#0 is initial, 1 is not reading from input or stack, 2 is only reading input, 3 is only reading stack, 4 is reading both
		for q in self.Q:	#go through every state in the pda
			state = 0	#state (referring to what inputs are being read from )
			inputs = []	#list containing inputs we have already encountered
			stack_inputs = []	#list containing stack inputs we have already encountered
			input_stack_combos = []	#list containing input and stack input combinations we have already encountered
			for t in self.T:	
				if(q == t['cs']):	#go through every transition out of the current state
					if((t['i'] == 'e') and (t['s'] == 'e')):	#transition input and stack input are both e	
						if(state == 0):
							state = 1	#set state to 1 if still in initial state
						else:	#encountered another transition where input and stack input are both e (not allowed in dpda)
							return 0	
					elif(t['s'] == 'e'):	#transition which only reads from input
						if(state == 0):	#set state to 2 and add inputs to their respective lists
							state = 2
							inputs.append(t['i'])
							input_stack_combos.append([t['i'], t['s']])
						elif(state == 1):	#this means there is already a transition of the form e, e --> x
							return 0
						elif(state == 3):	#this means that the dpda should only be reading from stack input
							return 0
						elif((state == 4) and (inputs.count(t['i'] > 0))): #this means there exists a more specific transition
							return 0
						elif(input_stack_combos.count([t['i'], t['s']]) > 0):	
							return 0	#this means that we are trying to push a different item on to the stack
						else:				#for the given input and stack input
							state = 2	
							input_stack_combos.append([t['i'], t['s']])
							inputs.append(t['i'])
					elif(t['i'] == 'e'):	#transition which only reads stack input
						if(state == 0):	#set state to 3 and add inputs to their respective lists
							state = 3
							stack_inputs.append(t['s'])
							input_stack_combos.append([t['i'], t['s']])
						elif(state == 1):	#this means there is already a transition of the form e, e --> x
							return 0
						elif(state == 2):	#this means that the dpda should only be reading from regular input
							return 0
						elif((state == 4) and (stack_inputs.count(t['s'] > 0))):#this means there exists a more specific transition
							return 0
						elif(input_stack_combos.count([t['i'], t['s']]) > 0): #trying to push a different item on to the stack for the same input and stack input
							return 0
						else:
							state = 3
							stack_inputs.append(t['s'])
							input_stack_combos.append([t['i'], t['s']])
					else:
						if(state == 0):	#set state to 4 and add inputs to their respective lists
							state = 4
							inputs.append(t['i'])
							stack_inputs.append(t['s'])
							input_stack_combos.append([t['i'], t['s']])
						elif(state == 1):	#this means there is already a transition of the form e, e --> x
							return 0
						elif((state == 2) and (inputs.count(t['i']) > 0)): #this means that there is a less specific transition
							return 0
						elif((state == 3) and (stack_inputs.count(t['s']) > 0)): #this means that there is a less specific transition
							return 0
						elif(input_stack_combos.count([t['i'], t['s']]) > 0):	#this means that we are trying to push a different item on to the stack for the same input and stack input
							return 0
						else:
							inputs.append(t['i'])
							stack_inputs.append(t['s'])
							input_stack_combos.append([t['i'], t['s']])
		return 1


	def accept(self):	#defining accept function
		for i in self.current:	#check if the current state is an accept state
			if(self.F.count(i) > 0):
				print "ACCEPT\n"	#print accept if current state is an accept state
				return 1
		print "REJECT\n"	
		return 1

	
	def reset(self):	#defining reset function
		self.current = []	#clearing current state and setting it to the start state
		self.current = self.S
		self.my_stack.CLEAR()	#clearing the stack

								

		
						
	
		
		
				
		
		
			
		
	
