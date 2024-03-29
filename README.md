# Inquisitor Telegram Bot
A telegram bot designed to moderate the group chat for the suburban residential complex "Petrivsky Kvartal" with over 4000 members. The bot is infused with local humor in user notifications and uses an additional microservice to check the availability of more than ten hosts with the ping command. The bot notifies users in case of electricity loss or appearance and is used daily by hundreds of people.  
  
You can try it in action [here](https://t.me/pk_moderatorbot)

## Features
- User notification system with local humor
- Electricity availability checking via ping microservice
- Alert subscriptions via private messages
- Statistics of electricity availability periods
- FAQ answers in group chat
- Donations

## Technology Stack
- Python 3.10
- aiogram 3.0
- asyncio
- sqlalchemy 2.0
- alembic
- loguru
- Github Actions for CI/CD to digitalocean

## Background
This project was created in the context of regular power outages due to the war in Ukraine and is being used to improve the daily lives of its users.
