from MiningNetwork import MiningNetwork
import time

bot = MiningNetwork()
bot.authorization_load()

circle = 1

while True:

    print(f'[Круг {circle}]')

    time.sleep(10)
    bot.collect_reward()
    bot.collect_id(100)
    bot.upgrade_nft()
    # bot.sell_shares()

    circle += 1
    time.sleep(60)

