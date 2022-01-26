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
GETCOMPETENCE="select name from competence where id=?"
GETALLCOMPETENCES="select * from competence order by name"
PRINTCOMPETENCE="select * from cmatrix where competence_id=? and scale_id>0 order by scale_id desc"
UPDATESESSTION="update user set session_id=? where username=?"
SCALE="select * from competence_scale order by id"
#-----------------------------------------------------------------------
# Function
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
  competence_id=1
  if form.getvalue('competence_id') is not None:
    competence_id=form.getvalue('competence_id')
  cur.execute(GETCOMPETENCE,(competence_id,))
  row=cur.fetchone()
  competence=row[0]
  cur.execute(SCALE)
  rowscale=cur.fetchall()
  cur.execute(PRINTCOMPETENCE,(competence_id,))
  rowcompetence=cur.fetchall()
  cur.execute(GETALLCOMPETENCES)
  rowallcompetence=cur.fetchall()
  print(template('competence.tpl', username=username, competence=competence, rowcompetence=rowcompetence, rowscale=rowscale,rowallcompetence=rowallcompetence))
  conn.close()

except Exception as e:
  print("ERROR: %s" % e)
