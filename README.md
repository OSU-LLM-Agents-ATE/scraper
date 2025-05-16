
# Scraper

## Project Identity

A high-performance, modular web scraping framework built for efficient and scalable data extraction.

**Team Members**
- Varun Bhat  
- Nathan Levites  
- Hao Zhu  

**Project Timeline/Status**
- Development: Completed  
- Testing: Completed   

---

## Value Proposition

### Problem Statement
Oregon State University’s College of Engineering has a large array of information available to its students, prospective students, faculty, and anyone else who might be interested in its resources. The university has done a great job in organizing this information into a series of web domains available to the public. However, this vast information isn’t exactly quick to navigate.

### Target Audience
 OSU Students/Faculty 


### Core Features and Benefits
- Multi-threaded architecture for performance  
- Docker support for fast deployment  
- Centralized, configurable URL management  
- Modular architecture to support various data sources and clients  
- Basic unit testing included  

### Comparison with Existing Solutions
The current existing solutions in place are navigating the Oregon State websites through clicking links or surfing the internet.

---

### Key Technologies
- Python 3  
    - concurrent.futures
- AWS
    - S3
    - DynamoDB

### Repository Overview

- **scraper.py**: Implements the core scraping logic, defining how data is extracted from web pages or APIs.
- **worker_pool.py**: Manages a pool of workers for concurrent scraping tasks, optimizing performance.
- **url_manager.py**: Centralized management of URLs, handling queueing, and duplicates.
- **config.py**: Configuration settings for the scraper, customizable to adjust scraping parameters.
- **constants.py**: Contains constants used throughout the code, improving maintainability.
- **clients.py**: Manages API or database clients, likely integrating with external services for data retrieval.
- **subdomains.txt**: A plain text file listing subdomains to be targeted in the scraping process.
- **tests/unit/test_scraper.py**: Contains unit tests for the scraper, ensuring core functionality works as expected.



### Installation Requirements
- Python

Install dependencies:
```bash
pip install -r requirements.txt
```

###  Running the Scraper
Edit `config.py` to configure targets and parameters.

Then run:
```bash
python main.py
```

### Docker Deployment
```bash
docker-compose up
```

### Running Unit Tests
```bash
pytest tests/unit/test_scraper.py
```

---

## License

MIT License
