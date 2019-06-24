#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os 
import sys
import codecs
from ZmSharing import ZmSharing

reload(sys)
sys.setdefaultencoding('utf-8')

url = os.getenv('ldap_url')
userdn = os.getenv('zimbra_ldap_userdn')
password = os.getenv('zimbra_ldap_password')
searchAccount = ZmSharing(url, userdn, password)
filename = sys.argv[1]
f = open(filename, 'r')
index = [1,2,5,7,8]
dictShare = {}

with f:
	lines = [line.rstrip("\n") for line in f]
	for account in lines:
		getAccountShare = searchAccount.zmLdapSearch(account)
		try:
			zimbraShare = getAccountShare['zimbraSharedItem']
		except KeyError:
			pass
		else:
			for share in zimbraShare:
				myshare = share.split(";")
				for getindex in index:
					(key, value) = myshare[getindex].split(':')
					dictShare[key] = value
				with codecs.open('sharing.sh', 'a', encoding='utf-8') as sharing:
					sharing.write('zmmailbox -z -m %s mfg "%s" account %s %s\n'%(account, dictShare['folderPath'], dictShare['granteeName'], dictShare['rights']))
