#!/usr/bin/env python
# Author: Hibathul Careem
# Version1.1 - Generates the vpn configuration for Cloud and Hosted Customers



while True:

    CUSTOMER_TYPE = input("Is your Customer Hosted OR Cloud? (H / C): ")

    if CUSTOMER_TYPE.upper() == 'C' or CUSTOMER_TYPE.upper() == 'H':
        break

while True:
    CUSTOMER_REGION = input("Whats is the Region (US/EU) : ")

    if CUSTOMER_REGION.upper() == 'US' or CUSTOMER_REGION.upper() == 'EU':
        break


CUSTOMER_NAME = input ("What is CUSTOMER_NAME: " )
CUSTOMER_VPN_IP = input ("What is CUSTOMER_VPN_IP: " )
PRE_SHARED_KEY = input ("What is PRE_SHARED_KEY: ")
IKE_PROPOSALS = input ("What is IKE_PROPOSAL (psk_dh2_aes256-sha1_p1) : " )
IPSEC_PROPOSALS = input ("What is IPSEC_PROPOSAL (esp_aes256_sha1_3600_p2) : ")
INTERFACE = input ("What is INTERFACE: " )
CUSTOMER_IPS = input ("What are CUSTOMER_IPS: " )
PROXY_REMOTE_IDENTITY = input ("What is PROXY_REMOTE_IDENTITY: " )
CUSTOMER_NAT_POOL = input ("What is CUSTOMER_NAT_POOL: " )
CUSTOMER_NAT_IPS = input   ("What are CUSTOMER_NAT_IPS: " )


if CUSTOMER_TYPE.upper() == "H":

    WEB_INSTANCES_IP =  input ("What are the WEB_INSTANCES_IPS: ")

print ( '.'*20 + "All variables you have entered are like below " + '.'*20)
print ("CUSTOMER_TYPE: ", CUSTOMER_TYPE.upper())
print ("CUSTOMER_NAME: ", CUSTOMER_NAME)

print ("CUSTOMER_VPN_IP: ",CUSTOMER_VPN_IP)
print ("PRE_SHARED_KEY: " ,PRE_SHARED_KEY)    
print ("IKE_PROPOSALS: ",IKE_PROPOSALS)    
print ("IPSEC_PROPOSALS: ",IPSEC_PROPOSALS)    
print ("INTERFACE: ",INTERFACE)
print ("CUSTOMER_IPS: ",CUSTOMER_IPS)     
print ("PROXY_REMOTE_IDENTITY: ",PROXY_REMOTE_IDENTITY)           
print ("CUSTOMER_NAT_POOL: ",CUSTOMER_NAT_POOL)      
print ("CUSTOMER_NAT_IPS: ",CUSTOMER_NAT_IPS)    

if CUSTOMER_TYPE.upper() == "H":
    print ('WEB_INSTANCES_IP: ', WEB_INSTANCES_IP)

gen_dict = {}

