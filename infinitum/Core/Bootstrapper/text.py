_welcome_screen1 = 'Welcome'
_welcome_screen2 = \
'''Welcome to the Infinitum installer

This installer will guide you through the process of setting up an Encrypted Virtual Disk for Infinitum on your computer.

Please be aware that this software is released under the Unlicense, which means that it is provided "as is" without any warranties or conditions of any kind. You are free to use, modify, and distribute the software as you see fit, but we cannot be held responsible for any issues that may arise from its use.

With that said, we hope you find the software useful and we encourage you to fork the project if you have any improvements or enhancements to share at https://github.com/KThankYou/Infinitum.
'''

_user_details1 = 'User Information'
_user_details2 = '''\
Please select a username and password for your device. 
The Username must be atleast 1 character long, the password must be at least 8 characters long and include at least one uppercase letter, one lowercase letter, one number, and one special character. Spaces are not allowed in the password. 
Note that the password cannot be changed once it has been created, and it is used to encrypt all data stored on your device. If you lose your password, there is no way to recover your data.
'''

_installation1 = 'Confirmation'
_installation2 = '''A drive for Infinitum encrypted with the password provided just now will be created in the cwd and will be named 'Infinitum.vc'. If you delete/move this file you can create a new drive of infinitum.'''
_installation3 = 'Once again if you forget the password you will not be able to recover the data stored.'
_installation4 = 'Press Next to continue'

_installation_alt1 = 'Error'
_installation_alt2 = '''Invalid Username or Password, press Next or Back to go back and try again or Cancel to quit the setup'''

_install_success1 = 'Installation Sucessful'
_install_success2 = '''\

Infinitum.vc has been successfully created. Please restart Infinitum to boot into the App.

Press finish or cancel to quit.
'''

_install_fail1 = 'Installation Failed'
_install_fail2 = '''\
Infinitum.vc has NOT been successfully created due to the Error:

{}

Please restart Infinitum and try again.

Press finish or cancel to quit.
'''

welcome = (('Header2', _welcome_screen1), ('Text1', _welcome_screen2))
user_details = (('Header6', _user_details1), ('Text1', _user_details2) )
installation = (('Header6', _installation1), ('Text1', _installation2), ('Text2', _installation3), ('Text1', _installation4))
installation_alt = (('Header6', _installation_alt1), ('Text1', _installation_alt2))
install_success = (('Header6', _install_success1), ('Text1', _install_success2))
install_fail = (('Header6', _install_fail1), ('Text1', _install_fail2))