import argparse
parser = argparse.ArgumentParser()

# 公共使用的配置文件
parser.add_argument("--mode", default='remote', type=str, help="连接数据库的模式，server直连，remote跳板机")

parser.add_argument("--test_sql_h", default='172.31.61.41', type=str, help="测试mysql host")
parser.add_argument("--test_sql_u", default='hwdata', type=str, help="测试mysql user")
parser.add_argument("--test_sql_p", default='Pass4dat@2018!0', type=str, help="测试mysql password")

parser.add_argument("--online_sql_h", default='coredb-cluster.cluster-cxs17h1ropjt.us-east-1.rds.amazonaws.com',
                    type=str, help="线上mysql host")
parser.add_argument("--online_sql_u", default='analyzer', type=str, help="线上mysql user")
parser.add_argument("--online_sql_p", default='P@ss4Aanlyze', type=str, help="线上mysql password")
parser.add_argument("--online_sql_d", default='xiaoshuo', type=str, help="线上mysql password")

parser.add_argument('--disk_host', default='172.31.61.42', type=str, help='dreame硬盘文件系统访问地址')
parser.add_argument('--disk_port', default=4102, type=int, help='dreame硬盘文件系统访问端口')

parser.add_argument('--bs_host', default="172.31.61.41", type=str, help='dreame beanstalk监听host')
parser.add_argument('--bs_port', default=11300, type=int, help='dreame beanstalk监听port')
parser.add_argument('--bs_tube', default="stary_user_log_for_realtime", type=str, help='dreame beanstalk监听tube')

# 解密配置文件
parser.add_argument('--key', default="kfd8127f2hdask2a", type=str, help='解密key')
parser.add_argument('--iv', default="3902746731267123", type=str, help='解密iv')
parser.add_argument('--salt', default="19836", type=str, help='解密salt')

# recall使用的配置文件
parser.add_argument('--verbose', type=int, default=3, help='0 : no stdout, 1: print userkey')
parser.add_argument('--max_queue_length', type=int, default=200, help='0 : no stdout, 1: print userkey')
parser.add_argument('--time_limit', type=int, default=1, help='0 : no stdout, 1: print userkey')

# ctr使用的配置文件
parser.add_argument("--read_window", default=3, type=int, help="read序列的窗口大小")
parser.add_argument("--cat_window", default=3, type=int, help="category的窗口大小")
parser.add_argument("--tag_window", default=3, type=int, help="tag的窗口大小")
parser.add_argument("--pre_tag_window", default=3, type=int, help="用户画像标签的窗口大小")
parser.add_argument("--pre_cat_window", default=3, type=int, help="用户画像类别的窗口大小")
parser.add_argument("--ratio", default=3, type=int, help="正负样本的比例")
parser.add_argument("--data_path", default=r'../data/ctr_data', type=str, help="存放数据的文件夹")
parser.add_argument("--read_enc", default=r'../data/ctr_data/read_enc_dic.pkl', type=str, help="阅读行为编码字典的路径")
parser.add_argument("--cat_enc", default=r'../data/ctr_data/pre_cat_enc_dic.pkl', type=str, help="分类编码字典的路径")
parser.add_argument("--tags_enc", default=r'../data/ctr_data/pre_tags_enc_dic.pkl', type=str, help="标签编码字典的路径")
parser.add_argument("--novel_info", default=r'../data/ctr_data/novel_info_dic.pkl', type=str, help="小说信息表的路径")
parser.add_argument("--model_path", default=r'../data/ctr_model/DeepFM.pb', type=str, help="模型储存的路径")
parser.add_argument("--TopK", default=45, type=int, help="TopK")
parser.add_argument("--hot_TopK", default=5, type=int, help="热门召回的topk")
parser.add_argument("--pre_batch", default=50000, type=int, help="预测的batch")

args = parser.parse_args()
