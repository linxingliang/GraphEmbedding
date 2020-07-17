# -*- coding: utf-8 -*-
# @Time    : 2020/7/17 14:47
# @Author  : Aliang
# @Email   : linxingliang@163.com
# @File    : gen_dreame_cat.py
# @Software: PyCharm

import pandas as pd
import sys
sys.path.append('../')
from src.connection_library import DiskFileSystem, get_db, get_beanstalk_conn, get_redis_con
from src.config import args
import pickle


class GenNovelCat(object):
    def __init__(self, args):
        self.online_sql_h = args.online_sql_h
        self.online_sql_u = args.online_sql_u
        self.online_sql_p = args.online_sql_p
        self.online_sql_d = args.online_sql_d

    def download(self):
        sql = "SELECT id,cat_id FROM `t_book_new` WHERE book_type = 1 and (source_id = 1 or source_id = 2 or source_id = 3) and (is_del = 0 or is_del = 99) and word_count > 0"
        con = get_db(host=self.online_sql_h, username=self.online_sql_u, password=self.online_sql_p, database=self.online_sql_d)
        data = pd.read_sql(sql, con)
        print(data.head())
        data['id'] = data['id'].astype(str)
        data['cat_id'] = data['cat_id'].astype((str))
        self.data_dic = data.set_index('id')['cat_id'].to_dict()
        print(self.data_dic)

    def read_edges(self):
        edges_path = '../data/dream/edges'
        fin = open(edges_path, 'r')
        X = []
        Y = []
        while 1:
            l = fin.readline()
            if l == '':
                break
            vec = l.strip().split('\t')
            X.append(vec[0])
        fin.close()
        X = list(set(X))
        for i in X:
            Y.append(self.data_dic[i])
        data = [X, Y]
        print(data)
        with open('../data/dream/label', 'wb') as f:
            pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    GN = GenNovelCat(args)
    GN.download()
    GN.read_edges()

