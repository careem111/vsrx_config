from pyautogui import typewrite

CUSTOMER_TYPE = input ("Is your Customer Hosted OR Cloud? Press H or C: ")

CUSTOMER_REGION = input("Whats is the Region (US/EU) : ")
VSRX_TYPE = input('Whats the VSRX type (Primary-1/Standby-2 : ')

CUSTOMER_NAME = input ("What is CUSTOMER_NAME:" "change_name " )
CUSTOMER_VPN_IP = input ("What is CUSTOMER_VPN_IP:" "54.x.x.x " )
PRE_SHARED_KEY = input ("What is PRE_SHARED_KEY:"  "..... " )
IKE_PROPOSALS = input ("What is IKE_PROPOSAL:" "psk_dh2_aes256-sha1_p1 " )
IPSEC_PROPOSALS = input ("What is IPSEC_PROPOSAL:" "esp_aes256_sha1_3600_p2 ")
INTERFACE = input ("What is INTERFACE:"  "xx " )
CUSTOMER_IPS = input ("What are CUSTOMER_IPS:" "10.x.x.1 10.x.x.2 ... " )
PROXY_REMOTE_IDENTITY = input ("What is PROXY_REMOTE_IDENTITY:"  "10.x.x.0/24 " )
CUSTOMER_NAT_POOL = input ("What is CUSTOMER_NAT_POOL:"  "10.201.x.0/20 " )
CUSTOMER_NAT_IPS = input   ("What are CUSTOMER_NAT_IPS:"  "10.160.x.x 10.160.x.x ... " )

#REGION_SUBNET = input ("What is REGION_SUBNET:"  "10.125.112.0/20 " )
#FW_SOURCE_ADDR = input ("What is FW_SOURCE_ADDR:"  "ms-prod-jcx/10.125.112.0_20 " )

#PROXY_LOCAL_IDENTITY = input ("What is PROXY_LOCAL_IDENTITY:"  "204.93.64.96/28 " )

if CUSTOMER_TYPE.upper() == "H":

    WEB_INSTANCES_IP =  input ("What are the WEB_INSTANCES_IPS?:"  "10.x.x.1 10.x.x.2 ... ")



#defining ike phase1 config
r1 = ( "set security ike policy {0} mode main").format(CUSTOMER_NAME)
r2 = ( "set security ike policy {0} proposals {1}").format(CUSTOMER_NAME,IKE_PROPOSALS)
r3 = ( "set security ike policy {0} pre-shared-key ascii-text {1}").format(CUSTOMER_NAME,PRE_SHARED_KEY)
r4 = ( "set security ike gateway {0} ike-policy {0}").format(CUSTOMER_NAME) 
r5 = ( "set security ike gateway {0} address {1}").format(CUSTOMER_NAME,CUSTOMER_VPN_IP)
r6 = ( "set security ike gateway {0} external-interface ge-0/0/1.0").format(CUSTOMER_NAME)


print(r1)
print(r2)
print(r3)
print(r4)
print(r5)
print(r6)

if CUSTOMER_REGION.upper() == "US" and VSRX_TYPE == 1:
    r7 = ( "set security ike gateway {} local-identity inet 35.174.181.188").format(CUSTOMER_NAME)
    print(r7)
elif CUSTOMER_REGION.upper() == "US" and VSRX_TYPE == 2:
    r7 = ( "set security ike gateway {} local-identity inet 34.203.130.199").format(CUSTOMER_NAME)
    print(r7)
elif CUSTOMER_REGION.upper() == "EU" and VSRX_TYPE == 1:
    r7 = ( "set security ike gateway {} local-identity inet 3.120.125.254").format(CUSTOMER_NAME)
    print(r7)
elif CUSTOMER_REGION.upper() == "EU" and VSRX_TYPE == "2":
    r7 = ( "set security ike gateway {} local-identity inet 35.156.27.106").format(CUSTOMER_NAME)
    print(r7)


# defining ipsec phase2 config
r8  = ( "set security ipsec policy {0} proposals {1}").format(CUSTOMER_NAME,IPSEC_PROPOSALS)
r9  = ( "set security ipsec vpn {0} bind-interface st0.{1}").format(CUSTOMER_NAME,INTERFACE)
r10 = ( "set security ipsec vpn {0} ike gateway {0}").format(CUSTOMER_NAME)

print(r8)
print(r9)
print(r10)

if CUSTOMER_REGION.upper() == "US" and VSRX_TYPE == 1:
    r11 = ( "set security ipsec vpn {0} ike proxy-identity local 204.93.64.96/28").format(CUSTOMER_NAME)
    print(r11)
elif CUSTOMER_REGION.upper() == "US" and VSRX_TYPE == 2:
    r11 = ( "set security ipsec vpn {0} ike proxy-identity local 204.93.64.112/28").format(CUSTOMER_NAME)
    print(r11)
