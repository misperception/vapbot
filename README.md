# VapBot

> A bot for all your disgusting and degenerate necessities!
***

> [!WARNING]
> This project is discontinued as of this commit, the code is extremely messy and unfortunately I do not have the time to refactor it nor do I have the interest in it. I thank it for revitalizing my love for programming in several occasions.

## What is VapBot?

Vapbot is a Discord bot made with [discord.py](https://github.com/Rapptz/discord.py) with multiple features ~~(none of them good)~~. It was born as a way to piss off a friend and evolved into a personal project to force me to learn Python in general, but also many other aspects of programming as it was being developed.

## Alright, but what can it do?

I'm glad you ask. VapBot can currently:

- Fetch Vaporeon images from e621.net and spam them in channels ***AND*** DMs! (please use this in moderation)
- Serve as a music bot! (allegedly)
- Post the [Vaporeon Copypasta](https://www.reddit.com/r/copypasta/comments/eidplc/vaporeon_copypasta/).
- Host Russian Roulette sessions! (more on this [later](#commands))

## Installation

VapBot is meant to be hosted individually by every server owner that wants to have it. However, this is done extremely easily.

VapBot can then be installed through [Docker](#docker) or by running `main.py` through [venv](#venv). However it is preferred to use Docker as it is easier to manage.

### Docker

> You need to have Docker Engine installed as a prerequisite. Check out <https://docs.docker.com/engine/install/> for more information.

If you want to build the image from scratch:

1. Clone the Github repository:

```bash
git clone https://github.com/misperception/vapbot
cd vapbot
```

2. Build the Docker image from the Dockerfile:

```bash
sudo docker build -t vapbot:latest .
```

Otherwise you could just use the Docker Hub image. (<https://hub.docker.com/r/misperception/vapbot>)

3. Run the image:

If you want to run the image through Docker Compose, add the following snippet to your `compose.yml` file:

```yaml
services:
    vapbot:
        container_name: vapbot
        # image: vapbot:latest if you built the image from the repo
        image: misperception/vapbot # to pull the image from Docker Hub (recommended)
        restart: unless_stopped
        environment:
            - TOKEN= # insert your bot token from https://discord.com/developers/applications
            - ID= # insert your Discord user ID to access debugging commands
            - PREFIX= # insert a prefix for classic text-based commands
```

This is the recommended method for adding the bot.

Otherwise run the following command:

```bash
sudo docker run -d \
    --name vapbot \
    -e TOKEN= `# insert your bot token from https://discord.com/developers/applications` \
    -e ID= `# insert your Discord user ID to access debugging commands` \
    -e PREFIX= `# insert a prefix for classic text-based commands` \
    --restart unless-stopped \
    misperception/vapbot # to pull the image from Docker Hub (recommended)
    # vapbot:latest # if you built the image from the repo
```

### venv

> You need to have Python installed as a prerequisite.

1. Clone the Github repository:

```bash
git clone https://github.com/misperception/vapbot
cd vapbot
```

2. Run `python -m venv venv` to create a virtual environment.

3. Modify the activation script of your preference in `venv/Scripts` to include the following:

> For `Activate.ps1`:

```ps1
$env:TOKEN=# insert your bot token from https://discord.com/developers/applications
$env:ID=# insert your Discord user ID to access debugging commands
$env:PREFIX=# insert a prefix for classic text-based commands
```

> For `activate.bat`:

```
set TOKEN=(insert your bot token from https://discord.com/developers/applications)
set ID=(insert your Discord user ID to access debugging commands)
set PREFIX=(insert a prefix for classic text-based commands)
```

> For `activate`:

```bash
TOKEN= # insert your bot token from https://discord.com/developers/applications
ID= # insert your Discord user ID to access debugging commands
PREFIX= # insert a prefix for classic text-based commands
```

You will need to run the activation script every time you want to start the bot, this is not an automated installation (unlike Docker).

## Commands

VapBot supports [Slash Commands](https://discord.com/blog/welcome-to-the-new-era-of-discord-apps), though conventional prefix commands are also supported. Configure the prefix during the installation.

> See [List of commands](commands.md).
