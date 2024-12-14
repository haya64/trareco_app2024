import psycopg2

class SELECTDATA:
    def __init__(self):
        # データベース接続を初期化
        self.connection = psycopg2.connect(
            host="localhost",
            port="5432",
            database="trareco",
            user="haya",
            password=""
        )

    def select(self, columns, table, where=None):
        # カーソルを作成
        cur = self.connection.cursor()

        # クエリを指定
        if where is not None:
            query = f'SELECT {columns} FROM {table} WHERE {where}'
        else:
            query = f'SELECT {columns} FROM {table}'

        # SQLクエリを実行
        cur.execute(query)

        # 結果を取得
        result = cur.fetchall()

        # カーソルを閉じる
        cur.close()

        return result

    def select_raw(self, query):
        """
        SQL クエリを直接実行して結果を返す。

        Parameters:
            query (str): 実行するSQLクエリ。

        Returns:
            list: クエリ結果のリスト。
        """
        cur = self.connection.cursor()

        # SQLクエリを実行
        cur.execute(query)

        # 結果を取得
        result = cur.fetchall()

        # カーソルを閉じる
        cur.close()

        return result

    def close(self):
        """データベース接続を閉じる"""
        self.connection.close()