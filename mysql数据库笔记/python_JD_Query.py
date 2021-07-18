from pymysql import connect

class JD(object):
    def __init__(self):
        # 1、创建conn连接
        self.conn = connect(host='localhost', port=3306, user='mysql', password='qwe123', database='jing_dong', charset='utf8')
        # 2、获取cursor对象
        self.cursor = self.conn.cursor()
        print('ok')

    def __del__(self):
        ''' 关闭cursor对象 '''
        self.cursor.close()
        self.conn.close()

    def execute_sql(self, sql):
        self.cursor.execute(sql)
        for temp in self.cursor.fetchall():
            print(temp)

    def show_all_goods(self):
        sql = "select * from goods;"
        self.execute_sql(sql)

    def show_goods_category(self):
        ''' 显示所有的商品分类 '''
        sql = "select DISTINCT cate_name from goods"
        self.execute_sql(sql)

    def show_goods_brand_category(self):
        ''' 显示所有的商品品牌分类 '''
        sql = "select DISTINCT brand_name from goods"
        self.execute_sql(sql)

    def add_brands(self):
        ''' 添加一行数据 '''
        item_name = input('请输入要添加的名字：')
        sql = "insert into goods_brands (name) values ('{}')".format(item_name)
        self.cursor.execute(sql)
        self.conn.commit()

    # @staticmethod
    def welcome_mune(self):
        print('********京东商城********')
        print('1：所有的商品')
        print('2：所有的商品分类')
        print('3：所有的商品品牌分类')
        print('4: 添加一行数据')
        return input('请输入查询功能对应的序号：')

    def run(self):
        while True:
            select_num = self.welcome_mune()
            if select_num == '1':
                # 查询所有商品
                self.show_all_goods()
            elif select_num == '2':
                # 查询所有的商品分类
                self.show_goods_category()
            elif select_num == '3':
                # 查询所有的商品品牌分类
                self.show_goods_brand_category()
            elif select_num == '4':
                # 添加一行数据
                self.add_brands(item_name)
            else:
                print('输入有误，请重新输入...')

def main():
    # 1、创建一个对象
    jd = JD()
    # 2、调用对象的run方法，使其运行
    jd.run()


if __name__ == '__main__':
    main()
