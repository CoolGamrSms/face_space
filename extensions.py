import MySQLdb
import MySQLdb.cursors
import os
import uuid
import hashlib
from flask import Flask, session, abort, redirect, render_template, url_for

def connect_to_database():
  options = {
    'host': 'localhost',
    'user': 'root',
    'passwd': 'bill',
    'db': 'facespace',
    'port': 3306,
    'cursorclass' : MySQLdb.cursors.DictCursor
  }
  db = MySQLdb.connect(**options)
  db.autocommit(True)
  return db

def check_password(pinput, password):
  algorithm, salt, phash = password.split("$")
  m = hashlib.new(algorithm)
  m.update(salt + pinput)
  if m.hexdigest() == phash:
    return True
  return False

def hash_password(password):
  algorithm = 'sha512'     # name of the algorithm to use for encryption
  salt = uuid.uuid4().hex  # salt as a hex string for storage in db

  m = hashlib.new(algorithm)
  m.update(salt + password)
  password_hash = m.hexdigest()

  return "$".join([algorithm,salt,password_hash])

db = connect_to_database()
