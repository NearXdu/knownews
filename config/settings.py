# -*- coding: utf-8 -*-

#db config


MySQLdb_setting = {
	'knownews':{
		'host':'localhost',
		'port': 3306,
		'user':'root',
		'passwd':'root',
		'db':'knownews',
		'charset':'utf8'
	}
}

db_prod={
	'knownews':{
		'drivername':'mysql',
		'username':'root',
		'password':'root',
		'database':'knownews',
		'host':'localhost',
		'port':3306
	}
}


DATABASE = db_prod
