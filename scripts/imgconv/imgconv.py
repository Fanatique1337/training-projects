#!/usr/bin/env python3

# Exit codes:
# 6:	Argparse Error. Probably a wrong argument, input type, or a spelling mistake.
# 7:	Global exception caught. Could be anything.

import argparse
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
							help="Converting mode: [1] to JPG | [2] to PNG | [3] to Grayscale",
							type=int,
							default=1)
		parser.add_argument("-w",
							"--overwrite",
							help="Overwrite the image given.",
							action="store_true",
							default=False)
		parser.add_argument("imgfile",
							help="Path to the image to be converted, defaults to all images.",
							type=str,
							default="*")
		parser.add_argument("-o",
							"--output",
							help="Output file name.",
							type=str,
							default="imgconv")
		args = parser.parse_args()

		return args.mode, args.overwrite, args.imgfile, args.output

	except argparse.ArgumentError:
		print("An error occured while parsing your arguments.", file=sys.stderr)
		sys.exit(ARGPARSE_ERR)

class imageconv():

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

def main():

	convert_mode, overwrite, imagefile, output = parse_arguments()

	imagefile = os.path.abspath(imagefile)

	if convert_mode == 1:
		image = imageconv.to_jpg(imagefile)
		
		if not overwrite:
			output = output + '.jpg' if '.jpg' not in output else output
		elif overwrite:
			output = imagefile

		image.save(output, 'JPEG', quality=95)

	elif convert_mode == 2:
		image = imageconv.to_png(imagefile)
		output = output + '.png' if '.png' not in output else output
		image.save(output, 'PNG')

	elif convert_mode == 3:
		image = imageconv.grayscale(imagefile)
		image.save(output)

	elif convert_mode == 4:
		image = imageconv.black_white(imagefile)
		output = output + '.bmp' if '.bmp' not in output else output
		image.save(output, "BMP")


if __name__ == "__main__":
	main()


