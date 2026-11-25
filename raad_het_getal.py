import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from hardware import Rotary



page0 = None
lblGok = None
lblHint = None
rotary = None

import random

gok = None
geheim = None
pogingen = None


def setup():
  global page0, lblGok, lblHint, rotary, gok, geheim, pogingen

  M5.begin()
  Widgets.setRotation(0)
  m5ui.init()
  page0 = m5ui.M5Page(bg_c=0xffffff)
  lblGok = m5ui.M5Label("0", x=103, y=92, text_c=0x000000, bg_c=0xffffff, bg_opa=0, font=lv.font_montserrat_48, parent=page0)
  lblHint = m5ui.M5Label("Draai en druk", x=71, y=161, text_c=0x000000, bg_c=0xffffff, bg_opa=0, font=lv.font_montserrat_14, parent=page0)
    
  rotary = Rotary()
  geheim = random.randint(1, 50)
  pogingen = pogingen + 1
  page0.screen_load()
    

def loop():
  global page0, lblGok, lblHint, rotary, gok, geheim
  M5.update()
  gok = rotary.get_rotary_value()
  lblGok.set_text(str(gok))
  if BtnA.wasClicked():
    if gok < geheim:
      lblHint.set_text(str('Hoger!'))
    else:
      if gok > geheim:
        lblHint.set_text(str('Lager!'))
      else:
        lblHint.set_text(str('Geraden!'))
        Speaker.tone(2000, 600)
    


if __name__ == '__main__':
  try:
    setup()
    while True:
      loop()
  except (Exception, KeyboardInterrupt) as e:
    try:
      m5ui.deinit()
      from utility import print_error_msg
      print_error_msg(e)
    except ImportError:
      print("please update to latest firmware")
