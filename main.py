import time

from MiningNetwork import MiningNetwork


def main():
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

if __name__ == '__main__':
    main()
