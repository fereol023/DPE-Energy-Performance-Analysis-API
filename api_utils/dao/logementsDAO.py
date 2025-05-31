from api_utils.queries.logements import create_table as CREATE_LOGEMENTS_TABLE_QUERY

def select_all_consommations(conn):
    """
    Fetch all records from the consommations table.

    :param conn: Database connection object
    :return: List of all records from the consommations table
    """
    query = "SELECT * FROM logements"
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        cursor.close()


def insert_many_consommations(conn, logements):
    """
    Insert multiple records into the consommations table.

    :param conn: Database connection object
    :param logements: List of dictionaries containing logements data
    :return: Number of rows inserted
    """
    # Extract column names 
    columns = CREATE_LOGEMENTS_TABLE_QUERY.split('(')[1].split(')')[0].split(',')
    column_names = [col.split()[0].strip() for col in columns]

    # Dynamically build the query
    placeholders = ', '.join(['%s'] * len(column_names))
    query = f"""
    INSERT INTO logements ({', '.join(column_names)}) 
    VALUES ({placeholders})
    """
    try:
        cursor = conn.cursor()
        values = [[l[col] for col in column_names] for l in logements]
        cursor.executemany(query, values)
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
        return 0
    finally:
        cursor.close()