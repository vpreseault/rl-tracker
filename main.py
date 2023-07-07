from Session import Session
from Store import Store

store = Store()
s = Session(store, store.getCurrentMmr())
s.loop()
