_welcome_screen1 = 'Welcome'
_welcome_screen2 = \
'''Welcome to the Infinitum installer

This installer will guide you through the process of setting up an Encrypted Virtual Disk for Infinitum on your computer.

Please be aware that this software is released under the Unlicense, which means that it is provided "as is" without any warranties or conditions of any kind. You are free to use, modify, and distribute the software as you see fit, but we cannot be held responsible for any issues that may arise from its use.

With that said, we hope you find the software useful and we encourage you to fork the project if you have any improvements or enhancements to share at https://github.com/KThankYou/Infinitum.

This was made as a college project for our first sem in VIT Chennai by .........
'''

_user_details1 = 'User Information'

_user_details2 = '''\
Please select a username and password for your device. There is no requirement for the username, but the password must be at least 12 characters long and include at least one uppercase letter, one lowercase letter, one number, and one special character. Note that the password cannot be changed once it has been created, and it is used to encrypt all data stored on your device. If you lose your password, there is no way to recover your data.
'''


welcome = (('Header2', _welcome_screen1), ('Text1', _welcome_screen2))
user_details = (('Header6', _user_details1), ('Text1', _user_details2) )