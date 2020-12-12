# MoneySaver

This bot will help you to reduce your expenses. The bot was implemented by using Python3.8 + TelegramBotAPI + MySQL

![alt text](https://github.com/AndreyKaBelka/MoneySaver/blob/master/Скриншот1.PNG)   

![alt text](https://github.com/AndreyKaBelka/MoneySaver/blob/master/Скриншот2.PNG)

## Start the bot
0) Sstart MySql DB
1) Create config json file like in example.json in **MoneySaver folder**
2) In cmd go to MoneySaver folder
3) Install venv
```cmd
pip install venv
```
4) Create virtual env using python:
  ```cmd
  python -m venv venv
  ```
5) Activate venv and install all libraries:
```cmd
  \venv\bin\activate.bat
  pip install -r requirements.txt
  ```
6) Start the bot from the **MoneySaver folder**(!!!):
```cmd
  python -m app.main -f [config_file_name].json
  ```
7) Enjoy!
