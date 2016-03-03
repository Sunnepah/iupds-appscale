import csv
import MySQLdb
import sys
import logging
import os
from appscale_user_client import AppscaleUserClient

user_client = AppscaleUserClient()

logging.basicConfig(filename='app.log', level=logging.DEBUG)

if len(sys.argv) < 2:
    print('Specify file full path containing data')
    sys.exit(1)

file_path = sys.argv[1]

mydb = MySQLdb.connect(host='localhost',
                       user='root',
                       passwd='secret',
                       db='iupds_db')
cursor = mydb.cursor()

csv_data = csv.reader(open(file_path, 'r'), delimiter=';')

for row in csv_data:
    # user_client.disable_user(row[0])
    # user_client.delete_user(row[0])
    # continue
    # data in row: id, email, username, name
    # check for duplicate
    query = ("SELECT * FROM iupdsmanager_profile WHERE email = '" + row[1] + "' OR username = '" + row[2] + "'")
    cursor.execute(query)
    data = cursor.fetchall()

    if len(data) == 0:

        try:
            if user_client.does_user_exist(row[1]):
                user_client.disable_user(row[1])
                user_client.delete_user(row[1])
            else:
                print "User does not exist, proceed "

            # call uaserver to create user
            response = user_client.create_user(row[1], os.urandom(7))
            if response:
                user_data = user_client.get_user_data(row[1])
                # print user_data
                user_id = ''
                sql = "INSERT INTO iupdsmanager_profile(uid, user_id_old, email, username, full_name," \
                      " created_at, is_active, admin_type) " \
                      "VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (user_id,
                                                                            str(MySQLdb.escape_string(row[0])),
                                                                            str(MySQLdb.escape_string(row[1])),
                                                                            str(MySQLdb.escape_string(row[2])),
                                                                            str(MySQLdb.escape_string(row[3])),
                                                                            str(MySQLdb.escape_string(row[4])),
                                                                            1, 'RU')
                # Execute the SQL command
                cursor.execute(sql)
                # Commit your changes in the database
                mydb.commit()
            else:
                print 'Unable to create user on Appscale'
                logging.error('Unable to create user on Appscale')
                logging.error(response)
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print "Mysql Error, check log for details"
            logging.info('=============== Mysql Error ============')
            logging.info(sql)
            logging.error(e)
            # Rollback in case there is any error
            mydb.rollback()

    else:
        print 'Possible duplicate, unable to save'
        logging.info("================= Duplicate =================")
        logging.info(data)
# close the connection to the database.
# mydb.commit()
cursor.close()
print "Done"
