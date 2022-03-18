# personicle-authentication-service

Add ``` client_secrets.json ``` file in root folder.

``` pip install -r requirements.txt ```

Run the server:
``` python authenticate.py ```

**Endpoints**
  - Request
    - /authenticate
      - headers: Authorization Bearer token
  - Response
      ``` If authorized, {message:True}, 200 else "Unauthorized, 401"```
