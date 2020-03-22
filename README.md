# Shell Lover ❤
Reverse shell cheat sheet tool for pentesters and CTF players.
# Usage
```python3 shell_lover.py -i IPADDRESS -p PORT```

![alt text](https://github.com/de4dc0w/shell_lover/blob/master/shellover.png)

# Add new shells
To add your new reverse shell, you need to modify **shells.ini** file and add your shell in the following format
```
[SHELLNAME]
ANYVAR: YOUR_SHELL
```
And the main script will do the rest.
