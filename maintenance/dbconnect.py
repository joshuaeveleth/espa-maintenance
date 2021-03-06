# TODO Look at making an actual sub-class of connect and cursor to open up more
# TODO built in functionality
import psycopg2
import psycopg2.extras
import psycopg2.extensions
import numbers


class DBConnectException(Exception):
    pass

class DBConnect(object):
    """
    Class for connecting to a postgresql database using a single with statement
    """
    def __init__(self, dbhost='localhost', db='postgres', dbuser='postgres', dbpass='postgres',
                 dbport=5432, autocommit=False, cursor_factory=None, *args, **kwargs):
        try:
            self.conn = psycopg2.connect(host=dbhost, database=db, user=dbuser,
                                         password=dbpass, port=dbport)
            self.cursor = self.conn.cursor(cursor_factory=cursor_factory)
        except psycopg2.Error as e:
            raise DBConnectException(e)

        self.autocommit = autocommit
        self.fetcharr = []

    def execute(self, sql_str, params=None):
        """
        Used for enacting some change on a database
        """
        if params and not self.verify_type(params):
            params = self.conv_totuple(params)

        try:
            self.cursor.execute(sql_str, params)
        except psycopg2.Error or psycopg2.Warning as e:
            raise DBConnectException(e)

        if self.autocommit:
            self.commit()

    def select(self, sql_str, params=None):
        """
        Used for retrieving information from the database
        Results are stored in self.fetcharr to enable more flexible use
        Each row result is stored as a tuple in the list array
        """
        if params and not self.verify_type(params):
            params = self.conv_totuple(params)

        try:
            self.cursor.execute(sql_str, params)
            self.fetcharr = self.cursor.fetchall()
        except psycopg2.Error as e:
            raise DBConnectException(e)

    def commit(self):
        try:
            self.conn.commit()
        except psycopg2.Error as e:
            raise DBConnectException(e)

    def rollback(self):
        self.conn.rollback()

    @staticmethod
    def conv_totuple(val):
        """
        Allow for single string or number parameters to be passed in easier
        trying to avoid future issues with forgetting to wrap a single param
        in a tuple
        """
        if isinstance(val, (str, numbers.Number)):
            val = (val, )
        else:
            raise DBConnectException('Parameter not a valid string or number')

        return val

    @staticmethod
    def verify_type(val):
        """
        Verify the type is a sequence
        """
        # Leery of opening it up to all iter types
        # though psycopg2 documentation says it is supported
        if isinstance(val, (tuple, list, dict)):
            return True
        else:
            return False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.cursor.close()
            self.conn.close()
        except psycopg2.Error as e:
            raise DBConnectException(e)

    def __len__(self):
        return len(self.fetcharr)

    def __iter__(self):
        return iter(self.fetcharr)

    def __getitem__(self, item):
        try:
            return self.fetcharr[item]
        except IndexError:
            raise

    def __del__(self):
        try:
            self.cursor.close()
            self.conn.close()

            del self.cursor
            del self.conn
        except Exception as e:
            raise DBConnectException(e)
