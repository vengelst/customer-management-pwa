#!/usr/bin/env python3
import os
from app import app

if __name__ == '__main__':
    if not os.environ.get('DATABASE_URL'):
        os.environ['DATABASE_URL'] = 'sqlite:///customer_management.db'
    if not os.environ.get('SESSION_SECRET'):
        os.environ['SESSION_SECRET'] = 'dev-secret-key-12345'
    
    app.run(host='0.0.0.0', port=5000, debug=True)
