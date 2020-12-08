from pycoingecko import CoinGeckoAPI


CoinG = CoinGeckoAPI()

def trans(text):
    import re
    text = re.sub(r"Bitcoin", "btc", text)
    text = re.sub(r"Litecoin", "ltc", text)
    text = re.sub(r"USD", "usd", text)
    text = re.sub(r"Etherium", "eth", text)
    text = re.sub(r"Tron", "trx", text)
    text = re.sub(r"Ripple", "xrp", text)
    text = re.sub(r"Naira", "ngn", text)
    return(text)


def convert_to(A,B,value) -> str:
    """ Converts A to B given thier exchange rates """
    A = A.lower()
    B = trans(B)
    value = int(value)
    crypto = ['bitcoin','ripple','litecoin', 'ethereum']
    try:
        results = CoinG.get_price(ids=crypto,vs_currencies=B)
    except:
        return("Sorry an unexpected error occured")
    rate  = results[A][B]
    	
    ans = f"1 {A} = {rate}{B}\n{value}{A} = {value*rate}{B}"
    return(ans)
