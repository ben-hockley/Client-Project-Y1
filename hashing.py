import bcrypt

password = b"Alex"
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password,salt)
print(f"salt: {salt}")
print(f"hashed: {hashed}")
salt = bcrypt.gensalt()
print(f"salt: {salt}")

import hashlib
 
# Declaring Password
password = 'GeeksPassword'
# adding 5gz as password
salt = "5gz"
 
# Adding salt at the last of the password
dataBase_password = password+salt
# Encoding the password
hashed = hashlib.md5(dataBase_password.encode())
 
# Printing the Hash
print(hashed.hexdigest())
