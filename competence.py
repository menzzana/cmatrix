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
from bottle import template, response, request
#-----------------------------------------------------------------------
# Constants
#-----------------------------------------------------------------------
DBADDRESS="cmatrix.sqlite"
GETCOMPETENCE="select name from competence where id=?"
GETALLCOMPETENCES="select * from competence order by name"
PRINTCOMPETENCE="select * from cmatrix where competence_id=? and scale_id>0 order by scale_id desc"
SCALE="select * from competence_scale order by id"
#-----------------------------------------------------------------------
# Function
#-----------------------------------------------------------------------
def getUsernameCookie():
  if 'HTTP_COOKIE' in os.environ:
   for cookie in os.environ['HTTP_COOKIE'].split(';'):
      (key, value ) = cookie.split('=');
      if key.strip() == "username":
         return value
  return None
#-----------------------------------------------------------------------
def getUser(cur,form):
  if form.getvalue('username') is not None and form.getvalue('password') is not None:
    cur.execute("select username from user where username=? and password=?",(form.getvalue('username'),form.getvalue('password')))
    row=cur.fetchone()
    if row is not None:
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
  username=getUser(cur,form)
  if username is None:
    username=getUsernameCookie()
  else:
    response.set_cookie('username',form.getvalue('username'), path='/')
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
