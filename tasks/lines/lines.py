#!/usr/bin/env python3
import sys
import kivy
import time
from kivy.app import App
from kivy.uix.widget import Widget 
from kivy.graphics import Color, Line

inp = input("").split(" ")
length = int(inp[0])
a = int(inp[1])
b = int(inp[2])
c = int(inp[3])
mx = 100000

if length > mx or a > mx or b > mx or c > mx:
	print("All numbers must be lower than 100 000.")
	sys.exit(3)

counter_a = 0
counter_b = length
dots_a = []
dots_b = []
total = 0
colored = []
segments = {}

while(counter_a <= length):
	dots_a.append(counter_a)
	counter_a += a

while(counter_b >= 0):
	dots_b.append(counter_b)
	counter_b -= b

for dota in dots_a:
	for dotb in dots_b:
		tmp = max(dota, dotb)
		tmp2 = min(dota, dotb)
		if tmp - tmp2 == c:
			if tmp not in colored:
				colored.append(tmp)
			if tmp2 not in colored:
				colored.append(tmp2)
			total += c

colored.sort()



print(length-total)
print(dots_a)
print(dots_b)
print(colored)

class VisualizeLines(App):
	def build(self):
		return VisualWidget()

class VisualWidget(Widget):
	def __init__(self, **kwargs):
		super(VisualWidget, self).__init__(**kwargs)
		with self.canvas:
			Color(2, 3, 1, 1, mode="rgba")
			Line(points=(40, 40, 120, 40))

VisualizeLines().run()