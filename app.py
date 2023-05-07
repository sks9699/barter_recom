from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import pymongo
import json
from bson import ObjectId


app = FastAPI()


class Post(BaseModel):
    id: str


# Load the recommendation model
with open('recommendation_model.sav', 'rb') as f:
    tfidf, cosine_sim, data = pickle.load(f)

# Define a function to generate recommendations based on a post title


def get_recommendations(post_id, data2, cosine_sim, num_recommendations=6):
    # Get the index of the post that matches the ID
    # convert the string to an ObjectId
    id_obj = ObjectId(post_id)

    if id_obj not in data['_id'].values:
        raise ValueError(f"Post id {id_obj} not found in DataFrame")

    idx = data2[data2['_id'] == id_obj].index[0]

    # Get the cosine similarity scores for all posts
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the posts by similarity score
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices of the top N similar posts (excluding the query post itself)
    top_indices = [i[0] for i in sim_scores[1:num_recommendations+1]]

    # Return the IDs of the top N similar posts as strings
    return [str(data2.loc[i, '_id']) for i in top_indices]




# Connect to the MongoDB database
client = pymongo.MongoClient(
    f"mongodb+srv://akshay_jangra:Adiyta12345@cluster0.wenn6ur.mongodb.net/?retryWrites=true&w=majority")
db = client['Barter']
posts = db['posts']


@app.post('/recommend')
async def recommendations(request_data: Post):
    # Get the post title from the request
    
    input_data =request_data.json()
    input_dict = json.loads(input_data)

    post_id = str(input_dict['title'])

    
    # Generate recommendations based on the post title
    recommendations = get_recommendations(post_id, data, cosine_sim)

    return {'recommendations': recommendations}
