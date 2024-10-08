# Import python packages
import streamlit as st
import requests
import pandas as pd
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
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

# st.write(my_dataframe)
pd_df = my_dataframe.to_pandas()
# st.write(pd_df['FRUIT_NAME'])
# st.stop()

ingredients_list = st.multiselect(
    "Choose 5 options for your smoothie :"
    , pd_df['FRUIT_NAME']
    , max_selections=5
)

# st.dataframe(pd_df)


# st.write("You selected:", ingredients_list)
if ingredients_list:
    ingredients_string=''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write(search_on)
        
        st.subheader(fruit_chosen + 'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+search_on)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width = True)
        

    my_insert_stmt = """insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + title + """')"""
    TIME_TO_INSERT = st.button('Submit Order')
    if TIME_TO_INSERT:
        session.sql(my_insert_stmt).collect()
        st.success('Thank you '+title+', your Smoothie is ordered!', icon="✅")

