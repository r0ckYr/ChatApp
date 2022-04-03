# ChatApp
A simple multi client chat app in python

##Installation
```
git clone https://github.com/r0ckYr/ChatApp.git
cd ChatApp
pip3 install -r requirements.txt

```
##How to use
1. Open client.py in any text editor
2. Add your ip to the server variable
 ![Screenshot from 2022-04-03 21-06-53](https://user-images.githubusercontent.com/73944333/161435792-48ad74ba-a4ea-4b5d-87c8-0e7cc3b3bb09.png)
3. Start multi-client-server.py on you Server
   ```python3 multi-client-server.py```
   ![Screenshot from 2022-04-03 21-09-17](https://user-images.githubusercontent.com/73944333/161435897-acef2693-a59c-4344-ae8f-f43d74ba16b7.png)
   
4. Start the client app on you machine
  ```python3 client.py```
  ![Screenshot from 2022-04-03 21-11-13](https://user-images.githubusercontent.com/73944333/161435982-82c99da3-4207-4c3b-8739-ea21c45564da.png)


##TODO

There is problem in connection when a client disconnets and tries to connect again, the client has to try multiple times to connect properly. Should add feature in client side app to retry by itself OR use threading the traditional way, using Queue, to handle connections properly.