def gen_config():

     #defining ike phase1 config
    r1 = ( "set security ike policy {0} mode main").format(CUSTOMER_NAME)
    r2 = ( "set security ike policy {0} proposals {1}").format(CUSTOMER_NAME,IKE_PROPOSALS)
    r3 = ( "set security ike policy {0} pre-shared-key ascii-text {1}").format(CUSTOMER_NAME,PRE_SHARED_KEY)
    r4 = ( "set security ike gateway {0} ike-policy {0}").format(CUSTOMER_NAME) 
    r5 = ( "set security ike gateway {0} address {1}").format(CUSTOMER_NAME,CUSTOMER_VPN_IP)
    r6 = ( "set security ike gateway {0} external-interface ge-0/0/1.0").format(CUSTOMER_NAME)
        
    # defining ipsec phase2 config
    r8  = ( "set security ipsec policy {0} proposals {1}").format(CUSTOMER_NAME,IPSEC_PROPOSALS)
    r9  = ( "set security ipsec vpn {0} bind-interface st0.{1}").format(CUSTOMER_NAME,INTERFACE)
    r10 = ( "set security ipsec vpn {0} ike gateway {0}").format(CUSTOMER_NAME)
       
    r12 = ( "set security ipsec vpn {0} ike proxy-identity remote {1}").format(CUSTOMER_NAME,PROXY_REMOTE_IDENTITY)
    r13 = ( "set security ipsec vpn {0} ike ipsec-policy {0}").format(CUSTOMER_NAME)
    
    
    gen_dict.update({'a11': r1})
    gen_dict.update({'a12': r2})
    gen_dict.update({'a13': r3})
    gen_dict.update({'a14': r4})
    gen_dict.update({'a15': r5})
    gen_dict.update({'a16': r6})

    gen_dict.update({'a18': r8})
    gen_dict.update({'a19': r9})
    gen_dict.update({'a20': r10})

    gen_dict.update({'a22' : r12})
    gen_dict.update({'a23' : r13})
    
 
    customer_ips = CUSTOMER_IPS.split()

    #defining address book - customer internal ip 
    count =  10
    for ip in customer_ips:
        count += 1
        r15 = ( "set security address-book global address {0}-farend_{1} {1}/32").format(CUSTOMER_NAME,ip)
        gen_dict.update({'b'+ str(count): r15})

    count =  10
    for ip in customer_ips:
        count += 1
        r16 = ( "set security address-book global address-set {0}_remote_nodes address {0}-farend_{1}").format(CUSTOMER_NAME,ip)
        gen_dict.update({'c'+ str(count): r16})
    

    if CUSTOMER_TYPE.upper() == "H":
        count =  10
        for web_ip in WEB_INSTANCES_IP.split():
            count += 1
            r17 = ("set security address-book global address {0}-local_{1} {1}/32").format(CUSTOMER_NAME,web_ip)
            gen_dict.update({'d' + str(count): r17})
        count =  10  
        for web_ip in WEB_INSTANCES_IP.split():
            count += 1
            r18 = ("set security address-book global address-set {0}_local_nodes address {0}-local_{1}").format(CUSTOMER_NAME,web_ip)
            gen_dict.update({'e' + str(count): r18})
    
    #defining destination nat pool
    counter = 0
    count =  10
    for ip in customer_ips:
        counter += 1
        count += 2
        r19 = ("set security nat destination pool {0}-far-end-dst-{1} address {2}/32").format(CUSTOMER_NAME,counter,ip)
        gen_dict.update({'f' + str(count): r19})
        r20 = ("set security nat destination pool {0}-far-end-dst-{1} address to {2}/32").format(CUSTOMER_NAME,counter,ip)
        gen_dict.update({'f' + str(count+1): r20})
    

    if CUSTOMER_TYPE.upper() == "H":
        count =  10 
        for web_ip in WEB_INSTANCES_IP.split():
            count += 1
            r21 = ("set security nat source rule-set src-nat-toward-customer rule {0}-s2 match source-address {1}/32").format(CUSTOMER_NAME,web_ip)
            gen_dict.update({'g' + str(count): r21})
    
        r22 = ("set security nat source rule-set src-nat-toward-customer rule {0}-s2 then source-nat pool cvpn-out-natted-src-2").format(CUSTOMER_NAME)
        gen_dict.update({'h10' : r22})
    
    #defining natting rules
    counter = 0 
    count =  10
    for ip in CUSTOMER_NAT_IPS.split():
        counter += 1
        count += 2
        r23 = ("set security nat destination rule-set dst-nat-toward-customer rule {0}-d{1} match destination-address {2}/32").format(CUSTOMER_NAME,counter,ip)
        gen_dict.update({'i' + str(count): r23})
        r24 = ("set security nat destination rule-set dst-nat-toward-customer rule {0}-d{1} then destination-nat pool {0}-far-end-dst-{1}").format(CUSTOMER_NAME,counter)
        gen_dict.update({'i' + str(count+1): r24})
    
    #defining firewall policies
    if CUSTOMER_TYPE.upper() == "H":
        r25 = ("set security policies from-zone trust to-zone custvpn policy permit_{0}_outbound match source-address {0}_local_nodes").format(CUSTOMER_NAME)
        gen_dict.update({'j10' :r25})
    elif  CUSTOMER_TYPE.upper() == "C":
        if CUSTOMER_REGION.upper() == "US":
            r25 = ("set security policies from-zone trust to-zone custvpn policy permit_{0}_outbound match source-address ms-prod-jcx/10.125.112.0_20").format(CUSTOMER_NAME)
            gen_dict.update({'j10' :r25})
        elif CUSTOMER_REGION.upper() == "EU":
            r25 = ("set security policies from-zone trust to-zone custvpn policy permit_{0}_outbound match source-address ms-prod-jcx-2_10.124.32.0/20").format(CUSTOMER_NAME)
            gen_dict.update({'j10' :r25})
    
    r26 = ("set security policies from-zone trust to-zone custvpn policy permit_{0}_outbound match destination-address {0}_remote_nodes").format(CUSTOMER_NAME)
    r27 = ("set security policies from-zone trust to-zone custvpn policy permit_{0}_outbound match application junos-icmp-all").format(CUSTOMER_NAME)
    r28 = ("set security policies from-zone trust to-zone custvpn policy permit_{0}_outbound match application sldap_636").format(CUSTOMER_NAME)
    r29 = ("set security policies from-zone trust to-zone custvpn policy permit_{0}_outbound match application junos-ldap").format(CUSTOMER_NAME)
    r30 = ("set security policies from-zone trust to-zone custvpn policy permit_{0}_outbound match application msft-gc-ssl_3268").format(CUSTOMER_NAME)
    r31 = ("set security policies from-zone trust to-zone custvpn policy permit_{0}_outbound match application msft-gc-ssl_3269").format(CUSTOMER_NAME)
    r32 = ("set security policies from-zone trust to-zone custvpn policy permit_{0}_outbound match application junos-http").format(CUSTOMER_NAME)
    r33 = ("set security policies from-zone trust to-zone custvpn policy permit_{0}_outbound match application junos-https").format(CUSTOMER_NAME)
    
    #defining interface
    r34 = ("set interfaces st0 unit {1} description {0}").format(CUSTOMER_NAME,INTERFACE)
    r35 = ("set interfaces st0 unit {0} family inet").format(INTERFACE)

    r36 = ("set firewall family inet filter fbf-filter term {0} from destination-address {1}").format(CUSTOMER_NAME,CUSTOMER_NAT_POOL)
    r37 = ("set firewall family inet filter fbf-filter term {0} then count fbf{1}").format(CUSTOMER_NAME,INTERFACE)
    r38 = ("set firewall family inet filter fbf-filter term {0} then routing-instance fbf{1}").format(CUSTOMER_NAME,INTERFACE)
    
    # configuring the rib groups 
    r39 = ("set routing-options rib-groups fbf-group import-rib fbf{0}.inet.0").format(INTERFACE)
    r40 = ("set policy-options policy-statement redist-fbf{0} term 100 from instance fbf{0}").format(INTERFACE)
    r41 = ("set policy-options policy-statement redist-fbf{0} term 100 from protocol static").format(INTERFACE)
    r42 = ("set policy-options policy-statement redist-fbf{0} term 100 then next term").format(INTERFACE)
    r43 = ("set policy-options policy-statement redist-fbf{0} term 101 from route-filter 0.0.0.0/0 exact reject").format(INTERFACE)
    r44 = ("set routing-options instance-import redist-fbf{0}").format(INTERFACE)
    r45 = ("set routing-instances fbf{0} instance-type forwarding").format(INTERFACE)
    r46 = ("set routing-instances fbf{0} routing-options static route 0.0.0.0/0 next-hop st0.{0}").format(INTERFACE)
    r47 = ("set routing-instances fbf{0} routing-options static route {1} next-hop st0.{0}").format(INTERFACE,CUSTOMER_NAT_POOL)
    
     
    
    gen_dict.update({'k10' :r26})
    gen_dict.update({'k11' :r27})
    gen_dict.update({'k12' :r28})
    gen_dict.update({'k13' :r29})
    gen_dict.update({'k14' :r30})
    gen_dict.update({'k15' :r31})
    gen_dict.update({'k16' :r32})
    gen_dict.update({'k17' :r33})
    gen_dict.update({'k18' :r34})
    gen_dict.update({'k19' :r35})
    gen_dict.update({'k20' :r36})
    gen_dict.update({'k21' :r37})
    gen_dict.update({'k22' :r38})
    gen_dict.update({'k23' :r39})
    gen_dict.update({'k24' :r40})
    gen_dict.update({'k25' :r41})
    gen_dict.update({'k26' :r42})
    gen_dict.update({'k27' :r43})
    gen_dict.update({'k28' :r44})
    gen_dict.update({'k29' :r45})
    gen_dict.update({'k30' :r46})
    gen_dict.update({'k31' :r47})
   

