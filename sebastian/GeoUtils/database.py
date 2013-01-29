#!/usr/bin/python
# David Newell
# GeoUtils/database.py
# Geographical Utilities package
# Database Access Protocols


# Import MySQLdb module for MySQL database access functions
import MySQLdb


class RDB:
    """
     Research Database Access Protocols
         Storage variables:
             DBuser   - MySQL User
             DBpasswd - MySQL Password
             DBhost   - MySQL Host
             DBconn   - MySQL Connection Instance
             DBcursor - MySQL Cursor Instance
             ge_key - Connected User's ge_key
             connectedUserName - Connected User's Name
             connectedUserPrivilege - Connected User's Edit Privileges
             connectedUserType - Connected User's Type

         Methods:
              isConnected()   - Returns connection status (true/false)
              setUser(user)   - Change user from default
              setPass(passwd) - Change password from default
              setHost(host)   - change host from default
              connect(db)     - connect to database
              query(query)    - query the database
    """

    def __init__(self,ge_key=None):
        """ Initialize RDB class with default information """

        """ Default Database Information """
        self.DBuser   = 'uws_ge'
        self.DBpasswd = 'littlemermaid'
        self.DBhost   = 'localhost'
        self.defaultDB = "uws_ge"
        self.DBconn   = None
        self.DBcursor = None

        """ Connected User Information """
        self.ge_key = ge_key
        self.connectedUserName = None
        self.connectedUserType = None
        self.connectedUserPrivilege = 0
        self.setUserDetails()


    # isConnected - check if DB is connected
    def isConnected(self):
        return self.DBconn != None


    # setUser - set MySQL user
    def setUser(self,user):
        self.DBuser = user


    # setPass - set MySQL password
    def setPass(self,passwd):
        self.DBpasswd = passwd


    # setHost - set MySQL host
    def setHost(self,host):
        self.DBhost = host


    # connect - function to handle database connections
    def connect(self,db):
        #print 'connecting'
        if self.DBconn != None:
            self.close()

        self.DBconn = MySQLdb.connect(host = self.DBhost,
                              user = self.DBuser,
                              passwd = self.DBpasswd,
                              db = db)


    # query - function to handle database queries
    def query(self,query,type="dict"):
        if type == "dict":
            self.DBcursor = self.DBconn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            self.DBcursor.execute(query)
            return self.DBcursor.fetchall(),int(self.DBcursor.rowcount)
        else:
            return False,0


    # close - function to close database connection
    def close(self):
        if self.DBcursor != None:
            self.DBcursor.close()
        if self.DBconn != None:
            self.DBconn.commit()
            self.DBconn.close()


    # Set connected user's key and update details
    def setConnUserKey(self,ge_key):
        self.ge_key = str(ge_key)
        self.setUserDetails()

    # Retrieve connected user's name
    def ConnUserName(self):
        return self.connectedUserName

    # Retrieve connected user's type
    def ConnUserType(self):
        return self.connectedUserType

    # Retrieve connected user's edit privilege
    def ConnUserPrivilege(self):
        return self.connectedUserPrivilege

    # Retrieve connected user's key
    def ConnUserKey(self):
        return self.ge_key


    # Set user details
    def setUserDetails(self):
        # If no GE_KEY available, return visitor
        if self.ge_key == None or self.ge_key == '':
            # Function exits
            return 0

        # Build database query
        dbq = 'SELECT name,user_type FROM users WHERE GE_KEY="' + str(self.ge_key) + '"'

        if not self.isConnected():
            # Connect to default database
            self.DBconnect(self.defaultDB)

        # Query database
        dbdata,rowcount = self.query(dbq)

        # If no GE_KEY available, return visitor
        if rowcount > 1 or rowcount == 0:
            # Function exits
            return 0

        u = dbdata[0]

        user = str(u["name"])
        ut = str(u["user_type"])

        # Dictionary of user types and edit permissions
        userTypes = {
                "administrator" : 1,
                "professor" : 1,
                "student" : 1,
                "collaborator" : 1,
                "viewer" : 0,
                "visitor" : 0
            }

        # Set username, usertype, and privilege
        self.connectedUserName = user
        self.connectedUserType = ut
        self.connectedUserPrivilege = userTypes.get(ut)


