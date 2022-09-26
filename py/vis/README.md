

To get this working locally with random data:

1. Install dependencies like:

> pip3 install -r requirements.txt

2. Run the zmq proxy in ../../zmq/proxy.py

3. Run the `randtest.py` in this folder to stream the random data

4. Run `vis.py` here. 

You should now see the data appear in a cycle, with the sequence sent to tidal as 'facep', e.g. this should work:

```haskell
d1 $ speed (range 0.1 5 (cP "facep") ) # s "bd"
```

With Tidal 1.9+, it should be in sync via the link protocol

To work with the zmq proxy running on the raspberry pi, assuming it's on ip 192.168.0.10, change

`subscriberSocket.connect('tcp://127.0.0.1:5555')`

to

`subscriberSocket.connect('tcp://192.168.0.10:5555')`

To work with a different data source, change `key = 'rand'` to 'carpet3' or whatever