def pri_config():

    r14 = ( "set security ipsec vpn {0} establish-tunnels immediately").format(CUSTOMER_NAME)
    gen_dict.update({'a24' : r14})
    
    if CUSTOMER_REGION.upper() == "US":
        r7 = ( "set security ike gateway {0} local-identity inet 35.174.181.188").format(CUSTOMER_NAME)
        gen_dict.update({'a17': r7})
    
    elif CUSTOMER_REGION.upper() == "EU":
        r7 = ( "set security ike gateway {0} local-identity inet 3.120.125.254").format(CUSTOMER_NAME)
        gen_dict.update({'a17': r7})

    if CUSTOMER_REGION.upper() == "US":
        r11 = ( "set security ipsec vpn {0} ike proxy-identity local 204.93.64.96/28").format(CUSTOMER_NAME)
        gen_dict.update({'a21' :r11})
    
    elif CUSTOMER_REGION.upper() == "EU":
        r11 = ( "set security ipsec vpn {0} ike proxy-identity local 204.93.80.96/28").format(CUSTOMER_NAME)
        gen_dict.update({'a21' :r11})

    

def back_config():

    if CUSTOMER_REGION.upper() == "US":
        r7 = ( "set security ike gateway {0} local-identity inet 34.203.130.199").format(CUSTOMER_NAME)
        gen_dict.update({'a17': r7})
    elif CUSTOMER_REGION.upper() == "EU":
        r7 = ( "set security ike gateway {0} local-identity inet 35.156.27.106").format(CUSTOMER_NAME)
        gen_dict.update({'a17': r7})

    if CUSTOMER_REGION.upper() == "US":
        r11 = ( "set security ipsec vpn {0} ike proxy-identity local 204.93.64.112/28").format(CUSTOMER_NAME)
        gen_dict.update({'a21' :r11})
    elif CUSTOMER_REGION.upper() == "EU":
        r11 = ( "set security ipsec vpn {0} ike proxy-identity local 204.93.80.112/28").format(CUSTOMER_NAME)
        gen_dict.update({'a21' :r11})

  


CHOICE = input("Do you want to generate the config for Vsrx-1 (y/n):")

if CHOICE.upper() == 'Y':
    gen_config()
    pri_config()
    sort_dic = sorted(gen_dict.items())
    
    for line in sort_dic:
       print(line[1])
    Backup_CHOICE = input("Do you want to generate the config for Vsrx-2 (y/n):")
    if Backup_CHOICE.upper() == 'Y':
        gen_dict.clear()
        gen_config()
        back_config()
        sort_dic = sorted(gen_dict.items())
        for line in sort_dic:
           print(line[1])

    elif Backup_CHOICE.upper() == 'N':
        SystemExit()

elif CHOICE.upper() == 'N':
    SystemExit()

  


