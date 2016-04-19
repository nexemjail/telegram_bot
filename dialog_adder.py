from python_bot import *


dialog_id = 'a103aed4-1141-42da-a618-889f6b634682'


if __name__ == '__main__':
    dialog = DialogV1(username=dialog_credinitials['username'], password=dialog_credinitials['password'])
    for f in dialog.get_dialogs()['dialogs']:
        print f

    response = dialog.create_dialog(open('ex1_my.xml','r'), 'test_planets_dialog')
    print response