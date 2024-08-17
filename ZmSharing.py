#!/usr/bin/env python

import sys
import os
import ldap
import ldap.modlist as modlist
import timeout_decorator



class ZmSharing():
    def __init__(self, ldap_url, zimbra_ldap_userdn, zimbra_ldap_password, ou=""):
        self.url = ldap_url
        self.binddn = zimbra_ldap_userdn
        self.passwd = zimbra_ldap_password
        self.basedn = ou

    @timeout_decorator.timeout(10, timeout_exception=StopIteration)
    def zmLdapSearch(self, account):
        try:
            # Efetuando a conexao com o ldap
            connection = ldap.initialize("%s"%self.url)
            connection.protocol_version = ldap.VERSION3 # Define a versao 3 do protocolo ldap (recomendado)
            connection.bind(self.binddn, self.passwd)
        except StopIteration:
            print("Nao foi possivel conectar com o servidor ldap")
            sys.exit(1)
        except ldap.SERVER_DOWN:
            print("Nao foi possivel conectar com o servidor ldap")

        searchFilter = '(&(objectClass=zimbraAccount)(mail=%s))'%(account)
        searchAttributes = ['mail', 'zimbraSharedItem']
        getUser = connection.search_s(self.basedn, ldap.SCOPE_SUBTREE, searchFilter, searchAttributes)
    	return getUser[0][1]
