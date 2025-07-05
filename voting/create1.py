import dbutils.execute as exe

def insert_vote(prn, rfid, candidate):
    query = f"""
        INSERT INTO voting_data (PRN_NO, RFID, Selected_Candidate)
        VALUES ('{prn}', '{rfid}', '{candidate}');
    """
    exe.execute_query(query)
