# walk-kivy
# 

### animation and touch control testing
### python3 for android

## to do:
### - animate hat by giving position and angle instructions from a generator insise the 'Man' class (take these instructions but only implement if hat'inhand' is True)
### - game over action and page with return to menu or restart options
### - win game page with return to menu and score screen
### - add flames and animation to 'Fire' class


## double tap time in kivy config file
idefault is 250, changed to 300

python -m kivy.atlas fire 500x500 src/fire/fire-0*
python -m kivy.atlas man 1100x405 src/man/man*
python -m kivy.atlas background 1602x1926 src/background/*.png

#print(' - interval is', touch.double tap time)
