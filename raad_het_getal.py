import os, sys, io
import random
import M5
from M5 import *
import m5ui
import lvgl as lv
from hardware import Rotary

page0 = None
lblGok = None
lblHint = None
rotary = None

gok = 1
vorige_gok = None
geheim = None
pogingen = 0
spel_klaar = False

def nieuw_spel():
  global geheim, pogingen, spel_klaar, vorige_gok
  geheim = random.randint(1, 50)
  pogingen = 0
  spel_klaar = False
  vorige_gok = None
  rotary.reset_rotary_value()
  lblHint.set_text("Draai (1-50) en druk")

def setup():
  global page0, lblGok, lblHint, rotary

  M5.begin()
  Widgets.setRotation(0)
  m5ui.init()
  page0 = m5ui.M5Page(bg_c=0xffffff)
  lblGok = m5ui.M5Label("1", x=103, y=92, text_c=0x000000, bg_c=0xffffff, bg_opa=0, font=lv.font_montserrat_48, parent=page0)
  lblHint = m5ui.M5Label("Draai (1-50) en druk", x=55, y=161, text_c=0x000000, bg_c=0xffffff, bg_opa=0, font=lv.font_montserrat_14, parent=page0)
    
  rotary = Rotary()
  nieuw_spel()
  page0.screen_load()

def loop():
  global gok, vorige_gok, pogingen, spel_klaar
  M5.update()
  
  # Begrens de draaiknop tussen 1 en 50
  ruwe_waarde = rotary.get_rotary_value() + 1
  gok = max(1, min(50, ruwe_waarde))
  
  # Alleen scherm updaten als het getal verandert
  if gok != vorige_gok:
    lblGok.set_text(str(gok))
    vorige_gok = gok

  if BtnA.wasClicked():
    if spel_klaar:
      nieuw_spel()
      return

    pogingen += 1
    if gok < geheim:
      lblHint.set_text(f"Hoger! (Poging {pogingen})")
      Speaker.tone(800, 100)
    elif gok > geheim:
      lblHint.set_text(f"Lager! (Poging {pogingen})")
      Speaker.tone(600, 100)
    else:
      lblHint.set_text(f"Geraden in {pogingen}x! Klik=nieuw")
      Speaker.tone(2000, 600)
      spel_klaar = True

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