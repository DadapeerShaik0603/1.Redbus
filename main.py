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

# Utility function: Load image and encode it as base64
def load_image_as_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except Exception as e:
        st.error(f"Error loading image: {e}")
        return ""

# Utility function: Establish connection to the MySQL database
def get_connection():
    try:
        return connector.connect(
            host="127.0.0.1",
            user="root",
            passwd="123456789",
            database="redbus"
        )
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None

# Fetch route names starting with a specific letter
def fetch_route_names(connection, starting_letter):
    query = """
        SELECT DISTINCT Route_Name 
        FROM bus_routes 
        WHERE Route_Name LIKE %s 
        ORDER BY Route_Name
    """
    try:
        return pd.read_sql(query, connection, params=(f"{starting_letter}%",))['Route_Name'].tolist()
    except Exception as e:
        st.error(f"Error fetching route names: {e}")
        return []

# Fetch data based on selected Route_Name and sorting preferences
def fetch_data(connection, route_name, price_sort_order):
    order = "ASC" if price_sort_order == "Low to High" else "DESC"
    query = f"""
        SELECT * 
        FROM bus_routes 
        WHERE Route_Name = %s 
        ORDER BY Price {order}
    """
    try:
        return pd.read_sql(query, connection, params=(route_name,))
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

# Filter data by Star_Rating and Bus_Type
def filter_data(df, star_ratings, bus_types):
    try:
        return df[df['Star_Rating'].isin(star_ratings) & df['Bus_Type'].isin(bus_types)]
    except Exception as e:
        st.error(f"Error filtering data: {e}")
        return pd.DataFrame()

# Main Streamlit app function
def main():
    # Load background image
    background_image = load_image_as_base64("C:/Projects/Redbus/Volvo bus.png")

    # Apply custom CSS for background image
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

    st.markdown('<div class="main-header">🚌 Bus Dekho - Find Your Bus</div>', unsafe_allow_html=True)
    st.divider()

    # Connect to the database
    connection = get_connection()
    if not connection:
        return

    try:
        # Sidebar inputs
        with st.sidebar:
            st.header("🔍 Search Routes")
            starting_letter = st.text_input("Enter starting letter of Route Name", "A")

        # Fetch and display route names
        if starting_letter:
            route_names = fetch_route_names(connection, starting_letter.upper())
            if route_names:
                with st.sidebar:
                    selected_route = st.radio("Select Route Name", route_names)

                if selected_route:
                    # Price sorting preferences
                    with st.sidebar:
                        price_sort_order = st.selectbox("Sort Buses by Price", ["Low to High", "High to Low"])

                    # Fetch and display data for the selected route
                    data = fetch_data(connection, selected_route, price_sort_order)
                    if not data.empty:
                        st.markdown('<div class="main-content">', unsafe_allow_html=True)
                        st.subheader(f"Route: {selected_route}")
                        st.dataframe(data, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                        # Advanced filters
                        st.markdown("### 🔧 Advanced Filters")
                        col1, col2 = st.columns(2)
                        with col1:
                            star_ratings = data['Star_Rating'].unique().tolist()
                            selected_ratings = st.multiselect("Filter by Star Rating", star_ratings)
                        with col2:
                            bus_types = data['Bus_Type'].unique().tolist()
                            selected_bus_types = st.multiselect("Filter by Bus Type", bus_types)

                        if selected_ratings and selected_bus_types:
                            filtered_data = filter_data(data, selected_ratings, selected_bus_types)
                            st.markdown("### 🎯 Filtered Results")
                            st.dataframe(filtered_data, use_container_width=True)
                    else:
                        st.warning(f"No data found for route: {selected_route}")
            else:
                st.warning("No routes found starting with the specified letter.")

    finally:
        connection.close()

# Run the app
if __name__ == "__main__":
    main()
