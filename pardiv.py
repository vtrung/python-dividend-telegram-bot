from sys import argv
from bs4 import BeautifulSoup
import requests
import threading


class stock:
  symbol = ""
  company = ""
  div = ""
  exd = ""
  payd = ""
  annualrate = ""
  annualdiv = ""
  price = ""

  def __init__(self, symbol):
    self.symbol = symbol

  # request dividend data from nasdaq.com
  def get(self):
    url = "https://dividata.com/stock/" + self.symbol
    print(url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    

    small = soup.find_all(class_="small")
    if len(small) > 0:
      self.company = self.getcontent(small[0])
    
    bigstat = soup.find_all(class_="bigstat")
    if len(bigstat) > 0:
      self.price = self.getcontent(bigstat[0])
      self.payd = self.getcontent(bigstat[1])
      self.exd = self.getcontent(bigstat[2])
      self.annualdiv = self.getcontent(bigstat[3])
      self.annualrate = self.getcontent(bigstat[4])
      self.div = self.getcontent(bigstat[5])
    
    #self.exd = self.getcontent(soup.select("#quotes_content_left_dividendhistoryGrid_exdate_0"))
    #self.div = self.getcontent(soup.select("#quotes_content_left_dividendhistoryGrid_CashAmount_0"))
    #self.payd = self.getcontent(soup.select("#quotes_content_left_dividendhistoryGrid_PayDate_0"))

  def getcontent(self, tag):
    #print(tag)
    for t in tag:
      return t.string


  def getinfo(self):
    if self.exd:
      info = "Symbol: " + self.symbol + "\n"
      info += "Name: " + self.company + "\n"
      #info += "Price: " + self.price + "\n"
      info += "Ex-dividend Data: " + self.exd + "\n"
      info += "Payment Date: " + self.payd + "\n"
      info += "Dividend: " + self.div + "\n"
      info += "Annual Yield: " + self.annualrate + "\n"
      info += "Annual Dividend: " + self.annualdiv + "\n"
      return info
    else:
      return self.symbol + " Not Found"

  def print(self):
    print("Symbol:", self.symbol)
    print("Ex-dividend Date:", self.exd)
    print("Payment Date:", self.payd)
    print("Dividend: $", self.div, sep='')

class reqthread(threading.Thread):
  def __init__(self,symbol):
        threading.Thread.__init__(self)
        self.symbol = symbol
  def run(self):
        self.stock = stock(self.symbol)
        self.stock.get()
  def getstock(self):
        return self.stock


if __name__ == "__main__":
  if len(argv) > 1:
                # multi define if program will run in parallel or sequentially
                multi = False;
                symbols = argv[1:]
                threads = []
                for symbol in symbols:
                    if symbol[0] == '-':
                        if symbol == "-m":
                            multi = True
                        continue
                    th = reqthread(symbol)
                    threads.append(th)
                
                # start threads: if multi is true, run parallel. if false, run sequentially
                for t in threads:
                    t.start()
                    if not multi:
                        t.join()

                if multi:
                    for t in threads:
                        t.join()
                
                for t in threads:
                    stock = t.getstock()
                    stock.print()
                    print("===========")


  else:
                print("No arguments found")
                print("Please pass in any number of stock symbol you wish to lookup")
                print("Example: python3 pardiv.py IBM AAPL GE")

