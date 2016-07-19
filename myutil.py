#  -*-coding:utf-8-*-
"""
此模块包装用于操作数据结构的函数
"""
import re
import copy
import collections
import random
##==================================================操作字符串==============================================================
def s_splitStr(str, length):
    """分割字符串为几个等长的子串，并以list返回
    :type str:str
    :type length:int
    :rtype: list
    """
    res,subStr,acc_subStr=[],'',''
    for i in range(0, len(str), length):
        for j in range(length):
            try:
                subStr=str[i+j]
            except IndexError:
                break
            acc_subStr+=subStr
        res.append(acc_subStr)
        acc_subStr=''
    return res

def s_cutSubStr(string,subStr):
    """
    去除一个字符串里面的子串
    :param string:
    :param subStr:
    :return:
    """
    index=string.find(subStr)
    if index==-1:
        return string
    head=string[:index]
    tail=string[index+len(subStr):]
    return head+tail

def s_maStr(rule,string):
    """
    正则表达式匹配字符串
    返回匹配结果
    :param string:
    :param rule:
    :return:
    """
    return re.findall(rule,string)
#==================================================操作列表==============================================================
#====字符串列表====
def L_matchStrList(strList,reRule):
    """用正则表达式匹配List里面的字符串元素
        返回匹配成功的list元素，和剩余未匹配成功的元素
        :type strList:List
        :type reRule:unknow
    """
    matchedContent,unMatchedContent= [],strList[:]
    for i in strList:
        matched = reRule.match(i)
        if matched:
            matchedContent.append(matched.group())
            unMatchedContent.remove(matched.group())
    return matchedContent

def L_listElmCutSubStr(strList,substr):
    """
    去除list字符串元素里的子串，
    返回一个新的list
    :param strList:
    :param substr:
    :return:
    """
    newList=[]
    for i in strList:
        newList.append(s_cutSubStr(i,substr))
    return newList

def genRanList(elmTpl,lenth,showtime=None):
    """
    随机取elmTpl的元素生成指定长度的list，
    showtims指定元素最多出现次数
    :param elmTpl:
    :param lenth:
    :param showtime:
    :return:
    """
    R=random.Random()
    if not showtime:
        return [R.choice(elmTpl) for i in range(lenth)]
    while True:
        ranlst=[R.choice(elmTpl) for i in range(lenth)]
        d=collections.Counter(ranlst)
        if not len([i for i in map(d.get,d.keys()) if i >showtime]):#提取字典的值为list检查是否有超过showtimes的
            return ranlst

def L_ListElmStoN(oneList,reverse=False):
    """
    转换多维list里面的数字字符串为数值型
    :param oneList: list
    :param reverse: bool
    :return:None
    """
    for i in range(len(oneList)):
        if type(oneList[i])==list:
            L_ListElmStoN(oneList[i])
        try:
            oneList[i]=int(oneList[i])
        except:
            continue
    oneList.sort(reverse=reverse)

def L_twoListDiff(blist,alist):
    """
    检测blist中有而alist没有的元素
    并装入新list返回
    :param blist:
    :param alist:
    :return:
    """
    return list(set(blist).difference(set(alist)))

def L_findBigLineInNumList(list,length):
    """
    在一个数值型list中找到指定长度的 最大的序列并返回
    :param list:
    :param length:
    :param little:未实现，有待实现功能
    :return:
    """
    list.sort(reverse=True)
    count,head,end= 1, list[0], 0
    for i in range(len(list)):
        if count == length:
            end=list[i]
            break
        try:
            if list[i]-1==list[i+1]:
                count+=1
                continue
            else:
                count,head= 1, list[i + 1]
                continue
        except IndexError:
            return
    return range(end,head+1)[::-1]

def L_twoLtoADict(keylist,valuelist):
    """
    把两个list转换为一个字典
    :param keylist:
    :param valuelist:
    :return:
    """
    if not keylist or not valuelist:
        return
    return dict(zip(keylist, valuelist))

def L_LtoD(list):
    """
    统计list中重复出现的元素
    返回字典
    :param list:
    :return:
    """
    return collections.Counter(list)