elif CUSTOMER_REGION.upper() == "EU" and VSRX_TYPE == 1:
    r11 = ( "set security ipsec vpn {0} ike proxy-identity local 204.93.80.96/28").format(CUSTOMER_NAME)
    print(r11)
elif CUSTOMER_REGION.upper() == "EU" and VSRX_TYPE == 2:
    r11 = ( "set security ipsec vpn {0} ike proxy-identity local 204.93.80.112/28").format(CUSTOMER_NAME)
    print(r11)


r12 = ( "set security ipsec vpn {0} ike proxy-identity remote {1}").format(CUSTOMER_NAME,PROXY_REMOTE_IDENTITY)
r13 = ( "set security ipsec vpn {0} ike ipsec-policy {0}").format(CUSTOMER_NAME)
r14 = ( "set security ipsec vpn {0} establish-tunnels immediately").format(CUSTOMER_NAME)


print(r12)
print(r13)
print(r14)

#defining address book - customer internal ip 
for ip in CUSTOMER_IPS.split():

    r15 = ( "set security address-book global address {0}-farend_{1} {1}/32").format(CUSTOMER_NAME,ip)
    print(r15)

for ip in CUSTOMER_IPS.split():
    r16 = ( "set security address-book global address-set {0}_remote_nodes address {0}-farend_{1}").format(CUSTOMER_NAME,ip)
    print(r16)

if CUSTOMER_TYPE.upper() == "H":

    for web_ip in WEB_INSTANCES_IP.split():

        r17 = ("set security address-book global address {0}-local_{1} {1}/32").format(CUSTOMER_NAME,web_ip)
        print(r17)
        
    for web_ip in WEB_INSTANCES_IP.split():

        r18 = ("set security address-book global address-set {0}_local_nodes address {0}-local_{1}").format(CUSTOMER_NAME,web_ip)
        print(r18)

#defining destination nat pool
counter = 0
for ip in CUSTOMER_IPS.split():
    counter += 1
    r19 = ("set security nat destination pool {0}-far-end-dst-{1} address {2}/32").format(CUSTOMER_NAME,counter,ip)
    print(r19)
    r20 = ("set security nat destination pool {0}-far-end-dst-{1} address to {2}/32").format(CUSTOMER_NAME,counter,ip)
    print(r20)

if CUSTOMER_TYPE.upper() == "H":
    for web_ip in WEB_INSTANCES_IP.split():

        r21 =  ("set security nat source rule-set src-nat-toward-customer rule {0}-s2 match source-address {1}/32").format(CUSTOMER_NAME,web_ip)
        print(r21)

    r22 =  ("set ecurity nat source rule-set src-nat-toward-customer rule {0}-s2 then source-nat pool cvpn-out-natted-src-2").format(CUSTOMER_NAME)
    print(r22)

#defining natting rules
counter = 0 
for ip in CUSTOMER_NAT_IPS.split():
    counter += 1
    r23 =  ("set security nat destination rule-set dst-nat-toward-customer rule {0}-d{1} match destination-address {2}/32").format(CUSTOMER_NAME,counter,ip)
    print(r23)
    r24 =  ("set security nat destination rule-set dst-nat-toward-customer rule {0}-d{1} then destination-nat pool {0}-far-end-dst-{1}").format(CUSTOMER_NAME,counter)
    print(r24)

#defining firewall policies
if CUSTOMER_TYPE.upper() == "H":

    r25 = ("set security policies from-zone trust to-zone custvpn policy permit_{0}_outbound match source-address ${0}_local_nodes").format(CUSTOMER_NAME)
    print(r25)
elif  CUSTOMER_TYPE.upper() == "C":
    if CUSTOMER_REGION.upper() == "US":
        r25 =  ("set security policies from-zone trust to-zone custvpn policy permit_{0}_outbound match source-address ms-prod-jcx/10.125.112.0_20").format(CUSTOMER_NAME)
        print(r25)
    elif CUSTOMER_REGION.upper() == "EU":
        r25 =  ("set security policies from-zone trust to-zone custvpn policy permit_{0}_outbound match source-address ms-prod-jcx-2_10.124.32.0/20").format(CUSTOMER_NAME)
        print(r25)

r26 = ("set security policies from-zone trust to-zone custvpn policy permit_{0}_outbound match destination-address {0}_remote_nodes").format(CUSTOMER_NAME)
r27 = ("set security policies from-zone trust to-zone custvpn policy permit_{}_outbound match application junos-icmp-all").format(CUSTOMER_NAME)
r28 = ("set security policies from-zone trust to-zone custvpn policy permit_{}_outbound match application sldap_636").format(CUSTOMER_NAME)
r29 = ("set security policies from-zone trust to-zone custvpn policy permit_{}_outbound match application junos-ldap").format(CUSTOMER_NAME)
r30 = ("set security policies from-zone trust to-zone custvpn policy permit_{}_outbound match application msft-gc-ssl_3268").format(CUSTOMER_NAME)
r31 = ("set security policies from-zone trust to-zone custvpn policy permit_{}_outbound match application msft-gc-ssl_3269").format(CUSTOMER_NAME)
r32 = ("set security policies from-zone trust to-zone custvpn policy permit_{}_outbound match application junos-http").format(CUSTOMER_NAME)
r33 = ("set security policies from-zone trust to-zone custvpn policy permit_{}_outbound match application junos-https").format(CUSTOMER_NAME)

