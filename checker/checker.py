#!/usr/bin/python
from checker_lib import *
from argparse import ArgumentParser
import http.client
import sqlite3
#http.client.HTTPConnection.debuglevel = 1


def log(error_code, status):
    print("%s - %s" % (error_code, status))


# put-get flag to service success
def service_up():
    print("[service is worked] - 101")
    exit(101)


# service is available (available tcp connect) but protocol wrong could not put/get flag
def service_corrupt():
    print("[service is corrupt] - 102")
    exit(102)


# waited time (for example: 5 sec) but service did not have time to reply
def service_mumble():
    print("[service is mumble] - 103")
    exit(103)


# service is not available (maybe blocked port or service is down)
def service_down():
    print("[service is down] - 104")
    exit(104)
    
def initialize_db():
    db = sqlite3.connect("BioGuard.db")
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS checker (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            host TEXT,
            flag_id TEXT,
            flag TEXT,
            username TEXT,
            password TEXT,
            key TEXT,
            message TEXT
        )
        """
    )
    db.commit()
    return db

class Checker():
    vulns: int = 2
    timeout: int = 10
        
    def __enter__(self):
        self.db = initialize_db()
        return self

    def __exit__(self, type, value, traceback):
        self.db.close()

    def __init__(self, host, port):
        # self.host = host
        self.db = initialize_db()
        self.mch = CheckMachine(host=host, port=port, timeout=self.timeout)

    def check(self): 
        #register staff and create service
        with self.mch as c:
            resp = c.get_main_page()
            if resp.status_code != 200: service_corrupt()
            staff = c.generate_staff()
            csrf = resp.cookies['csrftoken']
            staff['csrfmiddlewaretoken'] = resp.cookies['csrftoken']
            if c.register_staff(staff).status_code != 200: service_corrupt()
            
            if (resp := c.login(staff['username'],staff['password1'], csrf)).status_code != 200: service_corrupt()
            # После логина csrf кука обновляется!!!!!!!!!!!!!
            sessionid = resp.cookies['sessionid']
            csrf = resp.cookies['csrftoken']
            service = c.generate_service()
            resp = c.create_service(service, csrf, sessionid)
            if c.create_service(service, csrf, sessionid).status_code != 201: service_corrupt()
            if (resp := c.logout()).status_code != 200: service_corrupt()


        #register patient and create appointment
        # with self.mch as c:
        #     if c.get_main_page().status_code != 200: service_corrupt()
        #     patient = c.generate_patient()
        #     if c.register_patient(patient).status_code != 200: service_corrupt()
        #     if c.login(patient['username'],patient['password']).status_code != 200: service_corrupt()
        #     if c.get_profile().status_code != 200: service_corrupt()
        #     if c.create_appointment().status_code != 200: service_corrupt()
        #     if c.logout().status_code != 200: service_corrupt()


    def put(self, flag_id: str, flag: str, vuln: int):
        with self.mch as c:
                #todo
                staff = CheckMachine.generate_staff()
                resp = c.register_staff(staff)
                if resp.status_code != 200:
                    service_corrupt()
                resp = c.login(staff['username'],staff['password'])
                if resp.status_code != 200:
                    service_corrupt()
                service = CheckMachine.generate_service()
                resp = c.create_service(service)
                resp = c.logout()
                # Я не знаю, что ещё хранить для доступа к флагу, потом добавишь
                cursor = self.db.execute('INSERT INTO checker (host, flag_id, flag, username, password) VALUES (?, ?, ?, ?, ?, ?, ?)', (self.host, flag_id, flag, staff["username"], staff["password1"]))
                self.db.commit()
                cursor.close()
                


    def get(self, flag_id: str, flag: str, vuln: str):
        cursor = self.db.execute('SELECT username, password, key FROM checker WHERE flag=?', ([flag]))
        db_response = cursor.fetchone()
        cursor.close()
        with self.mch as c:
            resp = c.login(db_response[0], db_response[1])
            if resp.status_code != 200:
                service_corrupt()
            #Дальше хз что проверять
            pass



def main():
    pargs = ArgumentParser()
    pargs.add_argument("host")
    pargs.add_argument("command", type=str)
    pargs.add_argument("f_id", nargs='?')
    pargs.add_argument("flag", nargs='?')
    args = pargs.parse_args()
    port = 4444
    url = f"http://{args.host}:{port}"
    with Checker(args.host, port) as c:
        if args.command == "put":
            if not args.flag:
                pargs.error("You need to specify flag with PUT method")
            try:
                c.put(args.f_id, args.flag, 1)
                c.check()
            except requests.Timeout:
                service_mumble()
            # except:
            #     service_down()
            service_up()
        elif args.command == "check":
            try:
                # c.get(args.f_id, args.flag, 1)
                c.check()
            except requests.Timeout:
                service_mumble()
            # except Exception as e:
            #     print(e)
            #     service_down()
            service_up()
        else:
            pargs.error("Wrong command")


if __name__ == "__main__":
    main()