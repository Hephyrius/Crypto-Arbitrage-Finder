# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 11:35:31 2018

@author: Khera
"""
import time
import requests
import json

def coinfalcon():
    data = requests.get('https://coinfalcon.com/api/v1/markets/#/orders').json()['data']
    newFormat = []
    for i in data:
        try:
            time.sleep(1.1)
            market = i['name']
            link = 'https://coinfalcon.com/api/v1/markets/'+market+'/orders'
            #print(link)
            data2 = requests.get(link).json()['data']
            
            j = {'Exchange':'CoinFalcon', 'Market':i['name'], 'Ask':float(data2['asks'][0]['price']),'Bid':float(data2['bids'][0]['price'])}
            newFormat.append(j)
        except Exception as e:
            print(e)
                                        
    return newFormat

def cryptopia():
    
    data = requests.get('https://www.cryptopia.co.nz/api/GetMarkets').json()['Data']
    currencyData = requests.get('https://www.cryptopia.co.nz/api/GetCurrencies').json()['Data']
    for i in data:
        i['Label'] = i['Label'].replace('/', '-')
        
    newFormat = []
    for i in data:
        currencies = i['Label'].split("-")
        available1 = False
        available2 = False
        
        for l in currencyData:
            if l['Symbol'] in currencies[0]:
                if l['Status'] == 'OK' and l['ListingStatus'] == 'Active':
                    available1 = True
                else:
                    available1 = False
                    
            if l['Symbol'] in currencies[1] and currencies[1] != 'DOGE' and currencies[1] != 'LTC':
                if l['Status'] == 'OK'and l['ListingStatus'] == 'Active':
                    available2 = True
                else:
                    available2 = False
                        
        if available1 == True and available2 == True:
            j = {'Exchange':'Cryptopia', 'Market':i['Label'], 'Ask':float(i['AskPrice']),'Bid':float(i['BidPrice'])}
            newFormat.append(j)
    
    return newFormat

def gateio():
    data = requests.get('http://data.gate.io/api2/1/tickers').json()
    newFormat = []
    
    for i in data:
        market = i
        market2 = market.upper().replace("_", "-")
        j = {'Exchange':'Gate.io', 'Market':market2.upper(), 'Ask':float(data[i]['lowestAsk']),'Bid':float(data[i]['highestBid'])}
        newFormat.append(j)
        
    return newFormat
    
def tradeSatoshi():
    
    data = requests.get('https://tradesatoshi.com/api/public/getmarketsummaries').json()['result']
    currencyData = requests.get('https://tradesatoshi.com/api/public/getcurrencies').json()['result']
    
    for i in currencyData:
        i['currency'] = i['currency'].replace('$','')
    
    
    for i in data:
        i['market'] = i['market'].replace("_","-")
    
    newFormat = []
    for i in data:
        currencies = i['market'].split("-")
        available1 = False
        available2 = False
        
        for l in currencyData:
            if l['currency'] in currencies[0]:
                if l['status'] == 'OK':
                    available1 = True
                else:
                    available1 = False
                    
            if l['currency'] in currencies[1]:
                if l['status'] == 'OK':
                    available2 = True
                else:
                    available2 = False
                        
        if available1 == True and available2 == True:
            j = {'Exchange':'TradeSatoshi','Market':i['market'], 'Ask':float(i['ask']),'Bid':float(i['bid'])}
            newFormat.append(j)
        
    
    return newFormat

def Kucoin():
    currencyData = requests.get('https://api.kucoin.com/v1/market/open/coins').json()['data']
    data = requests.get('https://api.kucoin.com/v1/open/tick').json()['data']
    
    
    
    newFormat = []
    for i in data:
        
        available1 = False
        available2 = False
        
        market = i['symbol'].split('-')
        for k in currencyData:
            if k['coin'] in market[0]:
                if k['enableDeposit'] == True and k['enableWithdraw'] == True:
                    available1 = True
                else:
                    available1 = False
                    
            if k['coin'] in market[1]:
                if k['enableDeposit'] == True and k['enableWithdraw'] == True:
                    available2 = True
                else:
                    available2 = False
                    
        if available1 == True and available2 == True:
            try:
                j = {'Exchange':'KuCoin', 'Market':i['symbol'], 'Ask':float(i['sell']),'Bid':float(i['buy'])}
                newFormat.append(j)
            except Exception as e:
                print(e)
        
    
    return newFormat

def coinexchange():
    data = requests.get('https://www.coinexchange.io/api/v1/getmarketsummaries').json()['result']
    data2 = requests.get('https://www.coinexchange.io/api/v1/getmarkets').json()['result']
    currencyData = requests.get('https://www.coinexchange.io/api/v1/getcurrencies').json()['result']
    
    newFormat = []
    
    for i in data:
        found = False
        
        for j in data2:
            if found == False:
                if j['MarketID'] == i['MarketID']:
                    Market = j['MarketAssetCode'] + "-" + j['BaseCurrencyCode']
                    found = True
        
        currencies = Market.split("-")
        available1 = False
        available2 = False
        currencyName = ""
        for l in currencyData:
            if l['TickerCode'] in currencies[0]:
                currencyName = l['Name'].lower()
                currencyName =currencyName.replace(" ", "")
                if l['WalletStatus'] == 'online':
                    available1 = True
                else:
                    available1 = False
                    
            if l['TickerCode'] in currencies[1]:
                if l['WalletStatus'] == 'online':
                    available2 = True
                else:
                        available2 = False
            
        
        if available1 == True and available2 == True:
        
            j = {'Exchange':'coinexchange', 'Market':Market, 'Ask':float(i['AskPrice']),'Bid':float(i['BidPrice']), 'CurrencyName':currencyName}
            newFormat.append(j)
    
    return newFormat


def findArbitage():
    
    data = [tradeSatoshi(),coinfalcon(),cryptopia(),coinexchange(),Kucoin(),gateio()]
    
    for i in data:
        for j in i:
            for k in data:
                for l in k: 
                    
                    if l['Exchange'] != j['Exchange']:
                        if l['Market'] == j['Market']:
                            
                            Exchange1Bid = j['Bid']
                            Exchange2Bid = l['Bid']
                            Exchange1Ask = j['Ask']
                            Exchange2Ask = l['Ask']
                            if Exchange1Bid>0 and Exchange2Bid>0 and Exchange1Ask>0 and Exchange2Ask>0:
                                Ex1To2 = Exchange2Bid/Exchange1Ask
                                
                                if Ex1To2 > 1 and Ex1To2 < 2:
                                    percentage1 = (Ex1To2-1)*100
                                    print(j['Exchange'] + " to " + l['Exchange'] + " with marker " + j['Market'] + " has profits of " + str(percentage1) + "%")

findArbitage()



