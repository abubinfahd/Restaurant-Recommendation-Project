import streamlit as st
import pickle
import pandas as pd

# Manually set the path to the models folder and .pkl files
cosine_sim_path = r'D:\Restaurant Recommendation Project\models\cosine_sim.pkl'
df_sample_path = r'D:\Restaurant Recommendation Project\models\df_sample.pkl'

# Load your pre-trained models using pickle
with open(cosine_sim_path, 'rb') as c:
    cosine_sim = pickle.load(c)

with open(df_sample_path, 'rb') as d:
    df_sample = pickle.load(d)

# Define the recommendation function
def get_content_based_recommendations(restaurant_name, top_n=5):
    # Normalize the input to handle case insensitivity
    restaurant_name = restaurant_name.strip().lower()
    
    # Find matching restaurants (case insensitive search)
    matching_restaurants = df_sample[df_sample['name'].str.lower() == restaurant_name]
    
    # Check if the restaurant exists in the dataset
    if matching_restaurants.empty:
        return {"error": f"{restaurant_name} not found in the dataset."}
    
    # If multiple restaurants match, you can handle it or just take the first match
    idx = matching_restaurants.index[0]
    
    # Get similarity scores for the matched restaurant
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:]  # Exclude the input restaurant from recommendations
    
    recommended_restaurants = []
    for i in sim_scores:
        restaurant = df_sample['name'].iloc[i[0]]
        if restaurant != restaurant_name and restaurant not in recommended_restaurants:
            recommended_restaurants.append(restaurant)
        
        if len(recommended_restaurants) == top_n:
            break
    
    return recommended_restaurants

# Streamlit App
st.title("Restaurant Recommendation System")

# Input section
restaurant_name = st.text_input("Enter the restaurant name:")
top_n = st.slider("Number of recommendations:", min_value=1, max_value=10, value=5)

# Display recommendations
if st.button("Get Recommendations"):
    if restaurant_name:
        recommendations = get_content_based_recommendations(restaurant_name, top_n)
        
        if isinstance(recommendations, dict) and "error" in recommendations:
            st.error(recommendations["error"])
        else:
            st.write(f"Recommendations for '{restaurant_name}':")
            for i, restaurant in enumerate(recommendations, 1):
                st.write(f"{i}. {restaurant}")
    else:
        st.error("Please enter a restaurant name.")

