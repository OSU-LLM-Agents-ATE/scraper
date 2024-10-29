
# Scraper Repository

## Project Overview

This project is a web scraping framework designed for efficient data extraction, utilizing multi-threaded processing and modular components for URL management and client handling. The repository includes configurations for Docker deployment and a basic testing suite.

## Requirements

To install the required dependencies, use:

```bash
pip install -r requirements.txt
```

**Note**: Docker configuration is also provided in `docker-compose.yml` for containerized deployment.

## Usage

1. **Configuration**: Edit `config.py` to set scraping parameters such as target URLs, API keys, or other configurations.
2. **Docker Deployment**:
   ```bash
   docker-compose up
   ```
3. **Running the Scraper**: Use `main.py` as the entry point for executing the scraper.
   ```bash
   python main.py
   ```


## Repository Structure

- **scraper.py**: Implements the core scraping logic, defining how data is extracted from web pages or APIs.
- **worker_pool.py**: Manages a pool of workers for concurrent scraping tasks, optimizing performance.
- **url_manager.py**: Centralized management of URLs, handling queueing, and duplicates.
- **config.py**: Configuration settings for the scraper, customizable to adjust scraping parameters.
- **constants.py**: Contains constants used throughout the code, improving maintainability.
- **clients.py**: Manages API or database clients, likely integrating with external services for data retrieval.
- **subdomains.txt**: A plain text file listing subdomains to be targeted in the scraping process.
- **tests/unit/test_scraper.py**: Contains unit tests for the scraper, ensuring core functionality works as expected.

## Testing

To run unit tests:

```bash
pytest tests/unit/test_scraper.py
```
