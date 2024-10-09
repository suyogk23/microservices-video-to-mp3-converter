## auth service server
# user requests for auth via gateway
# gateway will forward req to auth
# if user is valid, auth will send a jwt token to user to use our app
        
import jwt  #JSON web token for auth 
import datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)    #instantiate flask object
mysql = MySQL(server)       #mysql object

## configurations in env vars
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST") 
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD") 
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB") 
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER") 
server.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT"))

# LOGIN ROUTE
@server.route("/login", methods=["POST"])
def login():
    #get the authentication header
    auth = request.authorization #auth header format = base64(username:password)
    if not auth:
        return "credentials not found(server.py)", 401  #401: invalid credentials
    
    #check DB-SQL for username and password
    cur = mysql.connection.cursor()
    res = cur.execute("SELECT email, password FROM user WHERE email=%s", (auth.username,) )

    if res>0:    #more than 0 rows found
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]
        
        print(f"Fetched email from database: {email}")

        if (auth.username  != email) or (auth.password != password):
            return "LOGIN FAILED: INVALID CREDENTIALS", 401 
        else:
            return createJWT(auth.username, os.environ.get('JWT_SECRET'), True)
    
    else:
        return "LOGIN FAILED: USER NOT FOUND", 401

#token validation
@server.route("/validate", methods=['POST'])
def validate():
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "Credentials validation failed: Missing token", 401
    
    #authentication header format: Bearer <token>
    try:
        encoded_jwt = encoded_jwt.split(" ")[1]
    except:
        return "Credentials validation failed: Invalid token format", 401

    try:
        decoded = jwt.decode(
            encoded_jwt, 
            os.environ.get('JWT_SECRET'), 
            algorithms=['HS256']
        )
    except: 
        return 'NOT AUTHORIZED', 403
    
    return decoded, 200

  
def createJWT(username, secret, is_admin):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1),    #taken valid for 24 hrs
            "iat": datetime.datetime.now(datetime.timezone.utc),  #issue at timestamp
            "admin": is_admin,
        },
        secret, 
        algorithm = "HS256",
    )


if __name__ == "__main__":
    server.run(
        host = '0.0.0.0', #listen to all incoming networks (as ip is not static)
        port = 5010
    )