# Schwifty-Insights
This Python application delves into the Rick and Morty universe, leveraging the Rick and Morty API to analyze data about characters, episodes, and locations. It uncovers intriguing insights and relationships, exposing them through a well-designed RESTful API built with FastAPI.

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/Gal-Noy/Schwifty-Insights.git
   ```
3. Navigate to the project directory:
   ```
   cd Schwifty-Insights
   ```
5. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
7. Run the FastAPI application:
   ```
   uvicorn main:app --reload
   ```
9. Access the API at http://localhost:8000 in your web browser or API client, or visit Swagger documentation at at http://localhost:8000/docs.
10. Authenticate via `/auth/` endpoints (or using Swagger interface).
11. Refer to the API documentation for available endpoints and usage details.

## Features
- **Explore Insights** - Provides the ability to analyze data retrieved from the Rick and Morty API. Users can discover trends, relationships, and other interesting details about characters, episodes, and locations
- **Data Analysis** - The application performs in-depth analysis on the retrieved data leveraging AI algorhitms such as clustering. This analysis uncovers patterns and trends like relationships, species diversity, and dangerous locations based on character status.
- **Authentication** - API access is retricted by token authentication implemented with JWT, users must authenticate themselves before interacting with the data.
- **Caching** - Optimized performance by caching mechanism to store API responses, reducing the number of requests to the Rick and Morty API.
- **API Documentation** - The application provides documentation using Swagger, detailing all available endpoints, request parameters, and response formats.
- **Unit Tests** - The application includes unit tests that verify the correctness of the data analysis logic and API functionality. This ensures the reliability of the insights provided by the application.
- **Pagination** - Allows users to retrieve large datasets in smaller chunks. Users can set defalut page size in config.py.
- **Rate Limits** - Manages API requests to prevent overwhelming the Rick and Morty API and ensure fair usage. Can also be configured in config.py.
- **Dependencies** - List and manage project dependencies, including FastAPI, scikit-learn, numpy, and other required libraries for data analysis, API development, and testing.

## Usage Examples
### Analyzing Character Relationships
Utilize the ```/insights/characters-relationships``` endpoint to uncover clusters of characters based on their appearances throughout the series. Explore how characters are grouped together and discover potential relationships and interactions.

![image](https://github.com/Gal-Noy/Schwifty-Insights/assets/109943831/abeeb201-29a6-46be-80d3-66fa66945b89)

### Exploring Dimension Species Diversity
Dive into the ```/insights/dimension-species-diversity``` endpoint to understand species diversity across different dimensions. Investigate which dimensions exhibit higher species variety and uncover potential correlations between dimensions and species distribution.

![image](https://github.com/Gal-Noy/Schwifty-Insights/assets/109943831/e24ebdbd-9451-4ca9-8677-f58ab3182b94)

### Identifying Dangerous Locations
Use the ```/insights/dangerous-locations``` endpoint to identify locations with higher mortality rates among characters. Explore the correlation between character statuses (Alive, Dead, Unknown) and their respective locations, providing insights into the dangers characters face in different settings.

![image](https://github.com/Gal-Noy/Schwifty-Insights/assets/109943831/bc9ea6bb-12e5-43c7-964a-24a75091bb9c)

