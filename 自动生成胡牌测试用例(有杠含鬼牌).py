#-*-coding:utf-8-*-
#a代表万 b代表筒 c代表条
import collections
import random
import myutil
class GenTestCase:
    r = random.Random()
    template = sorted([i + str(j) for i in 'abc' for j in range(1, 10)])
    @staticmethod
    def getGen(lenth):
        for i in range(1, 15)[::3]:
            if i == lenth:
                return GenTestCase(lenth)
        raise Exception('wrong lenth!')
    def __init__(self,lenth):
        self.lenth=lenth
    def __getOne(self):
        return self.r.choice('abc')+str(self.r.choice(range(1,10)))
    def __getRan(self, lenth, ign=None):
        if not ign:
            return myutil.genRanList(self.template[:],lenth,3)
        return myutil.genRanList(sorted(list(set(self.template[:]).difference(set(ign)))), lenth, 3)
    def __getDkgang(self, lenth, ign=None):
        times = lenth / 4  # 暗杠最多出现的次数
        if times <1:
            return
        while True:
            dgangs = sorted(self.__getRan(random.randint(1, times), ign=ign))  
            if len(set(dgangs))==len(dgangs):
                break
        return sorted([i for i in dgangs] * 4)

    def __getFlush(self,c):
        n = int(c[1])
        if n > 7:
            return []
        return [c[0] + str(i) for i in range(n, n + 3)]
    def __getThree(self,c):
        return [c]*3
    def __gethuitem(self):
        while True:
            LF = map(self.r.choice([self.__getThree, self.__getFlush]),[self.__getOne() for i in range(self.lenth / 3)])
            LFT = [j for i in LF for j in i] + [self.__getOne()] * 2
            d = collections.Counter(LFT)
            if len(LFT)-1==self.lenth and not len([i for i in d.keys() if d[i] >4]):
                return LFT

    def __getDarkGangHu(self):
        while True:
            item = self.__gethuitem()
            d = collections.Counter(item)
            dg = [i for i in d.keys() if d[i] == 4]
            if len(dg):
                return item

    def getGHu(self, hasdgang=False):
        if hasdgang:
            while True:
                item= self.__getDarkGangHu()
                d = collections.Counter(item)
                dg = [i for i in d.keys() if d[i] == 4]
                dgPrtOne=self.r.choice(dg)#选择一个暗杠保护
                nodgPrtOne = [i for i in item if i != dgPrtOne]  # 除去被保护杠的手牌
                ghost = ''.join(self.__getRan(1,[dgPrtOne]))#选择一个鬼牌
                if ghost in nodgPrtOne:
                    print item,'item'
                    print dgPrtOne,'要保护的暗杠'
                    print nodgPrtOne,'去除被保护的鞍钢的手牌'
                    print ghost,'鬼在手牌里里面'
                    ghosts = [i for i in nodgPrtOne if i == ghost]
                    print ghosts, '统计手里鬼牌'
                    if not len(ghosts):
                        noghosts = [i for i in nodgPrtOne if i != ghost]
                        print noghosts,'无鬼的手牌'
                        times = random.randint(1, 4 - len(ghosts))  # 除去手牌中的鬼，其余牌随机变鬼的随机次数
                        print times,'鬼次'
                        become = random.sample(noghosts, times)  # 将要变鬼的手牌
                        print become,'变鬼'
                        [noghosts.remove(i) for i in become]  # 删除将要变鬼的手牌
                        final = noghosts + [ghost] * times + ghosts + [dgPrtOne]*4# 删除将变鬼的牌的手牌+变鬼+手牌里本来就有的鬼+被保护的鞍钢
                    else:
                        final=item #选鬼全在手牌里面，无需变鬼
                else:
                    print item,'item'
                    print dgPrtOne,'要保护的暗杠'
                    print nodgPrtOne,'去除被保护的鞍钢的手牌'
                    print ghost,'选鬼'
                    times=random.randint(1,4)#变鬼牌随机次数
                    become = random.sample(nodgPrtOne, times)
                    print become,'变鬼'
                    [nodgPrtOne.remove(i) for i in become]#删除变鬼的牌
                    final= nodgPrtOne+[dgPrtOne]*4+[ghost]*times
                    print final

                get = self.r.choice(final)
                final.remove(get)
                print final, get, ghost
                return ''.join(final) + ';' + get + ';1;1;' + ''.join(ghost) + '\n'

    def getHu(self, hasdgang=False):
        if not hasdgang:
            while True:
                s = map(self.r.choice([self.__getThree, self.__getFlush]),
                        [self.__getOne() for i in range(self.lenth / 3)])
                SFT = [j for i in s for j in i] + [self.__getOne()] * 2
                d = collections.Counter(SFT)
                if len(SFT) == self.lenth + 1 and not len([i for i in d.keys() if d[i] > 3]):
                    ghost = ''.join(self.__getRan(1, SFT))
                    get = self.r.choice(SFT)
                    SFT.remove(get)
                    return ''.join(SFT) + ';' + get + ';1;0;' + ghost + '\n'
        else:
            while True:
                s = map(self.r.choice([self.__getThree, self.__getFlush]),
                        [self.__getOne() for i in range(self.lenth / 3)])
                SFT = [j for i in s for j in i] + [self.__getOne()] * 2

                d = collections.Counter(SFT)
                if len(SFT) == self.lenth + 1 and len([d[i] for i in d.keys() if d[i] == 4]):
                    ghost = ''.join(self.__getRan(1, SFT))
                    get = self.r.choice(SFT)
                    SFT.remove(get)
                    return ''.join(SFT) + ';' + get + ';1;1;' + ghost + '\n'

def write(lenth,item):
    g=GenTestCase.getGen(lenth)
    with open(u'胡牌有鬼有杠','w') as f:
        #GH=[g.getGHu() for i in range(item)]
        GHG = [g.getGHu(True) for i in range(item)]
        cntn=[i for i in GHG if i]
        f.write(''.join(cntn))

write(10,50000)
