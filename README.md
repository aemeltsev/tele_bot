# tele_bot - Telegram Bot Integration Project

This project is a Telegram bot designed to integrate various API services to provide users with useful and up-to-date information. The bot ensures a secure and personalized interaction experience by requiring user authorization before granting access to its features.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [API Integration](#api-integration)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **User Authorization**: Secure access to bot features.
- **Weather Updates**: Get real-time weather information.
- **Customizable Alerts**: Set up personalized alerts and notifications (In progress).
- **Multi-language Support**: Interact with the bot in multiple languages (In progress).

## Installation

### Prerequisites

- **Python 3.7 or higher**: Ensure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).
- **pip (Python package installer)**: This comes with Python 3.7 and higher, so no additional installation is required.
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
    - On macOS/Linux:
      ```sh
      source venv/bin/activate
      ```
    - On Windows:
      ```sh
      .\venv\Scripts\activate
      ```

3. **Install dependencies**:
    - Install the required Python packages using pip:
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    - Create a `.env` file in the root directory of the project.
    - Add your Telegram Bot API token and other necessary environment variables to the `.env` file:
      ```env
      TOKEN=your_telegram_bot_token
      ADMIN_ID=your_admin_id
      GEOCODE_TOKEN=your_geocode_api_service_token
      DB_URL=your_database_path
      ```

## Usage

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