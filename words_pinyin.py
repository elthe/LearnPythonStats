#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
汉字转拼音
"""

# import pypinyin
from common import logcm

# from pypinyin import pinyin, lazy_pinyin
import pinyin
import unittest
from pinyin._compat import u

#
# py_list = lazy_pinyin(u'云浮新兴双线-01')
#
# logcm.print_obj(py_list, "py_list")
#
# py_str = ''.join(py_list)
#
# logcm.print_obj(py_str, "py_str")

def to_pinyin(var_str):
    """
    汉字[钓鱼岛是中国的]=>拼音[diaoyudaoshizhongguode]\n
    汉字[我是shui]=>拼音[woshishui]\n
    汉字[AreYou好]=>拼音[AreYouhao]\n
    汉字[None]=>拼音[]\n
    汉字[]=>拼音[]\n
    :param var_str:  str 类型的字符串
    :return: 汉字转小写拼音
    """
    if isinstance(var_str, str):
        if var_str == 'None':
            return ""
        else:
            return pinyin.get(var_str, format='strip', delimiter="")
    else:
        return '类型不对'

class TestPinYin(unittest.TestCase):
    def test_to_pinyin(self):
        list = ['钓鱼岛是中国的', '我是shui', 'AreYou好', None, '']
        for i in list:
            print('汉字[%s]=>拼音[%s]' % (i, to_pinyin(str(i))))

    def test_get(self):
        self.assertEqual(pinyin.get('你好'),
                         pinyin.get('你好', format="diacritical"))
        self.assertEqual(pinyin.get(u('你好'), format="strip"), u('nihao'))
        self.assertEqual(pinyin.get(u('你好'), format="numerical"), u('ni3hao3'))
        self.assertEqual(pinyin.get(u('你好'), format="diacritical"), u('nǐhǎo'))
        self.assertEqual(pinyin.get('你好吗?'), u('nǐhǎoma?'))
        self.assertEqual(pinyin.get('你好吗？'), u('nǐhǎoma？'))

        self.assertEqual(pinyin.get('你好'), u('nǐhǎo'))
        self.assertEqual(pinyin.get('叶'), u('yè'))
        self.assertEqual(pinyin.get('少女'), u('shǎonv̌'))

    def test_get_with_delimiter(self):
        self.assertEqual(pinyin.get('你好', " "), u('nǐ hǎo'))
        self.assertEqual(pinyin.get('你好吗?', " "), u('nǐ hǎo ma ?'))
        self.assertEqual(pinyin.get('你好吗？', " "), u('nǐ hǎo ma ？'))

    def test_get_initial_with_delimiter(self):
        self.assertEqual(pinyin.get_initial('你好', "-"), u('n-h'))
        self.assertEqual(pinyin.get_initial('你好吗?', "-"), u('n-h-m-?'))
        self.assertEqual(pinyin.get_initial('你好吗？', "-"), u('n-h-m-？'))

    def test_get_initial(self):
        self.assertEqual(pinyin.get_initial('你好'), u('n h'))
        self.assertEqual(pinyin.get_initial('你好吗?'), u('n h m ?'))
        self.assertEqual(pinyin.get_initial('你好吗？'), u('n h m ？'))

        self.assertEqual(pinyin.get_initial('你好'), 'n h')

    def test_mixed_chinese_english_input(self):
        self.assertEqual(pinyin.get('hi你好'), u('hinǐhǎo'))

    def test_correct_diacritical(self):
        self.assertEqual(pinyin.get("操"), u("cāo"))
        self.assertEqual(pinyin.get("小"), u("xiǎo"))
        self.assertEqual(pinyin.get("绝"), u("jué"))
        self.assertEqual(pinyin.get("被"), u("bèi"))
        self.assertEqual(pinyin.get("略"), u("lvè"))

from pypinyin import pinyin, lazy_pinyin, Style

if __name__ == '__main__':
    #unittest.main()
    print(pinyin('你好吗?'))
