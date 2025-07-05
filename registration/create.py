import dbutils.execute as exe

def insert_registration(PRN_NO, Name, RFID, Finger_Print):
    query = f"""
        INSERT INTO registration (PRN_NO, Name, RFID, Finger_Print)
        VALUES ('{PRN_NO}', '{Name}', '{RFID}', {Finger_Print});
    """
    exe.execute_query(query)