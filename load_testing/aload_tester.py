import asyncio
import sys
import time
import traceback
import os


sys.path.append(os.getcwd())


from magical.items import Item
from magical.users import User


async def start_session(user,i,arguments):
    try:
        str_out = ""
        start_create_acc = time.time()
        await user.ahttp.createAccount()
        elapsed_create_acc = time.time() - start_create_acc
        str_out += "create account:%.2f"%elapsed_create_acc
        elapsed_login = 0
        elapsed_add_item = 0
        if arguments['login_flag']:
            start_login = time.time()
            await user.ahttp.login()
            elapsed_login = time.time() - start_login
            str_out += ", login:%.2f" % elapsed_login
        if arguments['add_item_flag']:
            start_add_item = time.time()
            await user.ahttp.addItem(Item())
            elapsed_add_item = time.time() - start_add_item
            str_out += ", add item:%.2f" % elapsed_add_item
        await user.ahttp.session.close()
        print("user %i finished in %.2f [%s] "%(i, (elapsed_login + elapsed_create_acc),str_out))
        return elapsed_login + elapsed_create_acc
    except Exception as e:
        tb = traceback.format_exc()
        print ("user %s failed: %s"%(i,tb))
        await user.ahttp.session.close()
        return 0

async def main(arguments):
    users = [User() for i in range(arguments['nrequests'])]
    sessions = []
    for i in range(len(users)):
        sessions.append(start_session(users[i],i,arguments))
    start = time.time()
    results = await asyncio.gather(*sessions)
    total = time.time() - start
    print(".......Summary.......")
    nsucceeded = 0
    for result in results:
        if result:
            nsucceeded +=1
    nfailed = len(results) - nsucceeded
    print("total time was %.2f"%total)
    print("%s failed, %s succeeded"%(nfailed, nsucceeded))
    average = sum(results)/len(results)
    print("average time was %.2f"%average)

def parse_command_line_arguments():
    arguments = {}
    arguments['nrequests'] = 0
    arguments['login_flag'] = False
    arguments['add_item_flag'] = False

    if not (1 < len(sys.argv) < 5):
        sys.exit("usage: %s nrequests [-l] [-i] " % (sys.argv[0]))
    try:
        arguments['nrequests'] = int(sys.argv[1])
    except:
        sys.exit("Error: the first argument must be the number of requests. '%s' is not a number." % sys.argv[1])
    try:
        flag_1 = sys.argv[2]
        check_command_line_flags(flag_1, arguments)
        flag_2 = sys.argv[3]
        check_command_line_flags(flag_2, arguments)
    except IndexError:
        pass
    return arguments

def check_command_line_flags(flag, arguments):
    if flag == '-i':
        arguments['add_item_flag'] = True
    elif flag == '-l':
        arguments['login_flag'] = True
    else:
        sys.exit("'%s' is an invalid argument." % flag)


if __name__ == "__main__":
    arguments = parse_command_line_arguments()
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(main(arguments))
    loop.run_until_complete(future)
    '''
    time.sleep(5)
    users = [User() for i in range(arguments['nrequests'])]
    start = time.time()
    for user in users:
        print(user.http.createAccount())
    for user in users:
        print(user.http.login())
    print(time.time() - start)
    '''