import csv
import MySQLdb
import sys
import logging
import os
from appscale_user_client import AppscaleUserClient

import time

start_time = time.time()

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
    print row
    logging.debug(row)

    # data in row:
    # ['user_id', 'name', 'username', 'email','pwd', 'user_type', '0', '0', '18','created_at', 'last_login', '', '\n']

    user_id_old = str(row[0])
    fullname = str(row[1]).upper().decode('utf-8').upper().encode('utf-8')
    username = str(row[2])
    email = str(row[3])
    created_at = str(row[9])

    # check for duplicate
    query = ("SELECT * FROM iupdsmanager_profile WHERE email = '" + email + "' OR username = '" + username + "'")
    cursor.execute(query)
    data = cursor.fetchall()

    sql = ""
    if len(data) == 0:

        try:
            if user_client.does_user_exist(email):
                user_client.disable_user(email)
                user_client.delete_user(email)
            else:
                print "User does not exist, proceed "
                logging.info("User does not exist, proceed ")

            # call uaserver to create user
            start = time.time()
            # response = user_client.create_user(email, os.urandom(7))
            response = user_client.create_user(email, "1234567")

            if response:
                round_trip = time.time() - start
                writer = csv.writer(open("appscale_create_user_response_time_output.csv", 'a'), delimiter=';')
                writer.writerow([round_trip, ''])

                user_data = user_client.get_user_data(email)

                sql = "INSERT INTO iupdsmanager_profile(uid, user_id_old, email, username, full_name," \
                      " created_at, is_active, admin_type,first_name, last_name, is_admin,updated_at," \
                      "is_cloud_admin, appscale_user_id) " \
                      "VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s')" % \
                      (
                          user_id_old,
                          MySQLdb.escape_string(user_id_old),
                          MySQLdb.escape_string(email),
                          MySQLdb.escape_string(username),
                          MySQLdb.escape_string(fullname),
                          MySQLdb.escape_string(created_at),
                          1, 'RU', '', '', 0, '0000-00-00 00:00:00', 0, email
                      )

                # print sql
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
            logging.info('=============== Mysql Error ============ ' + email)
            logging.info(sql)
            logging.error(e)
            # Rollback in case there is any error
            mydb.rollback()
        except AttributeError as e:
            print e.message

    else:
        print 'Possible duplicate, unable to save'
        logging.info("================= Duplicate =================")
        logging.info(data)

    logging.debug("+++++ Processed "+email+" ++++++++++")
    time.sleep(15)

# close the connection to the database.
cursor.close()

print("--- %s seconds ---" % (time.time() - start_time))
print "Done"
