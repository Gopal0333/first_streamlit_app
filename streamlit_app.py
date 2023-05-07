import pandas as pd
import streamlit
import requests
import snowflake.connector
from urllib.error import URLError

def get_fruityvice_data(this_fruity_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruity_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()
  
def insert_row(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("Insert into fruit_load_list values({0})".format(new_fruit))
    return 'Thanks for adding '+new_fruit

streamlit.title("My ParentS New Healthy Diner")
streamlit.header("Breakfast Menu")
streamlit.text("🥣 Omega 3 & Blueberry Oatmeal")
streamlit.text("🥗 Kale, Spinach & Rocket Smoothie")
streamlit.text("🐔 Hard Boiled Free-Range Egg")
streamlit.text("🥑🍞 Avocado Toast")


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

my_fruit_list = my_fruit_list.set_index("Fruit")

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruit_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruit_to_show)
streamlit.header("Fruityvice Fruit Advice!")
# streamlit.dataframe(my_fruit_list)
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please slelect a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()
  

# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
# streamlit.text(fruityvice_response.json())

# write your own comment -what does the next line do? 
# fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
# streamlit.dataframe(fruityvice_normalized)
# my_cur = my_cnx.cursor()
# my_cur.execute("select * from fruit_load_list")
# my_data_row = my_cur.fetchall()

streamlit.header("The fruit load list contains:")
if streamlit.button("Get fruit load list"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_row = get_fruit_load_list()
  streamlit.dataframe(my_data_row)
add_myfruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button("Add a fruit to the List"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  backfrom_function = insert_row(add_myfruit)
  streamlit.text(backfrom_function)
