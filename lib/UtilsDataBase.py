# 创建pymysql工具类
import pymysql


# 创建工具类
class DataBaseUtils:

    __conn = None
    __cursor = None

    # 连接数据库方法
    @classmethod
    def __get_connect(cls):
        if cls.__conn is None:
            cls.__conn = pymysql.connect(host="52.83.144.39", port=3306, user="root", password="Itcast_p2p_20191228", database="czbk_member", charset="utf8", autocommit=True)
        return cls.__conn

    # 获取游标方法
    @classmethod
    def __get_cursor(cls):
        if cls.__cursor is None:
            cls.__cursor = cls.__get_connect().cursor()
        return cls.__cursor

    # 执行sql方法
    @classmethod
    def execute_sql(cls, string):
        try:
            # 执行sql，用__get_cursor()方法获取游标
            cursor = cls.__get_cursor()
            cursor.execute(string)
            # 如果切割获取到的第一个字符串是"select"，返回所有查询到的值
            if cls.__return_first_str(string) == "select":
                return cursor.fetchall()
            # 否则执行提交事务的语句
            else:
                cls.__get_connect().commit()
                # 返回受影响的行数
                return cls.__get_cursor().rowcount
        except Exception as result:
            # 发生异常，调用connect的rollback()方法，让事务回滚
            cls.__get_connect().rollback()
            #  打印异常信息
            print(result)
        finally:
            # 关闭游标和连接
            cls.__close_cursor()
            cls.__close_connect()

    # 关闭游标方法
    @classmethod
    def __close_cursor(cls):
        if cls.__cursor:
            cls.__cursor.close()
            cls.__cursor = None

    # 关闭连接方法
    @classmethod
    def __close_connect(cls):
        if cls.__conn:
            cls.__conn.close()
            cls.__conn = None

    # 以空格分隔，得到一个字符串的第一个子串
    @classmethod
    def __return_first_str(cls, string):
        str1 = str(string)
        return str1.split(" ")[0].lower()