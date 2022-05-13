from .analyst import Analyst
import sqlite3
import datetime

def main():
  credential = input()

  def authenticateSelf():
    con = sqlite3.connect('<path/to/sqlite3/db>')
    cur = con.cursor()
    for row in cur.execute("SELECT * FROM credentials WHERE keyId = <your_stored_credential_key>"):
      if credential == row['secret']:
        #instantiating the analyst class
        peteru = Analyst(credentials=credential, indicators=[])

        #begin while loop
        while True:
          if datetime.datetime.hour == 0 and datetime.datetime.minute == 0:
            #calling the methods on the analyst class
            peteru.fetchdata()
            peteru.compute_MovingAverage()
            peteru.compute_CCI()
            peteru.compute_MarketPressure()
            peteru.plotChart()
      else:
        print('Unauthorized access! provide a valid password')