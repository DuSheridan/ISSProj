import psycopg2
import json
import traceback

from flask import current_app, g

from modules.lib.formatted_output import Output, Status


def get_db(database):
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.

    :param database: Database key set in Flask's config.
    :type database: str
    :return: Connection
    :rtype: :class:`psycopg2.connection`
    """
    if "db" not in g:
        g.db = {}

    if database not in current_app.config["DATABASE"]:
        raise KeyError(
            "The database '{}' is not defined in "
            "the current config (ENV: '{}').".format(
                database, current_app.config["ENV"]
            )
        )

    if database not in g.db:
        g.db[database] = psycopg2.connect(
            "host={HOST} user={USER} password={PASSWORD} dbname={NAME}".format(
                **current_app.config["DATABASE"][database]
            )
        )
    return g.db[database]


def close_db(e=None):
    """If this request was connected to the database, close the
    connection.
    """
    db = g.get("db", None)

    if db is not None:
        for key in list(db):
            if not db[key].closed:
                db[key].close()
            db.pop(key)


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)


def execute_query_and_return_output(db_key, query, query_data, commit=False, fetch=None, fetch_all=None,
                                    no_result_message="No data found."):
    try:
        result = execute_query(db_key, query, query_data, commit=commit, fetch=fetch, fetch_all=fetch_all)
        current_app.logger.debug("Query result: {}".format(result))
        if result:
            if fetch_all:
                data = [dict(r) for r in result]
            elif fetch:
                data = dict(result)
            else:
                data = result  # None

            return Output(status=Status.SUCCESS, data=data).as_dict()

        return Output(status=Status.WARNING, message=no_result_message).as_dict()

    except (psycopg2.OperationalError, psycopg2.ProgrammingError) as pge:
        return Output(status=Status.ERROR, message=pge).as_dict()


def execute_query(db_key, query, query_params=None, commit=False, fetch=None, fetch_all=None, check_result=False):
    """
    Executes the query on the specified database
    :param db_key: <str> Key to identify db in the config
    :param query: <str> The query string, already properly formatted
    :param query_params: <dict> the query parameters to be used
    :param commit: <bool> Specifies whether to commit the transaction is committed
    :param fetch: <bool> If set to true, returns the result of the query
    :param fetch_all: <bool> If set to true, returns the list of results of the query
    :param check_result: <bool> If set to true, checks if any result was returned by the query
    """
    result = None
    db_connection = None
    cursor = None
    try:
        db_connection = get_db(db_key)
        cursor = db_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        current_app.logger.debug("Executing the following query: \n{}\nusing these params: {}".format(query,
                                                                                                      query_params))
        cursor.execute(query, query_params)
        if commit:
            db_connection.commit()
        if fetch:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
        if check_result:
            assert result
    except (psycopg2.OperationalError, psycopg2.InterfaceError, psycopg2.ProgrammingError, AssertionError) as pge:
        current_app.logger.error(pge)
        current_app.logger.error(traceback.format_exc())
        if commit and db_connection:
            db_connection.rollback()
        if cursor:
            cursor.close()
        raise
    finally:
        if cursor:
            cursor.close()
    return result


def generate_insert_query(table_name, insert_data, returning=None, multiple=False):
    """Creates the insert query string"""
    if multiple:
        query = """"
            INSERT INTO {} 
            ({}) 
            VALUES %s
        """.format(table_name, ", ".join(insert_data.keys()))
    else:
        query = """
            INSERT INTO {} 
            ({}) 
            VALUES 
            ({})
        """.format(
            table_name, ", ".join(insert_data.keys()),
            _insert_notation_values(insert_data))

    if returning:
        query += " RETURNING {};".format(returning)
    else:
        query += ";"
    return query


def _insert_notation_values(insert_data):
    """
    Creates the text corresponding to the VALUES (...) part of the INSERT QUERY
    Depending on the type of each piece of data, the text is differently formulated.
    Thus, dictionary object correspond to JSONB fields.
    If an value is passed as bytes, it is interpreted as a database valid object (usually a function call)
    The rest of them are passed as strings.
    :return: The VALUES value
    """
    values = []
    for k in insert_data.keys():
        if type(insert_data[k]) in [list, dict]:
            insert_data[k] = json.dumps(insert_data[k], indent=4)
            values.append("%({})s::JSONB".format(k))
        elif type(insert_data[k]) == bytes:
            values.append(str(insert_data[k], 'utf-8'))
        else:
            values.append("%({})s".format(k))

    return ", ".join(values)


def query_sequence_next_id():
    """
        Build the query to retrieves the next available id from the sequence name
    """

    query_next_sequence = """SELECT NEXTVAL(%(sequence_name)s) AS id;"""
    return query_next_sequence
