# personicle-authentication-service

Add ``` client_secrets.json ``` file in root folder.

``` pip install -r requirements.txt ```

Run the server:
``` python authenticate.py ```

**Endpoints**
  - Request Example
    - ```  curl -k https://20.121.8.101:5222/authenticate -H "Authorization: Bearer   eyJraWKi...5NQk" ```
     
  - Response Example (If valid bearer token)
      - ``` {"message":true} ```
      
  - Response Example (If invalid bearer token)
      - ``` Unauthorized ```
  