#==================================================操作字典==============================================================
def d_clearDictValue(dict, value):
    """
    删除字典内值为value的键值对
    :param dict:
    :param value:
    :return:
    """
    for k in dict.keys():
        if dict[k]==value:
            del dict[k]

def d_findMaxKey(dict, whenValueIs=None):
    """
    从字典查找其值为whenValueIs的最大的键名，
    并返回该键值对，不指定whenValueIs时返回键名最大的键名
    :param dict:
    :param whenValueis: 指定当键对应的值为whenValueis为时,若不指定则只找最大键名
    :return:
    """
    if not whenValueIs:
        return sorted(dict.keys(), reverse=True)[0]
    for k in sorted(dict.keys(),reverse=True):
        if dict[k]==whenValueIs:
            return k

def d_addAllDictItem(dict):
    """
    把字典里的值累加并返回
    :param dict:
    :return:
    """
    count=0
    for k in dict:
        num=dict[k]
        count+=num
    return count

def d_filterDict(dict,tuple):
    """
    把原始字典按tuple里的类型 过滤掉以这些类型 作为值的键值对
    并返回过滤出来值
    :param dict:
    :param tuple:
    :return:
    """
    fdict={}
    for k in dict.keys():
        if isinstance(dict[k],tuple):
            fdict[k]=dict[k]
            dict.pop(k)
    return fdict

def d_dictUnion(d1,d2):
    """
    返回两个字典的并集
    :param d1:
    :param d2:
    :return:
    """
    return dict(d1, **d2)
#==================================================操作集合=============================================================


#==================================================操作哈希表==============================================================
def h_countHashTableEachItem(hashTable):
    """
    统计哈希表各项的长度，
    返回字典
    :param hashTable:
    :return:
    """
    statistics=hashTable.copy()
    for k in statistics:
        statistics[k]=len(statistics[k])
    return statistics

def h_countHashTableAllItem(hashTable):
    """
    统计哈希表各项长度之和
    返回数值型
    :param hashTable:
    :return:
    """
    count=0
    for k in hashTable:
        oneLen=len(hashTable[k])
        count+=oneLen
    return count

def h_findHashEachHead(hashTable,reverse=False):
    """
    取出哈希表每项的头个元素，组成一个list并返回
    :param hashTable:
    :param reverse:指定读取顺序
    :return:
    """
    L=[]
    index=sorted(hashTable.keys(),reverse=reverse)
    for k in index:
        L.append(hashTable[k][0])
    return L

def h_hashRev(hashTable):
    """
    反转哈希表
    :param hashTable:
    :return:
    """
    if not hashTable:
        return
    newDict={}
    for k in hashTable.keys():
        for i in hashTable[k]:
            newDict[i]=[]
    for k in hashTable.keys():
        for i in hashTable[k]:
            newDict[i].append(k)
    return newDict

def h_rmHashItemByLen(hashTable,lenth):
    """
    按指定的项长度删除哈希表的项
    :param hashTable:
    :param lenth:int
    :return:
    """
    newHashTable=copy.deepcopy(hashTable)
    for k in newHashTable.keys():
        if len(newHashTable[k])==lenth:
            newHashTable.pop(k)
    return newHashTable
#==============================================操作哈希集合================================================
def diffhashset(bigSet,smallSet):
    """
    取bigSet与smallSet的差集
    :param bigSet:
    :param smallSet:
    :return:
    """
    repKys=dict.fromkeys(x for x in bigSet if x in smallSet).keys()#找出bigset中的smallset的键子集
    newhash={}
    for i in repKys:
        newhash[i]=L_twoListDiff(bigSet[i],smallSet[i])
    notRepKys = dict.fromkeys(x for x in bigSet if x not in smallSet).keys()#找出bigSet中smallset没有的键子集
    for i in notRepKys:
        newhash.update({i:bigSet[i]})
    return newhash

def callmore(func,times):
    """
    调用func函数times次
    把结果装入列表返回
    :param func:
    :param times:
    :return:
    """
    resultList=[]
    while times:
        resultList.append(func())
        times-=1
    return resultList