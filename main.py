from Session import Session
from Store import Store

store = Store()
s = Session(store.getCurrentMmr())
sessionResult = s.loop()
store.addSession(sessionResult)
