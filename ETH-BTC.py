#!/usr/bin/python
# -*- coding: latin-1 -*-

import gdax
import json,time
import math

class bcolors:
    HEADER = '\033[95m'
    OPEN = '\033[94m'
    BUY = '\033[92m'
    SELL = '\033[95m'
    CLOSED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

####API KEY####
key=' your key'
b64secret='your secret'
passphrase=' your passphrase'
#################

producto='ETH-BTC'

total_compras=0
total_ventas=0
ordenes_abiertas=0

last_buy_id="none"
last_sell_id="none"
indicador=0
indicador_compras=1
indicador_ventas=1
ganancia=0


def get_current_price():
    auth_client = gdax.AuthenticatedClient(key, b64secret, passphrase)
    result = auth_client.get_product_ticker(product_id=producto)
    if 'price' in result:
        print (result)
        return (float(result['price']))
    else:
       response= get_current_price()
       return response

def get_current_balance():
    auth_client = gdax.AuthenticatedClient(key, b64secret, passphrase)
    return (auth_client.get_accounts())

def get_order_list():
    auth_client = gdax.AuthenticatedClient(key, b64secret, passphrase)
    response=auth_client.get_orders()
    try:
        #json.loads(response[0])
        print (response) #comprobamos si puede decodificarlo como json
    except ValueError, e:               #Si no puede lanzará un error y
        resp=auth_client.get_orders() #volvemos a invocar a la función.
        return resp                   #y devolvemos la respuesta
    return response                     #si pudo decodificarlo lo devolvemos tal cual.

def compra(precio,cantidad):
    auth_client = gdax.AuthenticatedClient(key, b64secret, passphrase)
    r=auth_client.buy(price=precio,size=cantidad,product_id=producto)
    if 'message' in r:
        print (r['message'])
        return None
    else:
        return r

def vende(precio,cantidad):
    auth_client = gdax.AuthenticatedClient(key, b64secret, passphrase)
    r=auth_client.sell(price=precio,size=cantidad,product_id=producto)
    if 'message' in r:
        print (r['message'])
        return None
    else:
        return r
    #print r['id']


def cancela_orden( orden_id):
    auth_client = gdax.AuthenticatedClient(key, b64secret, passphrase)
    print(auth_client.cancel_order( orden_id))


def cancela_todo():
    resultado= get_order_list()
    for x in resultado:
            for y in x:
                t = y
                cancela_orden(t["id"])

def ver_fills():
    auth_client = gdax.AuthenticatedClient(key, b64secret, passphrase)
    response=auth_client.get_fills()
    return response


def get_last_fill(total_ventas, total_compras):#hace falta pasar variables total ventas
    auth_client = gdax.AuthenticatedClient(key, b64secret, passphrase)
    response=auth_client.get_fills()

    for x in response:
            for y in x:
                t = y
                if(t["order_id"] == last_sell_id ):
                     print(bcolors.CLOSED+"Se ejecuta la orden de venta"+bcolors.ENDC )
                     total_operacion_venta=float(t["price"])* float(t["size"])
                     print ("Total operacion venta: "+ str(total_operacion_venta))
                     total_ventas=total_ventas+total_operacion_venta
                     ########REVISAR ESTE indicador_ventas=indicador_ventas+1    UnboundLocalError: local variable 'indicador_ventas' referenced before assignment
                     return 1   #Valor de indicador

                    #ponemos el indicador para que indique que se realizo una venta..
                elif (t["order_id"] == last_buy_id ):
                    print(bcolors.CLOSED+"Se ejecuta la orden de compra"+bcolors.ENDC )
                    total_operacion_compra=float(t["price"])*float(t["size"])
                    print ("Total operacion compra: "+ str(total_operacion_compra))
                    total_compras=total_compras+total_operacion_compra
                    #########REVISAR ESTE indicador_compras=indicador_compras+1
                    return -1

                #if ((t["order_id"])==):

actual_price = get_current_price()
last_sell_price = actual_price
last_sell_price_media = actual_price
last_buy_price = actual_price
last_buy_price_media = actual_price
target_price_sell=actual_price
target_price_buy=actual_price

#cancela_todo()

#time.sleep (4)
#vende(actual_price+0.003,0.01)
#time.sleep (4)
#compra(actual_price-0.003,0.01)
#crear 10 slots y comprobar el estado y el numero de ordenes todo el tiempo....


