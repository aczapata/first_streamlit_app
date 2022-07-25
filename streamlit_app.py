
import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

def get_fruityvice_data(fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()

def insert_new_fruit(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('" + new_fruit+ "');")
    return 'Thanks for adding ' + new_fruit

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
                                        
streamlit.title("My parents New Healthy Diner")

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🥚 Hard-Boiled Free-Range Egg')
streamlit.text('🥑 Avocado Toast')
streamlit.header('🥭 Fruit Smoothie 🍇')

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
display_fruits = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(display_fruits)

streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
        fruityvice_normalized = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlit.error()
  
streamlit.header("The fruit load list contains:")
if streamlit.button('Get fruit load list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)

add_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add fruit'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_message = insert_new_fruit(add_fruit)
  my_cnx.close()
  streamlit.text(back_message)
