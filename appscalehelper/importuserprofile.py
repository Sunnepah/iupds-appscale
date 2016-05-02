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
    print row
    exit(1)

    # data in row:
    # ['user_id', 'name', 'username', 'email','pwd', 'user_type', '0', '0', '18','created_at', 'last_login', '', '\n']

    user_id_old = row[0]
    fullname = row[1]
    username = row[2]
    email = row[3]
    created_at = row[9]

    # check for duplicate
    query = ("SELECT * FROM iupdsmanager_profile WHERE email = '" + email + "' OR username = '" + username + "'")
    cursor.execute(query)
    data = cursor.fetchall()

    if len(data) == 0:

        try:
            if user_client.does_user_exist(email):
                user_client.disable_user(email)
                user_client.delete_user(email)
            else:
                print "User does not exist, proceed "

            # call uaserver to create user
            response = user_client.create_user(email, os.urandom(7))
            if response:
                user_data = user_client.get_user_data(email)
                print user_data
                appscale_user_id = ''

                sql = "INSERT INTO iupdsmanager_profile(uid, user_id_old, email, username, full_name," \
                      " created_at, is_active, admin_type,first_name, last_name, is_admin,updated_at," \
                      "is_cloud_admin, appscale_user_id) " \
                      "VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s')" % \
                      (
                          user_id_old,
                          str(MySQLdb.escape_string(user_id_old)),
                          str(MySQLdb.escape_string(email)),
                          str(MySQLdb.escape_string(username)),
                          str(MySQLdb.escape_string(fullname)),
                          str(MySQLdb.escape_string(created_at)),
                          1, 'RU', '', '', 0, '0000-00-00 00:00:00', 0, appscale_user_id
                      )

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

    exit(1)
# close the connection to the database.
# mydb.commit()
cursor.close()
print "Done"
