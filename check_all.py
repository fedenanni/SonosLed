import subprocess
import time
while True:
	try:
		subprocess.call("npm restart & python2 ../luma.led_matrix/examples/fede-giu.py --cascaded 4 --block-orientation -90", shell=True)
	except: #catch everything else
		print ("ups")
		conitnue
	finally:
		time.sleep(60) 
