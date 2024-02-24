import streamlit as st
from youtube import get_channel_data
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table
from sqlalchemy.orm import sessionmaker

password = 'XEW2JfS5bPVKoL56'
uri = f"mongodb+srv://researchwork15:{password}@cluster0.dwfzypk.mongodb.net/?retryWrites=true&w=majority"

def add_to_mongodb(data):
    client = MongoClient(uri)
    db = client.get_database('youtube')
    collection = db["cluster0"]

    existing_data = collection.find_one({'id':data['id']})

    if existing_data:
        st.warning("Data already exists in the collection.")
    else:
        collection.insert_one(data)
        st.success("Data added to MongoDB!")

# Function to add data to SQLite database
def add_to_sqlite(channel_details):

    mysql_uri = 'mysql+pymysql://root:researchwork15@localhost:3306/youtube_db'
    engine = create_engine(mysql_uri, echo=True)

    metadata = MetaData()

    # # Define the table structure
    # channels_table = Table('channels', metadata,
    #                       Column('id', Integer, primary_key=True),
    #                       Column('channel_id', String, unique=True))

    # Create the table if it doesn't exist
    metadata.create_all(engine, checkfirst=True)

    # Check if the channel_id already exists in the SQLite database
    channel_id = channel_details['id']
    channel_table = Table('mytable', metadata, autoload_with=engine)
    existing_channel = engine.execute(f"SELECT * FROM channel WHERE channel_id = '{channel_id}'").first()

    if existing_channel:
        st.warning("Data already exists in the SQLite database.")
    else:
        # Data not found, so add it to the SQLite database
        with engine.connect() as connection:
            connection.execute(channel_table.insert().values(channel_id=channel_id))
        st.success("Added to the SQLite database!")

if 'clicked' not in st.session_state:
    st.session_state.clicked = False


def save_channel_details(channel_details):
    st.session_state.channel_details = channel_details

search_query = st.text_input('Enter your search query:', '')
if st.button('Search'):

    # Call the backend_search function with the entered query
    results = get_channel_data(search_query)

    # Display the results
    if results:
        st.session_state.clicked = True
        st.success('Channel Details:')
        channel_details = {}
        channel_details['id'] = results['id']
        channel_details['title'] = results['snippet']['title']
        channel_details['viewCount'] = results['statistics']['viewCount']
        channel_details['subscriberCount'] = results['statistics']['subscriberCount']
        channel_details['videoCount'] = results['statistics']['videoCount']
        save_channel_details(channel_details)
        st.write(channel_details)

    else:
        st.warning('No results found.')

if st.session_state.clicked:
    if st.button('Add to database'):
        add_to_mongodb(st.session_state.channel_details)
        add_to_sqlite(st.session_state.channel_details)
    
