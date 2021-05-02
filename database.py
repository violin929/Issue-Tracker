#!/usr/bin/env python3
import psycopg2

#####################################################
##  Database Connect
#####################################################

'''
Connects to the database using the connection string
'''


def openConnection():
    # connection parameters - ENTER YOUR LOGIN AND PASSWORD HERE
    userid = "y20s1c9120_rwan9217"
    passwd = "500035351"
    myHost = "soit-db-pro-2.ucc.usyd.edu.au"

    # Create a connection to the database
    conn = None
    try:
        # Parses the config file and connects using the connect string
        conn = psycopg2.connect(database=userid,
                                user=userid,
                                password=passwd,
                                host=myHost)
    except psycopg2.Error as sqle:
        print("psycopg2.Error : " + sqle.pgerror)

    # return the connection to use
    return conn


'''
List all the user associated issues in the database for a given user 
See assignment description for how to load user associated issues based on the user id (user_id)
'''


def checkUserCredentials(userName):
    # TODO - get user info for user
    conn = openConnection()
    try:
        curs = conn.cursor()
        curs.execute("SELECT * FROM A3_USER WHERE username=%(uname)s; "
                     , {'uname': userName})
        user_Info = curs.fetchall()
        curs.close()

        if userName is '-':
            print(psycopg2.Error.pgerror)
            return None
        for userInfo in user_Info:
            return userInfo
    except psycopg2.Error as sqle:
        print(sqle.pgerror)


'''
List all the user associated issues in the database for a given user 
See assignment description for how to load user associated issues based on the user id (user_id)
'''


def findUserIssues(user_id):
    # TODO - list all user associated issues from db using sql
    # print(user_id)

    conn = openConnection()
    try:
        curs = conn.cursor()
        #curs.execute("SELECT ISSUE_ID, TITLE, CREATORjoin.username, RESOLVERjoin.username, VERIFIERjoin.username, DESCRIPTION FROM A3_ISSUE JOIN A3_USER CREATORjoin ON (CREATOR=CREATORjoin.USER_ID) JOIN A3_USER RESOLVERjoin ON (RESOLVER=RESOLVERjoin.USER_ID) JOIN A3_USER VERIFIERjoin ON (VERIFIER=VERIFIERjoin.USER_ID) ORDER BY TITLE",(user_id,user_id,user_id,))
       
        #curs.execute("SELECT ISSUE_ID, TITLE, CREATORjoin.username, RESOLVERjoin.username, VERIFIERjoin.username, DESCRIPTION FROM A3_ISSUE JOIN A3_USER CREATORjoin ON (CREATOR=CREATORjoin.USER_ID) JOIN A3_USER RESOLVERjoin ON (RESOLVER=RESOLVERjoin.USER_ID) JOIN A3_USER VERIFIERjoin ON (VERIFIER=VERIFIERjoin.USER_ID) ORDER BY TITLE")

        curs.execute("BEGIN;")
        curs.callproc("ListIssues", [int(user_id),int(user_id),int(user_id)])
        issue_db = curs.fetchall()
        curs.close()

        issue = [{
            'issue_id': str(row[0]),
            'title': str(row[1]),
            'creator': str(row[2]),
            'resolver': str(row[3]),
            'verifier': str(row[4]),
            'description': str(row[5])
        } for row in issue_db]

        return issue
    except psycopg2.Error as sqle:
        print("psycopg2.Error : " + sqle.pgerror)
        return None


'''
Find the associated issues for the user with the given userId (user_id) based on the searchString provided as the parameter, and based on the assignment description
'''


def findIssueBasedOnExpressionSearchOnTitle(searchString):
    # TODO - find necessary issues using sql database based on search input
    # print("search string '" + searchString + "'")
    conn = openConnection()
    try:
        curs = conn.cursor()

        
        curs.execute(
            "SELECT ISSUE_ID, TITLE, CREATORjoin.username, RESOLVERjoin.username, VERIFIERjoin.username, DESCRIPTION FROM A3_ISSUE JOIN A3_USER CREATORjoin ON (CREATOR=CREATORjoin.USER_ID) JOIN A3_USER RESOLVERjoin ON (RESOLVER=RESOLVERjoin.USER_ID) JOIN A3_USER VERIFIERjoin ON (VERIFIER=VERIFIERjoin.USER_ID) WHERE TITLE like %(keyword)s ORDER BY TITLE"
            , {'keyword': '%' + searchString + '%'})
        
        
            
        issue_db = curs.fetchall()
        curs.close()

        issue = [{
            'issue_id': str(row[0]),
            'title': str(row[1]),
            'creator': str(row[2]),
            'resolver': str(row[3]),
            'verifier': str(row[4]),
            'description': str(row[5])
        } for row in issue_db]

        return issue
    except psycopg2.Error as sqle:
        print("psycopg2.Error : " + sqle.pgerror)
        return None


#####################################################
##  Issue (new_issue, get all, get details)
#####################################################
# Add the details for a new issue to the database - details for new issue provided as parameters
def addIssue(title, creator, resolver, verifier, description):
    # TODO - add an issue
    # Insert a new issue to database
    conn = openConnection()
    try:
        curs = conn.cursor()

        curs.execute("SELECT USER_ID FROM A3_USER WHERE USERNAME=%s", (creator,))
        creatorId = curs.fetchone()
        curs.execute("SELECT USER_ID FROM A3_USER WHERE USERNAME=%s", (resolver,))
        resolverId = curs.fetchone()
        curs.execute("SELECT USER_ID FROM A3_USER WHERE USERNAME=%s", (verifier,))
        verifierId = curs.fetchone()

        if (not creatorId) or (not resolverId) or (not verifierId):
            return False
        else:
            curs.execute("Insert into A3_ISSUE (TITLE,DESCRIPTION,CREATOR,RESOLVER,VERIFIER) values (%s,%s,%s,%s,%s);",
                         (title, description, creatorId, resolverId, verifierId,))
        conn.commit()
        curs.close()
        return True

    except psycopg2.Error as sqle:
        print("psycopg2.Error : " + sqle.pgerror)
        return False


    # Update the details of an issue having the provided issue_id with the values provided as parameters
def updateIssue(title, creator, resolver, verifier, description, issue_id):
    # TODO - update the issue using db

    conn = openConnection()
    try:
        curs = conn.cursor()

        curs.execute("SELECT USER_ID FROM A3_USER WHERE USERNAME=%s", (creator,))
        creatorId = curs.fetchone()
        curs.execute("SELECT USER_ID FROM A3_USER WHERE USERNAME=%s", (resolver,))
        resolverId = curs.fetchone()
        curs.execute("SELECT USER_ID FROM A3_USER WHERE USERNAME=%s", (verifier,))
        verifierId = curs.fetchone()

        
        curs.execute(
            """UPDATE A3_ISSUE SET TITLE=%s, DESCRIPTION=%s, CREATOR=%s, RESOLVER=%s, VERIFIER=%s  WHERE ISSUE_ID=%s;""",
            (title, description, creatorId, resolverId, verifierId, issue_id,))
        

        conn.commit()
        curs.close()
        return True  # return True if adding was successful

    except psycopg2.Error as sqle:
        print("psycopg2.Error : " + sqle.pgerror)
        return False  # return False if adding was unsuccessful
