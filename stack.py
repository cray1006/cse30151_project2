#! /usr/bin/python -tt

#Christopher Ray
#Professor Blanton
#CSE 30151
#24 March 2015

#stack.py
#declaration and implementation of stack class for use in a DPDA

class stack(object):	#defining stack class
	def __init__(self):	#defining __init__ function
		self.myStack = []	#stack is really just a list, with the "top" being the last element of the list

	
	def POP(self):	#defining POP fucntion
		if(len(self.myStack) == 0):	#return None if the stack is empty
			return None
		elif(self.myStack[len(self.myStack) - 1] == '$'):	#return the end of stack character (but do not remove it from the stack)
			return '$'
		else:
			return self.myStack.pop()	#return and pop the top the stack

	
	def PUSH(self, x):	#defining the PUSH function
		if(x != 'e'):	#this prevents pushing empty string on to stack
			if((x == '$') and not('$' in self.myStack)):	#add the end of stack character to the stack if it is not there already
				self.myStack.append(x)
			elif(x != '$'):
				self.myStack.append(x)	#add x to the stack

	
	def CLEAR(self):	#defining CLEAR function
		self.myStack = []

	
	def PRINT(self):	#defining PRINT function
		i = len(self.myStack) - 1
		outputString = ' '
		while(i >= 0):	#iterate (in reverse) through the list underlying the stack and print its elements
			#formatting the output string
			if(self.myStack[i] == '$'):
				outputString = outputString + str(self.myStack[i])
			else:
				outputString = outputString + str(self.myStack[i]) + ','
			i = i - 1
		return outputString
			
				
