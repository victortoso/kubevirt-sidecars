#!/usr/bin/python3

import xml.etree.ElementTree as ET
import sys

WIDTH=2040
HEIGHT=1180

def add_resolution(video):
	resolution = ET.fromstring(f"<resolution x='{WIDTH}' y='{HEIGHT}'/>")
	model = video.find("model")
	if model.find("resolution") is not None:
		# Already has it.
		# Hook APIs might be called more than once.
		return

	model.insert(0, resolution)
	if model.find("resolution") is None:
		sys.stderr.write("Failed to add fixed resolution")
	else:
		sys.stderr.write("Fixed resolution added")

def fixed_resolution(domainxml):
	root = ET.fromstring(domainxml)
	devices = root.find("devices")
	for video in devices.findall("video"):
		add_resolution(video)
	ET.dump(root)

if __name__ == "__main__":
	fixed_resolution(sys.argv[4])
