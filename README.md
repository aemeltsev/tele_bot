# tele_bot - Telegram Bot Integration Project

This project is a Telegram bot designed to integrate various API services to provide users with useful and up-to-date information. The bot ensures a secure and personalized interaction experience by requiring user authorization before granting access to its features.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Directly in Local Machine](#directly-in-local-machine)
  - [Build and Run Docker Container as a Service](#build-and-run-docker-container-as-a-service)
- [Configuration](#configuration)
- [API Integration](#api-integration)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **User Authentication**: Secure access to bot features. It may be better to use a more secure method like OAuth.
- **Use Geo API**: Get location information by place name. For detail, please refer to [Geocoding API](https://geocode.maps.co/).
- **Use Weather API**: Get real-time weather forecast by place coordinates. More informations about weather API can be found in [Weather Forecast API](https://open-meteo.com/en/docs).
- **Custom Alerts**: Set up personalized alerts and notifications (in progress).

## Installation

### Prerequisites

- **Python 3.7 or higher**: Ensure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).
    ```sh
    sudo apt update
    sudo apt install python3
    ```
- **pip (Python package installer)**: This comes with Python 3.7 and higher, so no additional installation is required.
    ```sh
    sudo apt install python3-pip
    ```
- **Telegram Bot API token**: You need to obtain this token from BotFather on Telegram. Follow the instructions [here](https://core.telegram.org/bots#botfather) to create a new bot and get your API token.

### Steps
1. **Clone the repository**:
    ```sh
    git clone https://github.com/aemeltsev/tele_bot.git
    cd tele_bot
    ```

2. **Create a virtual environment**:
    - A virtual environment helps manage dependencies and avoid conflicts between different projects.
    ```sh
    python -m venv venv
    ```
    - Activate the virtual environment:
    ```sh
    source venv/bin/activate
    ```

3. **Install dependencies**:
    - Install the required Python packages using pip:
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    - Create a `.env` file in the root directory of the project.
    - Add your valid Telegram Bot API token and other necessary environment variables to the `.env` file:
      ```env
      TOKEN=your_telegram_bot_token
      ADMIN_ID=your_admin_id
      GEOCODE_TOKEN=your_geocode_api_service_token
      DB_URL=your_database_path
      ```

5. **Add database file**:
    ```sh
    touch core/base/database.db
    ```

## Usage
### Directly in Local Machine
1. **Start the bot**:
    - Run the following command to start the bot:
    ```sh
    python main.py
    ```

2. **Interact with the bot**:
    - Open Telegram and search for your bot by its username.
    - Start a chat with the bot and use the available commands to interact with it.

### Available Commands

- **`/start`**: Start the bot and get a welcome message.
- **`/help`**: Get information about available commands.
- **`/weather <city>`**: Get the current weather information for the specified city.
- **`/login`**: Log in to the bot to access personalized features.
- **`/signup <token>`**: Sign up for the bot using your unique token.

### Build and Run Docker Container as a Service

1. **Build the Docker image**
    ```sh
    docker build -t tele_bot -f Dockerfile .
    ```
    Docker executes the instructions in the Dockerfile and creates an image with the tele_bot tag

2. **Run the Docker container**
    ```sh
    docker run -it --workdir /app -v $(pwd):/app --name tele_bot_container -p 8080:8080 tele_bot python bot.py
    ```
    Command starts a container from the tele_bot image. The container is started in interactive mode with a terminal (`-it`). The working directory inside the container is set to `/app`. The current directory on the host is mounted to the `/app` directory inside the container (`-v $(pwd):/app`).
    The container is given the name `tele_bot_container`. Port `8080` from the container is forwarded to port `8080` on the host. Inside the container, the python bot.py command.

3. **Build and run container**
    You could also build and run in one go for the first time
    ```sh
    docker-compose up -d
    ```
    or you could also force build every you want to apply change into the image
    ```sh
    docker-compose up -d --build
    ```

4. **Stop container**
    ```sh
    docker-compose down
    ```

## Configuration

You can configure the bot by modifying the `.env` file. Here are some of the configurable options:

- **`TOKEN`**: Set your Telegram Bot API token obtained from BotFather.
- **`ADMIN_ID`**: Set the admin ID for administrative purposes.
- **`GEOCODE_TOKEN`**: Set the token for the geocode API service.
- **`DB_URL`**: Configure the path to your database.

### Example `.env` File

```env
TOKEN=your_telegram_bot_token
ADMIN_ID=your_admin_id
GEOCODE_TOKEN=your_geocode_api_service_token
DB_URL=your_database_path
```

## API Integration
TODO

## Contributing
TODO

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact
TODO