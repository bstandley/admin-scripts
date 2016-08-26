#!/usr/bin/python3

# description: determine public IP address and update DNS record using the Linode API

# notes:
#   - requests module would be simpler for both lookup and update, if not for
#     the need to handle both IPv4 and IPv6 addresses
#   - place urip.php on any webserver
#   - fill in configs below . . .

# refs:
#   - https://github.com/snorp/linode
#   - http://pycurl.io/docs/latest/quickstart.html

import io
import pycurl
import requests

conf_ip_url        = 'http://webserver/urip.php'
conf_api_url       = 'https://api.linode.com'
conf_api_key       = ''
conf_api_action    = 'domain.resource.update'
conf_resource_id_4 = ''
conf_resource_id_6 = ''

def lookup (ipv6=False) :

	buf = io.BytesIO()
	c = pycurl.Curl()
	c.setopt(c.URL, conf_ip_url)
	c.setopt(c.IPRESOLVE, c.IPRESOLVE_V6 if ipv6 else c.IPRESOLVE_V4)
	c.setopt(c.WRITEDATA, buf)
	c.perform()
	res_code = c.getinfo(c.RESPONSE_CODE)
	c.close()

	if res_code != 200 : return False

	bufstr = buf.getvalue().decode('iso-8859-1')
	return bufstr if ipv6 else bufstr.split(':')[-1]

def update (resource_id, ip_addr) :

	params = {'api_action' : conf_api_action,
	          'api_key'    : conf_api_key,
	          'ResourceID' : resource_id,
	          'Target'     : ip_addr}

	res = requests.get(conf_api_url, params=params)
	return res.ok

if __name__ == "__main__" :

	import datetime
	print('Timestamp:   ' + str(datetime.datetime.now()))

	ip_addr_4 = lookup(ipv6=False)
	ip_addr_6 = lookup(ipv6=True)

	print('Lookup IPv4: ' + ip_addr_4 if ip_addr_4 else '?')
	print('Lookup IPv6: ' + ip_addr_6 if ip_addr_6 else '?')

	if ip_addr_4 :
		ok = update(conf_resource_id_4, ip_addr_4)
		print('Update IPv4: ' + 'OK' if ok else 'NOK')
	if ip_addr_6 :
		ok = update(conf_resource_id_6, ip_addr_6)
		print('Update IPv6: ' + 'OK' if ok else 'NOK')

