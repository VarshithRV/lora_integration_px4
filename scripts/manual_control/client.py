# Client side
from multiprocessing.connection import Client

address = ('localhost', 6000)
conn = Client(address, authkey=b'secret password')
i=0
while i in range(100):
    conn.send(i)
    # print(conn.recv())
    i+=1
conn.send('close')
# can also send arbitrary objects:
# conn.send(['a', 2.5, None, int, sum])
conn.close()