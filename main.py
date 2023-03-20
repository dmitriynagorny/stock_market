import requests
import time
from threading import Thread
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Counter')


# Исполюзую binance для забора данных (Keys)
ETHUSDT_KEY = "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"
BTCUSDT_KEY = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

# Списки для хранения
eth_list = []
btc_list = []

time_start = time.time()


# Сохраняю цену пары ETHUSDT
def read_eth():
    while True:

        try:
            data = requests.get(ETHUSDT_KEY)
            data = data.json()

            if len(btc_list) > 1:
                true_price = float(data['price']) - float(data['price'])*((btc_list[-1] - btc_list[-2])/btc_list[-1]) # Определяю верную цену без фактора влияния USDT
                eth_list.append(true_price)
            else:
                eth_list.append(float(data['price']))

            if int(time.time() - time_start) >= 3600:
                eth_list.pop(0)

        except ValueError:
            logger.info('Error1')
        time.sleep(0.1)


# Сохраняю цену пары BTCUSDT
def read_btc():
    while True:

        try:
            data = requests.get(BTCUSDT_KEY)
            data = data.json()
            btc_list.append(float(data['price']))

            # Буду чистить список через час после начала, в списке будут цены в интервале 60 минут
            if int(time.time() - time_start) >= 3600:
                eth_list.pop(0)

        except ValueError:
            logger.info('Error2')

        time.sleep(0.1)


# Расчетная функция
def calc_percent_price():
    loop_var = 0
    while True:

        try:
            max_price = max(eth_list)
            min_price = min(eth_list)

            changes = max(abs((eth_list[-1] - max_price) / eth_list[-1]),
                          abs((eth_list[-1] - min_price) / eth_list[-1]))

            if changes > 1:
                print(f'Цена изменилась более чем на 1 процент')

            # Буду в логах выводить цену раз в 10 секунд
            if loop_var == 100:
                loop_var = 0
                logger.info(f'Present change price {eth_list[-1]}')

        except ValueError:
            logger.info(f'Lists is empty')
        time.sleep(0.1)
        loop_var += 1


# Буду использовать 3 потока
if __name__ == '__main__':
    Thread(target=read_btc).start()
    Thread(target=read_eth).start()
    Thread(target=calc_percent_price).start()