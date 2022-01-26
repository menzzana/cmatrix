#!/usr/bin/python
# coding=utf-8
"""
cmatrix
Copyright (C) 2022  Henric Zazzi <hzazzi@kth.se>
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
#-----------------------------------------------------------------------
import sqlite3
import sys
import os
import random
import hashlib
#-----------------------------------------------------------------------
# Constants
#-----------------------------------------------------------------------
DBADDRESS="cmatrix.sqlite"
INSERTUSER="insert into user(username,password,salt,full_name) Values(?,?,?,?)"
#-----------------------------------------------------------------------
# Functions
#-----------------------------------------------------------------------
def getRandomString(n):
  RANDOMPASSWD="ABCDEFGHJKLMNPQRSTUVXYZabcdefghjkmnpqrstuvxyz23456789"
  s1=""
  random.seed()
  for i in range(0,n):
    s1=s1+RANDOMPASSWD[random.randint(0,len(RANDOMPASSWD)-1)]
  return s1
#-----------------------------------------------------------------------
def encryptText(text):
  return hashlib.md5(text.encode()).hexdigest()
#-----------------------------------------------------------------------
# Main
#-----------------------------------------------------------------------
try:
  if len(sys.argv) == 1:
    print("create_user.py <username> <first name> <last name>")
    sys.exit(0)
  conn=sqlite3.connect(DBADDRESS)
  conn.row_factory=sqlite3.Row
  cur=conn.cursor()
  salt=getRandomString(5)
  password=getRandomString(10)
  hash_password=encryptText(password+salt)
  cur.execute(INSERTUSER,(sys.argv[1],hash_password,salt,sys.argv[2]+" "+sys.argv[3]))
  conn.commit()
  conn.close()
  print("Password for %s: %s" % (sys.argv[1],password))

except Exception as e:
  print("Error %s:" % e.args[0])
