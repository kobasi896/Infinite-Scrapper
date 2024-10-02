# Infinite Scrapper

![License](https://img.shields.io/github/license/kobasi896/Infinite-Scrapper)
![Stars](https://img.shields.io/github/stars/kobasi896/Infinite-Scrapper?style=social)
![Forks](https://img.shields.io/github/forks/kobasi896/Infinite-Scrapper?style=social)

Infinite Scrapper is a versatile and efficient web scraping tool designed to handle large-scale data extraction tasks with ease. Whether you're gathering data for research, analysis, or automation, Infinite Scrapper provides the tools you need to extract, process, and manage web data seamlessly.

## Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setup Steps](#setup-steps)
- [Usage](#usage)
  - [Basic Usage](#basic-usage)
  - [Advanced Configuration](#advanced-configuration)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgements](#acknowledgements)

## Features

- **Scalable Scraping**: Handle thousands of pages with ease.
- **Customizable Parsers**: Easily define how to extract data from different websites.
- **Data Export**: Export scraped data in various formats like CSV, JSON, or directly to databases.
- **Proxy Support**: Rotate proxies to avoid IP bans and enhance scraping efficiency.
- **Error Handling**: Robust mechanisms to handle and retry failed requests.
- **Scheduling**: Automate scraping tasks at specified intervals.
- **Extensible Architecture**: Plug and play modules to extend functionality.

## Demo

![Infinite Scrapper Demo](https://github.com/kobasi896/Infinite-Scrapper/blob/main/demo/demo.gif?raw=true)

*Screenshot demonstrating the Infinite Scrapper in action.*

## Installation

### Prerequisites

Before you begin, ensure you have met the following requirements:

- **Operating System**: Windows, macOS, or Linux
- **Python**: Version 3.7 or higher
- **Git**: Installed on your system
- **pip**: Python package installer

### Setup Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/kobasi896/Infinite-Scrapper.git
    ```
2. **Navigate to the Project Directory**  
    ```bash
    cd Infinite-Scrapper
    ```
3. **Create a Virtual Environment (Optional but Recommended)**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
4. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
5. **Configure Environment Variables**
    ```bash
    # .env file example
    USER_AGENT="Your User Agent String"
    PROXY_LIST="path/to/proxy_list.txt"
    DATABASE_URL="your_database_connection_string"
    ```
6. **Run Migrations (If Applicable)**
    ```bash
    python manage.py migrate
    ```

### Usage
**Basic Usage**
To start scraping, run the main script:
```bash
python main.py --config config.yaml
```

***Parameters***
- --config: Path to the configuration file.

### Advanced Configuration
Infinite Scrapper uses a YAML configuration file to define scraping tasks. Below is an example of a **config.yaml**:
```bash
settings:
  user_agent: "Your User Agent String"
  proxies:
    - "http://proxy1.com:port"
    - "http://proxy2.com:port"
  delay: 2  # Delay between requests in seconds

tasks:
  - name: "Example Task"
    start_url: "https://example.com"
    max_pages: 100
    selectors:
      title: "h1.title::text"
      price: "span.price::text"
      image: "img::attr(src)"
    export:
      format: "csv"
      path: "data/example.csv"
```


***Running with Custom Configuration:***
```bash
python main.py --config path/to/your_config.yaml
```