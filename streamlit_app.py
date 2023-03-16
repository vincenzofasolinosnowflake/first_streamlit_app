import streamlit

streamlit.title("My Parents New Healty Diner")
streamlit.header("Breakfast Favorites")
streamlit.text("🥣 Omega  3 and Blueberry Oatmeal")
streamlit.text("🥗 Kale, Spinach and Rocket Smoothie")
streamlit.text("🐔 Hard-Boiled Free-Range Eggs")
streamlit.text("🥑🍞 Avocado Toast")

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)


import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)

# write your own comment -what does the next line do? 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
streamlit.dataframe(fruityvice_normalized)

import snowflake.connector streamlit.header("The fruit load list contains:")
def get_fruit_load_list():
   with my_cnx.cursor() as my_cur:
      my_cur.execute("select * from fruit_load_list")
      return my_cur.fetchall()
if streamlit.button('Get Fruit load list'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_data_rows = get_fruit_load_list()
   streamlit.dataframe(my_data_rows)
# allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
   with my_cnx.cursor() as my_cur:
      my_cur.execute("insert into fruit_load_list values ('" + new_fruit + "')")
      return "thanks for adding " + new_fruit
add_my_fruit = streamlit.text_input('what fruit would you like to add?')
if streamlit.button('add a fruit to the list'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   back_from_function = insert_row_snowflake(add_my_fruit)
   streamlit.text(back_from_function) #streamlit.header('Fruityvice Fruit Advice')
#    try:
#     fruit_choice1 = streamlit.text_input('what fruit would you like information about?')
#      if not fruit_choice1:
#         streamlit.error("PLease select a fruit to get information.")
#      else: 
#          fruityvice_response1 = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice1)
#          fruityvice_normalized1 = pandas.json_normalize(fruityvice_response1.json())
#          streamlit.dataframe(fruityvice_normalized1)    #    except URLError as e:
   #       streamlit.error() 
# Create therepeatable code block (called a function) : def
def get_fruityvice_data(this_fruit_choice):
   fruityvice_response1 = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
   fruityvice_normalized1 = pandas.json_normalize(fruityvice_response1.json())
   return fruityvice_normalized1
# New section to display fruityvice api responce 
streamlit.header('Fruityvice Fruit Advice')
try:
   fruit_choice1 = streamlit.text_input('what fruit would you like information about?')
   if not fruit_choice1:
      streamlit.error("PLease select a fruit to get information.")
   else: 
      back_from_function = get_fruityvice_data(fruit_choice1)
      streamlit.dataframe(back_from_function)
except URLError as e:
      streamlit.error()
