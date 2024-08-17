#!/usr/bin/env python
import os
import sys
from ZmSharing import ZmSharing


url = os.getenv('ldap_url')
userdn = os.getenv('zimbra_ldap_userdn')
password = os.getenv('zimbra_ldap_password')
filename = sys.argv[1]
searchAccount = ZmSharing(url, userdn, password)
f = open(filename, 'r')
index = [1,2,5,7,8]

with f:
	lines = [line.rstrip('\n') for line in f]
	for account in lines:
		getAccountShare = searchAccount.zmLdapSearch(account)
		try:
			var = getAccountShare['zimbraSharedItem']
		except KeyError:
			pass
		else:
			for a in var:
				myshare = a.split(";")
				for getindex in index:
					(key, value) = myshare[getindex].split(':')
					print(key + " = " + value)
