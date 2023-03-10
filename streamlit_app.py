import streamlit
import pandas
import snowflake.connector
import requests
from urllib.error import URLError

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

def get_fruityvice_data (this_fruit_choice):
     fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
     fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
     return fruityvice_normalized
streamlit.dataframe(fruits_to_show)
try:
   fruit_choice = streamlit.text_input('What fruit would you like information about?')
   if not fruit_choice:
      streamlit.error('please select a fruit to get information')
   else:
      back_from_function = get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)
except URLError as e:
   streamlit.error()

#streamlit.write('The user entered ', fruit_choice)

streamlit.header("Fruityvice Fruit Advice!")


# write your own comment - what does this do?

# streamlit.stop()

def get_fuit_load_list():
    with my_cnx.cursor() as my_cur:
     my_cur.execute("SELECT * from fruit_load_list")
     return my_cur.fetchall()

if streamlit.button('Get fruit list list !'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fuit_load_list()
    my_cnx.close() 
    streamlit.dataframe(my_data_rows)


def insert_new_row_snowflake(new_fruit):
     with my_cnx.cursor() as my_cur:
          my_cur.execute("insert into  fruit_load_list values ('"+ new_fruit +"')")
          return 'Thanks for adding' + new_fruit
 
add_my_fuit = streamlit.text_input('What fruit would you like to add?')

if streamlit.button('Add a fuit to a list !'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_new_row_snowflake(add_my_fuit)
    my_cnx.close()
    streamlit.write(back_from_function)



