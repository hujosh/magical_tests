import asyncio
import concurrent.futures
import multiprocessing
import sys
import time
from multiprocessing.dummy import Pool

from magical.items import Item
from magical.users import User


def parse_command_line_arguments():
    arguments = {}
    arguments['nrequests'] = 0
    arguments['login_flag'] = False
    arguments['add_item_flag'] = False

    if not(1 < len(sys.argv) < 5):
        sys.exit("usage: %s nrequests [-l] [-i] "%(sys.argv[0]))
    try:
        arguments['nrequests'] = int(sys.argv[1])
    except:
        sys.exit("Error: the first argument must be the number of requests. '%s' is not a number."%sys.argv[1])
    try:
        flag_1 = sys.argv[2]
        check_command_line_flags(flag_1, arguments)
        flag_2 = sys.argv[3]
        check_command_line_flags(flag_2, arguments)
    except IndexError:
        pass
    return arguments
     
def check_command_line_flags(flag,arguments):
    if flag == '-i':
        arguments['add_item_flag'] = True
    elif flag == '-l':
        arguments['login_flag'] = True
    else:
        sys.exit("'%s' is an invalid argument."%flag)

def get_users(nrequests):
    return [User() for i in range(nrequests)]
                
def create_account(user):
    print( user.http.createAccount())
    
def login(user):
    return user.http.login()
    
def add_item(user):
    item = Item()
    return user.http.addItem(item)

def create_accounts_concurrently(users):
    print("Sending create account requests...")
    p = Pool(min(len(users), 5*multiprocessing.cpu_count()))
    start = time.time()
    for response in p.imap_unordered(create_account, users):
        print("{} (Time elapsed: {}s)".format(response, int(time.time() - start)))
    
def login_concurrently(users):
    print("Sending login requests...")
    p = Pool(len(users))
    start = time.time()
    for response in p.imap_unordered(login, users):
        print("{} (Time elapsed: {}s)".format(response, int(time.time() - start)))
    
def add_items_concurrently(users):
    print("Sending add item requests...")
    p = Pool(len(users))
    start = time.time()
    for response in p.imap_unordered(add_item, users):
        print("{} (Time elapsed: {}s)".format(response, int(time.time() - start)))
    
async def main(users):
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        loop  = asyncio.get_event_loop()
        futures = [loop.run_in_executor(executor,create_account, user) for user in users]
    
    
if __name__ == "__main__":
    arguments = parse_command_line_arguments()
    loop = asyncio.get_event_loop()
    users = get_users(arguments['nrequests'])
    loop.run_until_complete(main(users))

    
    
    
   
    
    