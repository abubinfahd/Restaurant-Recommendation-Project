from flask import Flask, jsonify, request, render_template
import pickle

# Manually set the path to the models folder and .pkl files
cosine_sim_path = 'models/cosine_sim.pkl'
df_sample_path = 'models/df_sample.pkl'

# Load your pre-trained models using pickle
with open(cosine_sim_path, 'rb') as c:
    cosine_sim = pickle.load(c)

with open(df_sample_path, 'rb') as d:
    df_sample = pickle.load(d)

# Ensure the function is defined before unpickling
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

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        restaurant_name = request.form.get('restaurant_name')  # Get the input restaurant name
        top_n = int(request.form.get('top_n', 5))  # Default to 5 recommendations

        # Get recommendations from the function defined above
        recommendations = get_content_based_recommendations(restaurant_name, top_n)
        
        # Check for error message in recommendations
        if isinstance(recommendations, dict) and "error" in recommendations:
            return jsonify(recommendations), 400

        return render_template('recommendations.html', restaurant_name=restaurant_name, recommendations=recommendations)

    return render_template('index.html')  # Render a form page on GET request

if __name__ == '__main__':
    app.run(debug=True)
