vsrx_config is script which will generate configuration for the IPsec vpn based on our inputs

Requirements

1. Python3

Install

follow the below link to install python
https://realpython.com/installing-python/

How to use

- Navigate to the script folder
- and run the below command
  - python3 vsrx_config
- and then you will be prompted to enter the following
  
  CUSTOMER_TYPE = cloud/hosted
  CUSTOMER_REGION = us/eu
  VSRX_TYPE = primary/standby
  CUSTOMER_NAME = name of the customer
  CUSTOMER_VPN_IP = customer peer ip
  PRE_SHARED_KEY = pre shared key
  IKE_PROPOSALS = phase-1 propsals
  IPSEC_PROPOSALS = phase-2 propsals
  INTERFACE = tunnel interface
  CUSTOMER_IPS = customer IPs
  PROXY_REMOTE_IDENTITY = remote encryption domain
  CUSTOMER_NAT_POOL = destination nat pool
  CUSTOMER_NAT_IPS = destination nat IPs
  
  
after inputting all values the configuration will be generated
