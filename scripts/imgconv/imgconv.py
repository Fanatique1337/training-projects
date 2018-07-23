#!/usr/bin/env python3

# Exit codes:
# 6:	Argparse Error. Probably a wrong argument, input type, or a spelling mistake.
# 7:	Global exception caught. Could be anything.

import argparse
import os
import sys

from PIL import Image as img

# Error constants

ARGPARSE_ERR = 6
GLOBAL_ERR = 7

def parse_arguments():
	"""Get arguments for use case"""

	try:
		parser = argparse.ArgumentParser(description="Python Image Converter")
		parser.add_argument("-m",
							"--mode",
							help="Converting mode: [1 = png to jpg] | [2 = jpg to png].",
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

	def jpg_to_png(imagefile):
		"""Convert the image from jpg to png format."""

		image = img.open(imagefile)
		image = image.convert('RGBA')

		return image

	def png_to_jpg(imagefile):
		"""Convert the image from png to jpg format."""

		image = img.open(imagefile)
		image = image.convert('RGB')

		return image


def main():
	convert_mode, overwrite, imagefile, output = parse_arguments()
	imagefile = os.path.abspath(imagefile)
	if convert_mode == 1:
		image = imageconv.png_to_jpg(imagefile)
		output = output + '.jpg' if '.jpg' not in output else output
		image.save(output, quality=95)
	elif convert_mode == 2:
		image = imageconv.jpg_to_png(imagefile)
		output = output + '.png' if '.png' not in output else output
		image.save(output)

main()


