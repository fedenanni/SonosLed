#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.

import re
import time
import argparse

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT


import requests
from time import sleep

def check_status():
        r = requests.get('http://localhost:5005/living%20room/state')
        response = r.json()
        status = response["playbackState"]
        if "PLAYING" in status:
            return response
        else:
            return False

        
def check_song(response):
        r = requests.get('http://localhost:5005/living%20room/state')
        response = r.json()
        try:
                playing = response["currentTrack"]["title"]
                artist = response["currentTrack"]["artist"]
                album = response["currentTrack"]["album"]
        
                return playing, artist
        except Exception as e:
                playing = response["currentTrack"]["title"]                
                return playing, playing
def check_year(song,artist):
        query = song + " " + artist

        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer BQDQj48VrPU--m_XTyXUAl5R6TmjlTbfqPQThVYSJKHEK9B6jb03cgj0QnIyp-U-BHRzVMBZijIzmMAPpsNgrpKnl5ZCX4wd9bnCUIy73DLndAIVKKZcp-gQpjrJYc6o-ndi5rzxVRLefdJ5m8RnL03PChAS',
        }

        params = (
            ('q', query),
            ('type', 'track'),
            ('limit', '1'),
        )

        response = requests.get('https://api.spotify.com/v1/search', headers=headers, params=params)
        response = response.json()
        id_album = response["tracks"]["items"][0]["album"]["id"]

        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer BQDQj48VrPU--m_XTyXUAl5R6TmjlTbfqPQThVYSJKHEK9B6jb03cgj0QnIyp-U-BHRzVMBZijIzmMAPpsNgrpKnl5ZCX4wd9bnCUIy73DLndAIVKKZcp-gQpjrJYc6o-ndi5rzxVRLefdJ5m8RnL03PChAS',
        }

        rs = requests.get('https://api.spotify.com/v1/albums/'+id_album, headers=headers)
        rs = rs.json()
        year = rs["release_date"].split("-")[0]
        return year

def demo(n, block_orientation, rotate):
        while True:
            # create matrix device
            serial = spi(port=0, device=0, gpio=noop())
            device = max7219(serial, cascaded=n or 1, block_orientation=block_orientation, rotate=rotate or 0)
            try:
                    res = check_status()
                    prev_artist = ""
                    year = "dont-know"
                    if res != False:
                        song,artist = check_song(res)
                        #if artist != prev_artist:
                                
                         #       year = check_year(song,artist)
                        
                        

                        
                        msg = song + " - " + artist 
                        
                        #msg = re.sub(" +", " ", msg)
                        show_message(device, msg, fill="white", font=proportional(LCD_FONT))
                        #text(device, (0, 0), chr(14), fill="white")
                        time.sleep(1)
                    else:
                        time.sleep(5)
            except Exception as e:
                    print (e)
                    time.sleep(5)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='matrix_demo arguments',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--cascaded', '-n', type=int, default=1, help='Number of cascaded MAX7219 LED matrices')
    parser.add_argument('--block-orientation', type=int, default=0, choices=[0, 90, -90], help='Corrects block orientation when wired vertically')
    parser.add_argument('--rotate', type=int, default=0, choices=[0, 1, 2, 3], help='Rotate display 0=0°, 1=90°, 2=180°, 3=270°')

    args = parser.parse_args()

    try:
        demo(args.cascaded, args.block_orientation, args.rotate)
    except KeyboardInterrupt:
        pass