#defining interface
r34 = ("set interfaces st0 unit {1} description {0}").format(CUSTOMER_NAME,INTERFACE)
r35 = ("set firewall family inet filter fbf-filter term {0} from destination-address {1}").format(CUSTOMER_NAME,CUSTOMER_NAT_POOL)
r36 = ("set firewall family inet filter fbf-filter term {0} then count fbf{1}").format(CUSTOMER_NAME,INTERFACE)
r37 = ("set firewall family inet filter fbf-filter term {0} then routing-instance fbf{1}").format(CUSTOMER_NAME,INTERFACE)

# configuring the rib groups 
r38 = ("set routing-options rib-groups fbf-group import-rib fbf{}.inet.0").format(INTERFACE)
r39 = ("set policy-options policy-statement redist-fbf{0} term 100 from instance fbf{0}").format(INTERFACE)
r40 = ("set policy-options policy-statement redist-fbf{0} term 100 from protocol static").format(INTERFACE)
r41 = ("set policy-options policy-statement redist-fbf{0} term 100 then next term").format(INTERFACE)
r42 = ("set policy-options policy-statement redist-fbf{0} term 101 from route-filter 0.0.0.0/0 exact reject").format(INTERFACE)
r43 = ("set routing-options instance-import redist-fbf{0}").format(INTERFACE)
r44 = ("set routing-instances fbf{0} instance-type forwarding").format(INTERFACE)
r45 = ("set routing-instances fbf{0} routing-options static route 0.0.0.0/0 next-hop st0.{0}").format(INTERFACE)
r46 = ("set routing-instances fbf{0} routing-options static route {1} next-hop st0.{0}").format(INTERFACE,CUSTOMER_NAT_POOL)

VPN_DEVICE="custvpn-vsrx-1"
r47 = ("\e[1;4;31m {} commands are like below====================================================== \e[0m").format(VPN_DEVICE)


print(r26)
print(r27)
print(r28)
print(r29)
print(r30)
print(r31)
print(r32)
print(r33)
print(r34)
print(r35)
print(r36)
print(r37)
print(r38)
print(r39)
print(r40)
print(r41)
print(r42)
print(r43)
print(r44)
print(r45)
print(r46)
print(r47)



#print ( "\e[1;4;31m  All variables you have entered are like below; \e[0m")
#print ( " CUSTOMER_NAME={CUSTOMER_NAME}")
#print ( " CUSTOMER_VPN_IP={CUSTOMER_VPN_IP}")
#print ( " PRE_SHARED_KEY={PRE_SHARED_KEY}")
#print ( " IKE_PROPOSALS={IKE_PROPOSALS}")
#print ( " IPSEC_PROPOSALS={IPSEC_PROPOSALS}")
#print ( " INTERFACE={INTERFACE}")
#print ( " CUSTOMER_IPS={CUSTOMER_IPS}")
#print ( " PROXY_REMOTE_IDENTITY={PROXY_REMOTE_IDENTITY}")
#print ( " CUSTOMER_NAT_POOL={CUSTOMER_NAT_POOL}")
#print ( " CUSTOMER_NAT_IPS={CUSTOMER_NAT_IPS}")
#print ( " REGION_SUBNET={REGION_SUBNET}")
#print ( " FW_SOURCE_ADDR={FW_SOURCE_ADDR}")
#print ( " PROXY_LOCAL_IDENTITY={PROXY_LOCAL_IDENTITY}")
#print ( " WEB_INSTANCES_IP={WEB_INSTANCES_IP}")





#while true; do
#    read -p "Press y or n ---> " yn
#    case yn in
        #[Yy]* ) print ( "Output is being generated for [custvpn-vsrx-1]...";break;;)
        #[Nn]* ) print ( "Cancelling...";exit;;)
        #* ) print ( "Please answer y or n!";;)
#    esac
#done	
#
#
#function_print (
#
#print ( "")
#
#while true; do
#    read -p "Do you want to list commands for second VPN device [custvpn-vsrx-2]? Press y or n ---> " yn
#    case yn in
#        [Yy]* ) print ( "Output is being generated for [custvpn-vsrx-2]...";break;;)
#        [Nn]* ) print ( "Cancelling...";exit;;)
#        * ) print ( "Please answer y or n!";;)
#    esac
#done	
#
#
#VPN_DEVICE="custvpn-vsrx-2"
#function_print (