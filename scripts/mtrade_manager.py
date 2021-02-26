from scripts.db_content_manager import reset_db, populate_db
import traceback


def run():
    print('\n-----------WELCOME TO MTRADE MANAGER-----------')

    selected_option = -1
    while(selected_option != '0'):
        selected_option = input('\
            \n---MAIN MENU---\
            \nSelect an option: \
            \n1. Empty database content and create default superuser \
            \n2. Generate database content \
            \n0. EXIT\n')

        try:
            if (selected_option == "1"):
                reset_db.run()
                continue

            if (selected_option == "2"):
                populate_db.run()
                continue

            elif (selected_option != '0'):
                print(f"I don't know what to do with {selected_option}")

        except Exception as e:
            traceback.print_exc()
            print('Problem in mtrade manager')

    print('--------- BYE! -----------------')
