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
import cgi
import os
import random
import hashlib
from bottle import template, response, request
#-----------------------------------------------------------------------
# Constants
#-----------------------------------------------------------------------
DBADDRESS="cmatrix.sqlite"
GETCATEGORY="select id from category where name=?"
NEWCOMPETENCE="insert into competence(category_id,name) Values(?,?)"
CHECKUSERCOMPETENCE="select id from user_competence where user_id=? and competence_id=?"
INSERTUSERCOMPETENCE="insert into user_competence(user_id,competence_id,scale_id) Values(?,?,?)"
UPDATEUSERCOMPETENCE="update user_competence set scale_id=? where id=?"
UPDATESESSTION="update user set session_id=? where username=?"
#-----------------------------------------------------------------------
# Functions
#-----------------------------------------------------------------------
def removeUnwantedChars(text):
  UNWANTED="\n\\\"'?;"
  for c in UNWANTED:
    text=text.replace(c,'')
  return text
#-----------------------------------------------------------------------
def getID(cur, tablename, entryname, value):
  sql = "select id from %s where %s=? collate nocase" % (tablename, entryname)
  cur.execute(sql, (value,))
  row = cur.fetchone()
  if row is not None:
    return row[0]
  return None
#-----------------------------------------------------------------------
def getRandomString():
  RANDOMPASSWD="ABCDEFGHJKLMNPQRSTUVXYZabcdefghjkmnpqrstuvxyz23456789"
  s1=""
  random.seed()
  for i in range(0,20):
    s1=s1+RANDOMPASSWD[random.randint(0,len(RANDOMPASSWD)-1)]
  return s1
#-----------------------------------------------------------------------
def getSessionCookie():
  if 'HTTP_COOKIE' in os.environ:
   for cookie in os.environ['HTTP_COOKIE'].split(';'):
      (key, value ) = cookie.split('=');
      if key.strip() == "session_id":
         return value
  return None
#-----------------------------------------------------------------------
def encryptText(text):
  return hashlib.md5(text.encode()).hexdigest()
#-----------------------------------------------------------------------
def getSessionUser(cur,session_id):
  if session_id is not None:
    cur.execute("select username from user where session_id=?",(session_id,))
    row=cur.fetchone()
    if row is not None:
      return row['username']
  return None
#-----------------------------------------------------------------------
def getUser(cur,form,session_id):
  if form.getvalue('username') is not None and form.getvalue('password') is not None:
    cur.execute("select salt from user where username=?",(form.getvalue('username'),))
    row=cur.fetchone()
    if row is not None:
      hash_password=encryptText(form.getvalue('password')+row['salt'])
      cur.execute("select username from user where username=? and password=?",(form.getvalue('username'),hash_password))
      row=cur.fetchone()
      if row is not None:
        cur.execute(UPDATESESSTION,(session_id,form.getvalue('username')))
        conn.commit()
        return form.getvalue('username')
  return None
#-----------------------------------------------------------------------
def isnumeric(s):
  try:
    n = int(s)
    return True
  except ValueError:
    return False
#-----------------------------------------------------------------------
# Main
#-----------------------------------------------------------------------
try:
  reload(sys)
  sys.setdefaultencoding('utf8')
  form = cgi.FieldStorage()
  conn=sqlite3.connect(DBADDRESS)
  conn.row_factory=sqlite3.Row
  cur=conn.cursor()
  session_id=getRandomString()
  username=getUser(cur,form,session_id)
  if username is None:
    session_id=getSessionCookie()
    username=getSessionUser(cur,session_id)
  else:
    response.set_cookie('session_id',session_id, path='/')
  response.content_type = 'text/html; charset=UTF-8' 
  print(response)
  if username is None:
    print(template('redirect.tpl',link="index.py",text="Wrong username/password"))
    exit(0)
  if form.getvalue('page')=="add_competence":
    user_id=getID(cur,"user","username",username)
    category_id=getID(cur,"category","id",form.getvalue('category_id'))
    competence_id=getID(cur,"competence","name",form.getvalue('mycompetence'))
    if competence_id is None:
      cur.execute(NEWCOMPETENCE,(category_id,form.getvalue('mycompetence')))
      competence_id=getID(cur,"competence","name",form.getvalue('mycompetence'))
    cur.execute(CHECKUSERCOMPETENCE,(user_id,competence_id))
    row=cur.fetchone()
    if row is None:
      cur.execute(INSERTUSERCOMPETENCE,(user_id,competence_id,form.getvalue('scale_id')))
      text="New user competence has been added"
    else:
      cur.execute(UPDATEUSERCOMPETENCE,(form.getvalue('scale_id'),row[0]))
      text="User competence has been updated"
  if form.getvalue('page')=="pers_cmatrix":
    for key in form.keys():
      value=form.getvalue(key)
      if key=='page' or value=="0":
        continue
      # In python3 convert to key.isnumeric()
      if isnumeric(key):
        cur.execute(UPDATEUSERCOMPETENCE,(value,key))
      else:
        competence_id=getID(cur,"competence","name",key)
        user_id=getID(cur,"user","username",username)
        cur.execute(INSERTUSERCOMPETENCE,(user_id,competence_id,value))
    text="User competence has been updated"
  conn.commit()
  conn.close()
  print(template('redirect.tpl',link=form.getvalue('page')+".py",text=text))  

except Exception as e:
  print(template('redirect.tpl',link="add_competence.py",text=e))