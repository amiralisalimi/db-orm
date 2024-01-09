import sys

from peewee import *

from models import *

if __name__ == '__main__':
    database.init('smart-city')

    try:
        command = sys.argv[1]
    except Exception:
        command = ''

    if command.startswith('create'):
        try:
            model = globals()[''.join(s.capitalize() for s in command.removeprefix('create-').split('-'))]
            attrs = sys.argv[2]
            obj = model.create(**eval(f'dict({attrs})'))
            print(f'Created object {obj} successfully')
        except IntegrityError as ie:
            print(ie)
        except Exception:
            print('Invalid command')

    elif command.startswith('delete'):
        try:
            model = globals()[''.join(s.capitalize() for s in command.removeprefix('delete-').split('-'))]
            attrs = sys.argv[2]
            del_cnt = model.delete().where(eval(attrs)).execute()
            print(f'Deleted {del_cnt} rows successfully')
        except IntegrityError as ie:
            print(ie)
        except Exception:
            print('Invalid command')

    elif command.startswith('select'):
        try:
            model = globals()[''.join(s.capitalize() for s in command.removeprefix('select-').split('-'))]
            attrs = sys.argv[2]
            for row in model.select().where(eval(attrs)).namedtuples():
                print(row)
        except IntegrityError as ie:
            print(ie)
        except Exception:
            print('Invalid command')
