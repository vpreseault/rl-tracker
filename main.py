from Session import Session
from Store import Store

store = Store(gamemode="doubles")
s = Session(store.getCurrentMmr())
sessionResult = s.loop()
if sessionResult != False:
    store.addSession(sessionResult)