while True:
    now = time.strftime("%c")
    ## Display current date and time from now variable
    print ("Current time %s"  % now )

    print ("total_ventas  :"+str(total_ventas))
    print ("total_compras :"+str(total_compras))

    print("Indicador: "+str(indicador))
    print ("Precio medio compra: "+str(last_buy_price_media) +" last_buy_id:  "+last_buy_id)
    print ("Precio medio venta : "+str(last_sell_price_media)+" last_sell_id: "+last_sell_id)
    #Calcular algo para ponderar la compra o la venta.
    print ("Ordenes abiertas: "+str(ordenes_abiertas))

    ###############
    actual_price=get_current_price()
    if (ordenes_abiertas == 0):
        cancela_todo()
        time.sleep (1)
        #last_sell_price_media=(last_sell_price_media+actual_price)/2
        #actual_price=get_current_price()

        #target_price_sell= round (actual_price+0.9,3)




        #la idea es implementar un sistema que siempre compre o venda en y fijar los precios de venta en funcion de la media de las compras más tanto% para obtener siempre beneficio.
        #

        #
        # Si baja compro.
        # Si sigue bajando.. compro más tarde (indicador de compras..incremental en función de la bajada)
        # Si el precio objetivo de venta > la media de las compras  entonces compro.
        #
        #
        #
        #


        #Fijamos los valores de compra y venta.
        target_price_sell= round (last_buy_price_media+0.0003,5)
        target_price_buy= round (actual_price-0.0003,5)

        if ((target_price_sell ) >= (actual_price ) ): #+spread
            #sellresult = vende(target_price_sell,0.01*indicador_ventas)   #Si llego aqui se vende
            sellresult = vende(target_price_sell,0.1)



            if (sellresult != None):
                last_sell_id = sellresult["id"]
                time.sleep (1)
        else:
                print("No se cumple la condicion incrementamos el precio de venta")
                target_price_sell= target_price_sell+0.0002

        if (( actual_price)  >= (target_price_buy)):
            #buyresult=compra(target_price_buy,0.01*indicador_compras)       #si llego aqui se compra
            buyresult=compra(target_price_buy,0.1)
            if (buyresult!=None):
                last_buy_id=buyresult["id"]
                time.sleep (1)
        else:
                print("No se cumple la condición dismuimos el precio de compra")
                target_price_buy=target_price_buy-0.0002



    print ("Price="+str(actual_price))
    time.sleep (1)
    #print (get_order_list())
    #if (auth_client.get_orders>0)
    #data = get_order_list()
    #for item in data:
    #    print("ITEM")
    #    tweet = json.loads(item[0])
    #    print(tweet["status"])

    resultado= get_order_list()

    #print (ordenes_abiertas)

    if (ordenes_abiertas == 1 ):

        for x in resultado:
            for y in x:
                ordenes_abiertas=len(x)
                #print (ordenes_abiertas)
                #la orden que no esté es la que se ejecutó...
                t = y
                if ((t["status"] == 'open') and (t["side"] == 'buy')):
                    #print(bcolors.CLOSED+"Se ejecuta la orden de venta"+bcolors.ENDC )
                    #print(ver_fills())
                    last_sell_price=get_current_price()
                    last_sell_price_media= (last_sell_price_media + last_sell_price)/2



                if ((t["status"] == 'open') and (t["side"] == 'sell')):
                    #print(bcolors.CLOSED+"Se ejecuta la orden de compra" +bcolors.ENDC )
                    #print(ver_fills())
                    last_buy_price=get_current_price()
                    last_buy_price_media=(last_buy_price_media +last_buy_price)/2

        modificador= get_last_fill(total_ventas,total_compras)
        if (modificador == None):
            modificador=0
        else:
            indicador=indicador+modificador

        cancela_todo()
        time.sleep (1)
        ordenes_abiertas=0




    for x in resultado:
        for y in x:
            ordenes_abiertas=len(x)
            #print (ordenes_abiertas)
            t = y
            if ((t["status"] == 'open') and (t["side"] == 'buy')):
                print(bcolors.BUY+"Status: " +t["status"] +"   id: "+t["id"] + "    Side: "+t["side"]+ "    price: "+t["price"]+"   size: "+t["size"] +bcolors.ENDC )

            if ((t["status"] == 'open') and (t["side"] == 'sell')):
                print(bcolors.SELL+"Status: " +t["status"] +"   id: "+t["id"] + "    Side: "+t["side"]+ "    price: "+t["price"]+"   size: "+t["size"] +bcolors.ENDC )

            if ((t["status"] == 'filled') and (t["side"] == 'sell')):
                print(bcolors.CLOSED+"Status: " +t["status"] +"   id: "+t["id"] + "    Side: "+t["side"]+ "    price: "+t["price"]+"   size: "+t["size"] +bcolors.ENDC )

            if (t["status"] != 'open'):
                print(bcolors.CLOSED+"Status: " +t["status"] +"   id: "+t["id"] + "    Side: "+t["side"]+ "    price: "+t["price"]+"   size: "+t["size"] +bcolors.ENDC )
            #print("id: "+t["id"])
            #print("Side: "+t["side"])



        #print (tweet)
        #:print (x[1])



            # check response
            ##""    if response is None:
            ##           return
              ##    elif 'message' in response:
                ##      self.messages.append(response['message'])
                  ## return
               ##       else:""
