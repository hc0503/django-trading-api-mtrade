import psycopg2
import sys
import os
from django.core.management import call_command
from django.contrib.auth import get_user_model
import traceback


def delete_database_content():
    """Deletes all tables from database"""
    print('Deleting tables from database...')

    # connect to database
    try:
        print("Establishing connection with database...")
        conn = psycopg2.connect(user=os.environ['DB_USER'],
                                password=os.environ['DB_PASSWORD'],
                                host=os.environ['DB_HOST'],
                                # port = "5432",
                                database=os.environ['DB_NAME'])
        conn.set_isolation_level(0)

    except:
        print("Unable to connect to the database.")
        return

    # delete all database tables
    try:
        cur = conn.cursor()
        cur.execute("SELECT table_schema,table_name \
                    FROM information_schema.tables \
                    WHERE table_schema = 'public' \
                    ORDER BY table_schema,table_name")
        rows = cur.fetchall()
        for row in rows:
            print("dropping table: ", row[1])
            cur.execute("drop table " + row[1] + " cascade")
    except:
        print("Error: ", sys.exc_info()[1])

    # close connections
    finally:
        if(conn):
            conn.close()
        if (cur):
            cur.close()

        print("PostgreSQL connection is closed")


def migrate_database_schemata():
    """Calls the django migrate command"""
    call_command("migrate", interactive=True)


def create_default_superuser():
    """Creates a default superuser with info provided in environment"""
    User = get_user_model()
    User.objects.create_superuser(os.environ["SUPERUSER_USERNAME"],
                                  os.environ["SUPERUSER_EMAIL"],
                                  os.environ["SUPERUSER_PASSWORD"])
    print("Superuser was successfully created")


def run():
    while(True):
        selected_option = input('\nThe following processes will be executed:\
                                \n1. All database content will be deleted\
                                \n2. A new migration will be performed\
                                \n3. A new  superuser will be created. \
                                \n IMPORTANT NOTE: for superuser to be successfully created, the following variables must be defined in environment:\
                                \n\t SUPERUSER_USERNAME\
                                \n\t SUPERUSER_PASSWORD\
                                \n\t SUPERUSER_EMAIL\
                                \n Else, you will have to manually create your superuser.\
                                \n\n If you want to abort execution press 0 (zero)\
                                press any other key to execute described processes...')

        if (selected_option == '0'):
            print("Database resetting process was interrupted by user.")
            break

        else:
            try:
                delete_database_content()
                migrate_database_schemata()
                create_default_superuser()

                print('SUCCESS')
                break
            except Exception as e:
                traceback.print_exc()
