import requests

STEAM_SEARCH_URL = "https://store.steampowered.com/api/storesearch/"
STEAM_REVIEWS_URL = "https://store.steampowered.com/appreviews/{app_id}"
REDDIT_SEARCH_URL = "https://www.reddit.com/search.json"

def reddit_reviews(game_name: str, limit: int = 5):
    headers = {"User-Agent": "GameReviewBot/1.0"}
    params = {
        "q": f"{game_name} review OR worth it OR impressions",
        "limit": limit,
        "sort": "relevance",
        "t": "year",
    }

    res = requests.get(REDDIT_SEARCH_URL, headers=headers, params=params, timeout=10).json()

    posts = []
    for child in res.get("data", {}).get("children", []):
        data = child["data"]
        posts.append({
            "title": data.get("title"),
            "subreddit": data.get("subreddit"),
            "score": data.get("score"),
            "comments": data.get("num_comments"),
            "url": "https://reddit.com" + data.get("permalink", ""),
            "selftext": (data.get("selftext") or "")[:400],
        })

    return {
        "source": "reddit",
        "query": game_name,
        "posts": posts
    }


def steam_search_game_id(game_name: str):
    params = {
        "term": game_name,
        "l": "english",
        "cc": "us"
    }
    headers = {
        "User-Agent": "GameReviewBot/1.0"
    }

    res = requests.get(STEAM_SEARCH_URL, params=params, headers=headers, timeout=10).json()
    items = res.get("items", [])

    if not items:
        return None

    return items[0]["id"]


def steam_get_reviews(app_id: int, limit: int = 8):
    params = {
        "json": 1,
        "num_per_page": limit,
        "language": "english",
        "purchase_type": "all"
    }
    headers = {
        "User-Agent": "GameReviewBot/1.0"
    }

    res = requests.get(
        STEAM_REVIEWS_URL.format(app_id=app_id),
        params=params,
        headers=headers,
        timeout=10
    ).json()

    summary = res.get("query_summary", {})

    reviews = []
    for r in res.get("reviews", []):
        reviews.append({
            "text": r.get("review", "")[:500],
            "recommended": r.get("voted_up"),
            "playtime_hours": round(r.get("author", {}).get("playtime_forever", 0) / 60, 1),
        })

    return {
        "rating_desc": summary.get("review_score_desc"),
        "total_reviews": summary.get("total_reviews"),
        "positive_reviews": summary.get("total_positive"),
        "negative_reviews": summary.get("total_negative"),
        "recent_reviews": reviews
    }


def steam_reviews(game_name: str):
    app_id = steam_search_game_id(game_name)

    if not app_id:
        return {"error": f"Game not found on Steam: {game_name}"}

    data = steam_get_reviews(app_id)
    data["steam_app_id"] = app_id
    print(f"Fetched Steam reviews for '{game_name}' (App ID: {app_id})")
    print(f"Summary: {data['rating_desc']} with {data['total_reviews']} total reviews")
    print(data)
    return data
