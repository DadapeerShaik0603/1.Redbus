import streamlit as st
import base64
from mysql import connector
import pandas as pd

# Set Streamlit page configuration
st.set_page_config(
    page_title="Bus Dekho",
    page_icon="🚌",
    layout="wide",
)

# Function to load image and encode it as base64
def load_image_as_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Connect to MySQL database
def get_connection():
    try:
        connection = connector.connect(
            host='127.0.0.1',
            user='root',
            passwd='123456789',
            database='redbus'
        )
        return connection
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None

# Function to fetch route names starting with a specific letter, arranged alphabetically
def fetch_route_names(connection, starting_letter):
    query = (
        "SELECT DISTINCT Route_Name FROM bus_routes "
        "WHERE Route_Name LIKE %s ORDER BY Route_Name"
    )
    try:
        route_names = pd.read_sql(query, connection, params=(f"{starting_letter}%",))['Route_Name'].tolist()
        return route_names
    except Exception as e:
        st.error(f"Error fetching route names: {e}")
        return []

# Function to fetch data from MySQL based on selected Route_Name and price sort order
def fetch_data(connection, route_name, price_sort_order):
    price_sort_order_sql = "ASC" if price_sort_order == "Low to High" else "DESC"
    query = (
        "SELECT * FROM bus_routes WHERE Route_Name = %s "
        f"ORDER BY Star_Rating DESC, Price {price_sort_order_sql}"
    )
    try:
        df = pd.read_sql(query, connection, params=(route_name,))
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

# Function to filter data based on Star_Rating and Bus_Type
def filter_data(df, star_ratings, bus_types):
    try:
        filtered_df = df[df['Star_Rating'].isin(star_ratings) & df['Bus_Type'].isin(bus_types)]
        return filtered_df
    except Exception as e:
        st.error(f"Error filtering data: {e}")
        return pd.DataFrame()

# Main Streamlit app
def main():
    # Load and encode the background image
    image_path = "C:/Projects/Redbus/Volvo bus.png"
    background_image = load_image_as_base64(image_path)

    # Add custom CSS for background image
    st.markdown(
        f"""
        <style>
        .main-content {{
            background-image: url('data:image/png;base64,{background_image}');
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
            padding: 200px;
            border-radius: 100px;
            color: white;
        }}
        .main-header {{
            font-size: 36px;
            font-weight: bold;
            text-align: center;
            color: #FF4B4B;
        }}
        .sidebar .sidebar-content {{
            background-color: #f0f2f6;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="main-header">🚌 Bus Dekho-Grab Your Bus Details</div>', unsafe_allow_html=True)
    st.divider()

    connection = get_connection()

    if connection:
        try:
            # Sidebar section for inputs
            with st.sidebar:
                st.header("🔍 Search  Routes")
                starting_letter = st.text_input('Enter starting letter of Route Name', 'A')

            # Fetch route names starting with the specified letter
            if starting_letter:
                route_names = fetch_route_names(connection, starting_letter.upper())

                if route_names:
                    # Display available route names in a sidebar
                    with st.sidebar:
                        selected_route = st.radio('Select Route Name', route_names)

                    if selected_route:
                        # Sidebar options for sorting preference
                        with st.sidebar:
                            price_sort_order = st.selectbox('Sort by Price', ['Low to High', 'High to Low'])

                        # Fetch data based on selected Route_Name and price sort order
                        data = fetch_data(connection, selected_route, price_sort_order)

                        if not data.empty:
                            # Main area - Display data table with background
                            st.markdown('<div class="main-content">', unsafe_allow_html=True)
                            st.subheader(f"Data for Route: {selected_route}")
                            st.dataframe(data, use_container_width=True)
                            st.markdown('</div>', unsafe_allow_html=True)

                            # Advanced filtering options
                            st.markdown("### 🔧 Advanced Filters")
                            col1, col2 = st.columns(2)
                            with col1:
                                star_ratings = data['Star_Rating'].unique().tolist()
                                selected_ratings = st.multiselect('Filter by Star Rating', star_ratings)
                            with col2:
                                bus_types = data['Bus_Type'].unique().tolist()
                                selected_bus_types = st.multiselect('Filter by Bus Type', bus_types)

                            if selected_ratings and selected_bus_types:
                                filtered_data = filter_data(data, selected_ratings, selected_bus_types)
                                st.markdown("### 🎯 Filtered Results")
                                st.dataframe(filtered_data, use_container_width=True)
                        else:
                            st.error(f"No data found for Route: {selected_route} with the specified price sort order.")
                else:
                    st.warning("No routes found starting with the specified letter.")
                
        finally:
            connection.close()

if __name__ == '__main__':
    main()
