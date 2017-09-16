cursor.execute("SELECT message,time FROM wallofshame")
        rows = cursor.fetchall()
 
        print('Total Row(s):', cursor.rowcount)
        for row in rows:
            room.message(str(row[0]))