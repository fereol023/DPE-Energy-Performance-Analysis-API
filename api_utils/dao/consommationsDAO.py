from api_utils.queries.consommations import create_table as CREATE_CONSOMMATIONS_TABLE_QUERY

def select_all_consommations(conn):
    """
    Fetch all records from the consommations table.

    :param conn: Database connection object
    :return: List of all records from the consommations table
    """
    query = "SELECT * FROM consommations"
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


def insert_many_consommations(conn, consommations):
    """
    Insert multiple records into the consommations table.

    :param conn: Database connection object
    :param consommations: List of dictionaries containing consommation data
    :return: Number of rows inserted
    """
    # Extract column names from the CREATE_CONSOMMATIONS_TABLE_QUERY
    columns = CREATE_CONSOMMATIONS_TABLE_QUERY.split('(')[1].split(')')[0].split(',')
    column_names = [col.split()[0].strip() for col in columns]

    # Dynamically build the query
    placeholders = ', '.join(['%s'] * len(column_names))
    query = f"""
    INSERT INTO consommations ({', '.join(column_names)}) 
    VALUES ({placeholders})
    """
    try:
        cursor = conn.cursor()
        values = [[cons[col] for col in column_names] for cons in consommations]
        cursor.executemany(query, values)
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
        return 0
    finally:
        cursor.close()