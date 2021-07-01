To install you need to install pyzmq and for subosc, also pyliblo

e.g.

```
pip install pyzmq pyliblo
```

You might need this library for pyliblo:
http://liblo.sourceforge.net/

Then run subosc.py and you should be able to do this sort of thing in
tidal

```
d1 $ sound "bd*8" # speed ("^sensor1"*8)

d2 $ sound "sd(5,8)" # speed ("^sensor2"*8)

d3 $ slow ("^sensor3") $ sound "gabor*8"
```
