# pwn-patrol
pwn-patrol will accept an email (or list of emails) to query  [Have I Been Pwned?](https://haveibeenpwned.com/) for associated leaks and pastes

Simply execute with `python3 pwn-patrol.py`, provide an HIBP API key, and choose your option.

Note: Currently the third option to conduct the OSINT is in dev and not merged.

```
 🍕  pwn-patrol  ➜ python3 pwn-patrol.py       
______ _    _ _   _       ______  ___ ___________ _____ _     
| ___ \ |  | | \ | |      | ___ \/ _ \_   _| ___ \  _  | |    
| |_/ / |  | |  \| |______| |_/ / /_\ \| | | |_/ / | | | |    
|  __/| |/\| | . ` |______|  __/|  _  || | |    /| | | | |    
| |   \  /\  / |\  |      | |   | | | || | | |\ \\ \_/ / |____
\_|    \/  \/\_| \_/      \_|   \_| |_/\_/ \_| \_|\___/\_____/
       🐾 No job is too big, no pwn is too small 🐾
           
[?] HIBP API Key: ********************************
[?] What are we doing?: 
 > Looking up an email for pwnage (quick)
   Providing a list of emails to query (normal)
   Performing OSINT, then checking for pwnage (slowest)
```