from fastapi import FastAPI
from typing import List
import joblib
from pydantic import BaseModel
import json

app = FastAPI()

class RecommendationRequest(BaseModel):
    user_id: int
    post_title: str

@app.get("/recommendations/")
async def get_recommendations(recommendation_request: RecommendationRequest):
    model = joblib.load("recommendation_model.pkl")

    user_id = recommendation_request.user_id
    post_title = recommendation_request.post_title

    # Use the recommendation model to get recommendations for this user and post
    recommended_posts = model.get_recommendations(user_id, post_title)

    # Return the recommended posts, along with the number of recommendations
    return {
        "recommended_posts": recommended_posts,
        "num_recommendations": len(recommended_posts)
    }
