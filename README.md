

# **Bus Dekho: Dynamic Bus Data Scraping, Storage, and Visualization Tool**

## **Overview**
This project automates the process of scraping, storing, and visualizing bus route data from the **RedBus** website. Using **Selenium**, the script extracts dynamic bus data, stores it in a **MySQL database**, and visualizes it interactively through a **Streamlit** dashboard. The project provides an efficient way for users to explore bus routes, schedules, prices, seat availability, and ratings in a user-friendly and visually appealing interface.

---

## **Project Structure**

### **Part 1: Data Scraping**

#### **Libraries Used**
- **Selenium**: For automating browser interactions to scrape dynamic content.
- **Pandas**: For organizing and processing the scraped data.
- **time**: For managing dynamic page loading waits.
  
#### **Process Overview**
1. **Driver Initialization**:
   - Uses Selenium to initialize the ChromeDriver and set up the web scraping environment.
  
2. **Page Navigation**:
   - Opens the RedBus URL and handles pagination to scrape multiple pages of bus routes.

3. **Data Extraction**:
   - Scrapes bus details such as route names, bus types, prices, seat availability, departure/arrival times, and ratings.
   - Handles dynamic content loading, pop-ups, and scrolling through the page using Selenium.

4. **CSV Output**:
   - Extracted data is saved to a CSV file (`bus_routes.csv`) for later use.

---

### **Part 2: Data Storage**

#### **Tools Used**
- **MySQL Database**: For structured and persistent data storage.
- **MySQL-Connector-Python**: To interface with the MySQL database.

#### **Process Overview**
1. **CSV to Database Integration**:
   - The script reads the `bus_routes.csv` file and imports the data into a MySQL database.
   - Creates a table (`bus_routes`) if it does not already exist.

2. **Error Handling**:
   - Handles missing or null values by dropping incomplete rows to maintain data integrity.
   - Logs any database connection issues or query failures.

---

### **Part 3: Data Visualization**

#### **Libraries Used**
- **Streamlit**: For creating an interactive and user-friendly dashboard.
- **Pandas**: To process and display data retrieved from the MySQL database.
- **Base64**: For encoding custom images used as backgrounds in the dashboard.

#### **Visualization Features**
- **Search Functionality**:
  - Users can search for bus routes by the starting letter of the route name.
  
- **Sorting and Filtering**:
  - Sort buses by price (Low to High or High to Low).
  - Filter by star ratings (e.g., 4-star or higher).
  - Filter by bus type (e.g., AC, Sleeper).

- **Interactive Table**:
  - Displays all bus details (name, route, prices, timings, seat availability) in a sortable, filterable table.

---

### **Part 4: Streamlit Application**

#### **Imports**
- **Streamlit**: For building the web application.
- **Pandas**: For data manipulation.
- **MySQL-Connector-Python**: For database operations.
- **time**: For managing page loading waits.

#### **Data Retrieval and Storage**
1. **Fetch Data from MySQL**:
   - Retrieves the bus data stored in the MySQL database and loads it into Pandas DataFrames.

2. **Visualization Functions**:
   - Functions to create dynamic visualizations based on the bus data (e.g., sorting, filtering, and displaying data).

#### **User Interface**
- **Interactive Dashboard**:
   - The Streamlit interface allows users to explore bus route data interactively by searching, filtering, and sorting based on different criteria.

---

## **Usage**

### **1. Setup Environment**

#### **Prerequisites**
- **Python 3.8+** installed.
- **MySQL Server** set up and running on your system.
- **ChromeDriver** available for Selenium.

### **2. MySQL Configuration**
1. **Create the Database**:
   - Open the MySQL shell and create a new database:
2. **Update Database Credentials**:
   - Modify the connection parameters in the script as per your MySQL setup.

### **3. Running the Project**
- Start the Streamlit application to visualize and interact with the bus data.
---

## **Dashboard Features**

- **Route Search**:
  - Search for routes starting with a specific letter.
  
- **Filters and Sorting**:
  - Filter by star ratings, bus types, and sort by price or availability.

- **Data Table**:
  - View bus details (e.g., seat availability, departure/arrival times, prices) in a sortable, filterable table.

---

## **Assumptions and Limitations**

1. **Website Structure**: 
   - Assumes the structure of the RedBus website remains constant. Any changes to the site may require updates to the scraping code.

2. **Dynamic Content**: 
   - The dynamic content is loaded using explicit waits and `time.sleep()`, which may not work under all network conditions.

3. **Scraping Limitations**: 
   - Currently, the scraper only extracts data from the first five pages of bus routes, though this can be extended.

4. **Local Database Setup**:
   - The script is configured to work with a local MySQL database. For remote databases, the connection parameters will need to be updated.

---

## **Conclusion**

**Bus Dekho** provides a complete solution for scraping, storing, and visualizing bus route data from **RedBus**. With its interactive dashboard, users can easily explore bus schedules, seat availability, pricing, and ratings. This project combines web scraping, database management, and data visualization to create a seamless user experience and can be adapted for other dynamic web scraping tasks.

---
