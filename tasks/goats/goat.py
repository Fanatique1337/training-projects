#!/usr/bin/env python
import itertools
from PIL import Image, ImageDraw, ImageFont

def main():
	goatnum = 0
	courses = 0
	goatw = []
	counter = 0

	goatnum = int(input("Enter the number of goats: "))
	courses = int(input("Enter the number of courses: "))
	for g in range(goatnum):
		goatw.append(int(input("Enter the weight of goat #{}: ".format(g+1))))

	goatw = sorted(goatw, reverse=True)
	goats = sum(goatw)
	result = []
	permlen = goatnum/courses
	print(permlen, courses, goatnum)
	while not result:
		result = [seq for i in range(goatnum) for seq in itertools.permutations(goatw, permlen) if sum(seq) == int(goats/courses)]
		if not result:
			goats += 1
			#permlen += 1
		else:
			break

	print(result)

	fig = goats/courses
	used_numbers = []
	result_courses = []
	

	for res in result:
		if len(result_courses) < courses and res not in result_courses:
			res_sum = 0
			tmp_numbers = []
			for number in res:
				if tmp_numbers.count(number) < goatw.count(number) and used_numbers.count(number) < goatw.count(number):
					res_sum += number
					tmp_numbers.append(number)
			if res_sum == fig:
				used_numbers.extend(list(res))
				result_courses.append(res)

	print(used_numbers)
	print(result_courses)

	delim = goatnum/courses

	images = []

	counter = 1
	for crs in result_courses:
		images.append(visualize(crs, counter))
		combine(images)
		counter += 1

def visualize(course, i):

	white = (255, 255, 255)

	fnt_20 = ImageFont.truetype('DejaVuSansMono.ttf', size=20)
	fnt_30 = ImageFont.truetype('DejaVuSansMono.ttf', size=30)
	fnt_40 = ImageFont.truetype('DejaVuSansMono.ttf', size=40)
	fnt_50 = ImageFont.truetype('DejaVuSansMono.ttf', size=50)

	image = Image.new('RGB', (400, 400), (42, 178, 47))
	drawing = ImageDraw.Draw(image)
	drawing.rectangle(xy=[0, 150, 400, 250], fill=(49, 190, 180)) # river
	drawing.rectangle(xy=[175, 175, 225, 225], fill=(76, 53, 0)) # raft
	drawing.text((190, 190), str(sum(course)), font=fnt_20, fill=white) # raft weight
	drawing.text((110, 20), "COURSE {}".format(i), font=fnt_40, fill=white) # course
	drawing.text((157, 270), "Goats", font=fnt_30, fill=white)
	pos_x = 20
	pos_y = 320
	for weight in course:
		pos = (pos_x, pos_y)
		drawing.rectangle(xy=[pos_x, pos_y, pos_x+20, pos_y+20], fill=white, outline=(0,0,0)) # goat
		drawing.text((pos_x+2, pos_y+2), str(weight), fill=(0,0,0,0))
		if pos_x + 40 < 400:
			pos_x += 40
		else:
			pos_x = 20
			pos_y += 40

	return image

def combine(images):

	imageg = Image.new('RGB', (400, 400*len(images)), (0, 0, 0))
	paste_x = 0
	paste_y = 0
	for img in images:
		imageg.paste(img, box=(paste_x, paste_y))
		paste_y += 400

	#imageg.show()
	imageg.save('courses.png')

main()