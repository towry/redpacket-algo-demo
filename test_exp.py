from random import expovariate as exp
import math


def test_exp():
    max = 100
    min = 10

    lambd = (max + min) / 2
    r = exp(lambd)
    money = min + r * max
    return money


def test_exp_round():
    rounds = 100
    res = []
    while rounds > 0:
        rounds -= 1
        money = test_exp()
        money = math.floor(money * 100) / 100
        res.append(money)

    res.sort()
    print res

if __name__ == "__main__":
    test_exp_round()
