#!/usr/bin/env python3

# Exit codes:
# 6:	Argparse Error. Probably a wrong argument, input type, or a spelling mistake.
# 7:	Global exception caught. Could be anything.

import argparse
import glob
import os
import sys

from PIL import Image as img
import numpy as np

# Error constants

ARGPARSE_ERR = 6
GLOBAL_ERR = 7

def parse_arguments():
	"""Get arguments for use case"""

	try:
		parser = argparse.ArgumentParser(description="Python Image Converter")
		parser.add_argument("-m",
							"--mode",
							help="1: jpg, 2: png, 3: grayscale, 4: black_white, 5: resize",
							type=int,
							default=1)
		parser.add_argument("-w",
							"--overwrite",
							help="Overwrite the image given.",
							action="store_true",
							default=False)
		parser.add_argument("imgfile",
							help="Path to the image to be converted.",
							type=str)
		parser.add_argument("-o",
							"--output",
							help="Output file name.",
							type=str,
							default="imgconv")
		parser.add_argument("-r",
							"--resize",
							help="Resize to a new X Y size (-r X Y)",
							type=int,
							nargs="+")
		parser.add_argument("-s",
							"--show",
							help="Show the image after processing it.",
							action="store_true",
							default=False)
		args = parser.parse_args()

		return (args.mode, args.overwrite, args.imgfile,
				args.output, args.resize, args.show)

	except argparse.ArgumentError:
		print("An error occured while parsing your arguments.", file=sys.stderr)
		sys.exit(ARGPARSE_ERR)

class imageconv():
	"""The image converter class."""

	def to_png(imagefile):
		"""Convert the image to png format."""

		image = img.open(imagefile)
		image = image.convert('RGBA')

		return image

	def to_jpg(imagefile):
		"""Convert the image to jpg format."""

		image = img.open(imagefile)
		image = image.convert('RGB')

		return image

	def grayscale(imagefile):
		"""Convert image to grayscale format."""

		image = img.open(imagefile)
		image = image.convert('L')

		return image

	def black_white(imagefile):
		"""Convert colors to black & white bitmap."""

		image = img.open(imagefile)
		imgarray = np.array(image)

		red, green, blue = np.split(imgarray, 3, axis=2)
		red = red.reshape(-1)
		green = green.reshape(-1)
		blue = blue.reshape(-1)

		bitmap = list(map(lambda x: 0.299*x[0] + 0.587*x[1] + 0.114*x[2], zip(red, green, blue)))
		bitmap = np.array(bitmap).reshape([imgarray.shape[0], imgarray.shape[1]])
		bitmap = np.dot((bitmap >128).astype(float), 255)

		image = img.fromarray(bitmap.astype(np.uint8))

		return image

	def size_to(imagefile, new_size):
		"""Resize the image."""

		image = img.open(imagefile)
		image = image.resize(tuple(new_size), img.LANCZOS)

		return image

def main():

	convert_mode, overwrite, imagefile, output, req_size, show = parse_arguments()

	imagepath = os.path.abspath(imagefile)

	if convert_mode == 1:
		image = imageconv.to_jpg(imagepath)
		
		if not overwrite:
			output = output + '.jpg' if not output.endswith('.jpg') else output
		elif overwrite:
			output = imagepath

		image.save(output, 'JPEG', quality=95)

	elif convert_mode == 2:
		image = imageconv.to_png(imagepath)

		if not overwrite:
			output = output + '.png' if not output.endswith('.png') else output
		elif overwrite:
			output = imagepath

		image.save(output, 'PNG')

	elif convert_mode == 3:
		image = imageconv.grayscale(imagepath)

		if overwrite:
			output = imagepath

		image.save(output)

	elif convert_mode == 4:
		image = imageconv.black_white(imagepath)

		if not overwrite:
			output = output + '.bmp' if not output.endswith('.bmp') else output
		elif overwrite:
			output = imagepath

		image.save(output, "BMP")

	if convert_mode == 5:
		image = imageconv.size_to(imagepath, req_size)

		if overwrite:
			output = imagepath

		image.save(output)

	if show:
		image.show()


if __name__ == "__main__":
	main()


