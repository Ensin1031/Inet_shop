from decimal import Decimal

from main_app.tests.test_settings import ForGetFuncTests


class ShowObjectsTest(ForGetFuncTests):
    """test of class ShowObjects"""

    def test_validators_meta(self):
        print('-----test class ShowObjects in get_func----- ')
        print('obj_list =', self.test_list.obj_list)
        print('show_goods_all =', self.test_list.show_goods_all)
        print('rating_dict_all', self.test_list.rating_dict_all)
        print('promo_dict_all =', self.test_list.promo_dict_all)
        print('new_price_dict_all =', self.test_list.new_price_dict_all)
        print('sort_by_rating =', self.test_list.sort_by_rating)
        print('sort_by_price =', self.test_list.sort_by_price)
        print('sort_by_price_desc =', self.test_list.sort_by_price_desc)

    def test_valid_count(self):
        self.assertEqual(2, self.test_list.obj_list.count())

    def test_valid_sort_by_rating(self):
        self.assertEqual('testGood', self.test_list.sort_by_rating[0].title)
        self.assertEqual('testGoodForGetFunc', self.test_list.sort_by_rating[1].title)

    def test_valid_sort_by_price(self):
        self.assertEqual('testGoodForGetFunc', self.test_list.sort_by_price[0].title)
        self.assertEqual('testGood', self.test_list.sort_by_price[1].title)

    def test_valid_sort_by_price_desc(self):
        self.assertEqual('testGood', self.test_list.sort_by_price_desc[0].title)
        self.assertEqual('testGoodForGetFunc', self.test_list.sort_by_price_desc[1].title)

    def test_valid_new_price_dict_all(self):
        for obj in self.test_list.obj_list:
            if obj.title == 'testGoodForGetFunc':
                self.assertEqual(Decimal('150.38'), self.test_list.new_price_dict_all[obj])
            elif obj.title == 'testGood':
                self.assertEqual(Decimal('170.42'), self.test_list.new_price_dict_all[obj])

    def test_valid_promo_dict_all(self):
        for obj in self.test_list.obj_list:
            if obj.title == 'testGoodForGetFunc':
                self.assertEqual(Decimal('0.75'), self.test_list.promo_dict_all[obj]['discount_index'])
                self.assertEqual(25, self.test_list.promo_dict_all[obj]['discount'])
            elif obj.title == 'testGood':
                self.assertEqual(Decimal('0.85'), self.test_list.promo_dict_all[obj]['discount_index'])
                self.assertEqual(15, self.test_list.promo_dict_all[obj]['discount'])

    def test_valid_rating_dict_all(self):
        for obj in self.test_list.obj_list:
            if obj.title == 'testGoodForGetFunc':
                self.assertEqual(0, self.test_list.rating_dict_all[obj])
            elif obj.title == 'testGood':
                self.assertEqual(50, self.test_list.rating_dict_all[obj])

    def test_valid_show_goods_all(self):
        for obj in self.test_list.obj_list:
            if obj.title == 'testGoodForGetFunc':
                self.assertEqual(obj, self.test_list.show_goods_all[f'{obj.pk}']['product'])
                self.assertEqual(Decimal('150.38'), self.test_list.show_goods_all[f'{obj.pk}']['new_price'])
                self.assertEqual(0, self.test_list.show_goods_all[f'{obj.pk}']['rating'])
                self.assertEqual(25, self.test_list.show_goods_all[f'{obj.pk}']['promo'])
            elif obj.title == 'testGood':
                self.assertEqual(obj, self.test_list.show_goods_all[f'{obj.pk}']['product'])
                self.assertEqual(Decimal('170.42'), self.test_list.show_goods_all[f'{obj.pk}']['new_price'])
                self.assertEqual(50, self.test_list.show_goods_all[f'{obj.pk}']['rating'])
                self.assertEqual(15, self.test_list.show_goods_all[f'{obj.pk}']['promo'])


class ShowOneObjectTest(ForGetFuncTests):
    """test of class ShowOneObject"""

    def test_validators_meta(self):
        print('-----test class ShowOneObject in get_func----- ')
        print('good =', self.test_object.good)
        print('promo =', self.test_object.promo)
        print('rating =', self.test_object.rating)
        print('data_good =', self.test_object.data_good)

    def test_valid_good(self):
        self.assertEqual('testGood', self.test_object.good.title)

    def test_valid_promo(self):
        self.assertEqual(Decimal('0.85'), self.test_object.promo['discount_index'])
        self.assertEqual(15, self.test_object.promo['discount'])

    def test_valid_rating(self):
        self.assertEqual(50, self.test_object.rating['int_rating'])
        self.assertEqual(2, self.test_object.rating['reviews_list'].count())

    def test_valid_data_good(self):
        self.assertEqual(self.test_good, self.test_object.data_good['product'])
        self.assertEqual(Decimal('170.42'), self.test_object.data_good['new_price'])
        self.assertEqual(50, self.test_object.data_good['rating'])
        self.assertEqual(15, self.test_object.data_good['promo'])
        self.assertEqual(2, self.test_object.data_good['review_list'].count())


class GetPromoFuncTest(ForGetFuncTests):
    """test of function get_promo in get_func"""
    def test_valid_get_promo(self):
        self.assertEqual(Decimal('0.75'), self.test_get_promo)
