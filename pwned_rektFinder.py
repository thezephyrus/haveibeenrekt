import boto3
import json
import hashlib
import requests
import re

# CONSTANTS
PWNED_URL = "https://api.pwnedpasswords.com/range/"

test_password ="admin123"

# Function to get the hash value - SHA1
def sha1Hash(toHash):
        try:
            messageDigest = hashlib.sha1()
            stringM = str(toHash)
            byteM = bytes(stringM, encoding='utf')
            messageDigest.update(byteM)
            return messageDigest.hexdigest()
        except TypeError:
            raise "String to hash was not compatible"

# API call to haveibeenpwned
def pwned_api(range):
    try:
        print(PWNED_URL+range)
        response = requests.get(PWNED_URL+range)
        #print(response.text)
        return response.text
    except:
        print("Error making the API call")

def lambda_handler(event, context):
    is_breached=False
    seen_count=0
    # get the password from context here and convert it to sha1
    sha1_string = str.upper(sha1Hash(test_password))
    #print("SHA1-String: "+sha1_string)

    # trim the hash string with last 5 chars to invoke the API call
    my_range = sha1_string[:5]
    #print("Range: "+my_range)

    # invoke the haveibeenpwned API call
    data = pwned_api(my_range)
    sub =sha1_string[5:]
    my_regex=".*"+sub+"\:(\d+)"
    count=re.search(my_regex,data).group(1)

    if int(count)>0:
        is_breached=True
        seen_count=int(count)
    result={
        "is_breached":is_breached,
        "seen_count":seen_count
    }


    return result




if __name__ =="__main__":
    results=lambda_handler("event","context")
    print(results)