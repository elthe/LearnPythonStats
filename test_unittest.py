#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
单体测试

这个类的实例表示一个测试用例，默认的methodName是runTest，
即最简单的测试用例类的定义只包含runTest方法的定义。
如果同时定义了runTest方法和以test开头命名的方法，会忽略runTest方法。
"""

import unittest

from common import logcm


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        测试用例们被执行前执行的方法，定义时必须加上classmethod装饰符
        :return:
        """
        logcm.print_info('setUpClass ...')

    def setUp(self):
        """
        在执行每个测试用例之前被执行，任何异常（除了unittest.SkipTest和AssertionError异常以外）
        都会当做是error而不是failure，且会终止当前测试用例的执行。
        :return:
        """
        logcm.print_info('setUp ...')

    def tearDown(self):
        """
        执行了setUp()方法后，不论测试用例执行是否成功，都执行tearDown()方法。
        如果tearDown()的代码有异常(除了unittest.SkipTest和AssertionError异常以外)，会多算一个error。
        :return:
        """
        logcm.print_info('tearDown ...', show_header=False)

    @classmethod
    def tearDownClass(cls):
        """
        测试用例们被执行后执行的方法，定义时必须加上classmethod装饰符
        :return:
        """
        logcm.print_info('tearDownClass ...')

    def test_equal(self):
        logcm.print_info('test_equal ...', show_header=False)
        self.assertEqual(1, 1, '1 not equals 1')

    def test_true(self):
        logcm.print_info('test_true ...', show_header=False)
        self.assertTrue('LOO'.isupper(), 'LOO not upper')

