# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """
)


title = st.text_input("Name on Smoothie: ")
st.write("The name on your smoothie will be: ", title)


cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)



ingredients_list = st.multiselect(
    "Choose 5 options for your smoothie :"
    , my_dataframe
    , max_selections=5
)

# st.write("You selected:", ingredients_list)
if ingredients_list:
    ingredients_string=''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    # st.write(ingredients_string, title)

    my_insert_stmt = """insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + title + """')"""
    TIME_TO_INSERT = st.button('Submit Order')
    if TIME_TO_INSERT:
        session.sql(my_insert_stmt).collect()
        st.success('Thank you '+title+', your Smoothie is ordered!', icon="✅")
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# st.text(fruityvice_response).json()

fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width = True)
