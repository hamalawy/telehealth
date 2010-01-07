"""Project LifeLink: RxBox Database Commands

Author:     Thomas Rodinel Soler
            ------------------------------------------------
            Instrumentation, Robotics and Control Laboratory
            University of the Philippines - Diliman
            ------------------------------------------------
            January 2010
"""


from MySQLdb import connect


class rxboxDB:


	def __init__(self):
		pass
		
	def dbconnect(self):
		"""connects to the database and activate a cursor"""
		self.conn = connect(host = "localhost",
								user = "root",
								passwd = "irc311",
								db = "mysql")
		self.cursor = self.conn.cursor()
		self.cursor.execute("create database if not exists rxboxdb")
		self.cursor.execute("use rxboxdb") 

	
	def dbcreatetables(self):
		"""creates session, patient and biomed information tables in the database"""
		# creates session information table (if does not exist) and uses it.
		self.cursor.execute("""
			create table if not exists sessioninfo 
			(
				uuid varchar(36),
				sessionid varchar(36),
				starttime datetime,
				endtime datetime,
				primary key (uuid)
			)
			""") 
		# creates patient information table (if does not exist) and uses it.
		self.cursor.execute("""
			create table if not exists patientinfo 
			(
				uuid varchar(36),
				lastname varchar(20),
				firstname varchar(20),
				middlename varchar(20),
				address varchar(100),
				phonenumber varchar(20),
				age varchar(15),
				dmy varchar(15),
				gender varchar(10),
				foreign key (uuid) references sessioninfo(uuid)
			)
			""") 
		# creates biomedical information table (if does not exist) and uses it.			
		self.cursor.execute("""
			create table if not exists biomedinfo 
			(
				uuid varchar(36),
				biomedinfotype varchar(20),
				biomedfilename varchar(30),
				biomedcontent longblob,
				timestamp timestamp,
				foreign key (uuid) references sessioninfo(uuid)
			)
			""") 	
	
	def dbinsert(self,tblname,colname,value):
		"""insert a value into a specified column of a database table"""		
		self.cursor.execute("""
		    	insert into %s (%s)
		    	values 
		    	('%s')
		    	"""%(tblname,colname,value))

	def dbupdate(self,tblname,colname,value,condition1,condition2):
		"""updates a value into a specified column of a database table"""		
		self.cursor.execute("""
		    	update %s 
				set %s = '%s'
		    	where %s = '%s' 
		    	"""%(tblname,colname,value,condition1,condition2))
	
	def dbpatientinsert(self,tblname,col1name,col2name,col3name,\
						col4name,col5name,col6name,col7name,col8name,\
						col9name,value1,value2,value3,value4,value5,\
						value6,value7,value8,value9):
		"""inserts a new patient information to the patientinfo table"""
		self.cursor.execute("""
		    	insert into %s (%s,%s,%s,%s,%s,%s,%s,%s,%s) 
				values 
				('%s','%s','%s','%s','%s','%s','%s','%s','%s')
		    	"""%(tblname,col1name,col2name,col3name,col4name,\
					col5name,col6name,col7name,col8name,col9name,\
					value1,value2,value3,value4,value5,value6,value7,\
					value8,value9))			
	
	def dbpatientupdate(self,tblname,col1name,value1,col2name,value2,\
						col3name,value3,col4name,value4,col5name,\
						value5,col6name,value6,col7name,value7,col8name,\
						value8,condition1,condition2):
		"""updates a patient information to the patientinfo table"""		
		self.cursor.execute("""
		    	update %s set 
					%s = '%s',
					%s = '%s',
					%s = '%s',
					%s = '%s',
					%s = '%s',
					%s = '%s',
					%s = '%s',
					%s = '%s'
		    	where %s ='%s'			
		    	"""%(tblname,col1name,value1,col2name,value2,\
						col3name,value3,col4name,value4,col5name,\
						value5,col6name,value6,col7name,value7,col8name,\
						value8,condition1,condition2))
						
	def dbbiomedinsert(self,tblname,col1name,col2name,col3name,\
						col4name,value1,value2,value3,value4):
		"""inserts a new biomed information to the biomedinfo table"""
		self.cursor.execute("""
		    	insert into %s (%s,%s,%s,%s) 
				values 
				('%s','%s','%s','%s')
		    	"""%(tblname,col1name,col2name,col3name,col4name,\
					value1,value2,value3,value4))
					
	def dbbiomedupdate(self,tblname,col1name,value1,col2name,value2,\
						col3name,value3,condition1,condition2):
		"""updates a biomed information to the biomedinfo table"""
		self.cursor.execute("""
		    	update %s set 
					%s = '%s',
					%s = '%s',
					%s = '%s',
		    	where %s ='%s'			
		    	"""%(tblname,col1name,value1,col2name,value2,\
						col3name,value3,condition1,condition2))
