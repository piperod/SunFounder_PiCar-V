#!/usr/bin/env python
'''
**********************************************************************
* Filename    : stream.py
* Description : A streamer module base on mjpg_streamer
* Author      : xxx
* Brand       : SunFounder
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Update      : xxx    xxxx-xx-xx    New release
*               xxx    xxxx-xx-xx    xxxxxxxx
**********************************************************************
'''
import tempfile
import subprocess
import os
import glob

_CODE_DIR_ = "/home/pi/SunFounder_PiCar-V"

MJPG_STREAMER_PATH = "mjpg_streamer"
INPUT_PATH = "/usr/local/lib/input_uvc.so"
VIDEO_PATH = "videos/"

try: 
  os.makedirs(VIDEO_PATH)
except:
  print('Folder Already Exists')
  
SAVE_PATH = "/usr/local/lib/output_file.so -f " + VIDEO_PATH +" -d 1"
OUTPUT_PATH = "/usr/local/lib/output_http.so -w /usr/local/www "

stream_cmd = '%s -i "%s" -o "%s" -o "%s" &' % (MJPG_STREAMER_PATH, INPUT_PATH, OUTPUT_PATH,SAVE_PATH)

def run_command(cmd):
	with tempfile.TemporaryFile() as f:
		subprocess.call(cmd, shell=True, stdout=f, stderr=f)
		f.seek(0)
		output = f.read()
	return output

def start():
	files = os.listdir('/dev')
	if 'video0' in files:
		run_command(stream_cmd)
	else:
		raise IOError("Camera is not connected correctly")

def get_host():
	return run_command('hostname -I')

def stop():
	pid = run_command('ps -A | grep mjpg_streamer | grep -v "grep" | head -n 1')
	if pid == '':
		return False
	else:
		run_command('sudo kill %s' % pid)
		return True

def restart():
	stop()
	start()
	return True

def test():
	run_command(stream_cmd[:-2])

if __name__ == "__main__":
	test()
