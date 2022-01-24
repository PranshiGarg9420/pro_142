from flask import Flask, jsonify, request
from numpy import rec
from pro_storage import all_articles, liked_articles, not_liked_articles
from pro_demographic import output
from pro_content_bases import get_recommendations

app= Flask(__name__)

@app.route('/get-articles')
def get_article():
    artcle_data={
        "url": all_articles[0][11],
        "title": all_articles[0][12],
        "text": all_articles[0][13],
        "lang": all_articles[0][14],
        "total_events": all_articles[0][15]
    }
    return jsonify({
       'data': artcle_data,
       'status':'success' 
    })

@app.route("/liked-article", methods=["POST"])
def liked_article():
    article = all_articles[0]
    liked_articles.append(article)
    all_articles.pop(0)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/unliked-article", methods=["POST"])
def unliked_article():
    article = all_articles[0]
    not_liked_articles.append(article)
    all_articles.pop(0)
    return jsonify({
        "status": "success"
    }), 201

@app.route('/get-popular-articles')
def get_popular_articles():
    popular_articles=[]
    for article in output:
        temp_list={
            "url": article[0],
            "title": article[1],
            "text": article[2],
            "lang": article[3],
            "total_events": article[4]
        }
        popular_articles.append(temp_list)
    return jsonify({
        "data": popular_articles,
        "status": "success"
    }), 200

@app.route('/get-recommended-articles')
def get_recomended_articles():
    recommended_articles=[]
    for liked_article in liked_articles:
        output= get_recommendations(liked_article[4])
        for data in output:
            recommended_articles.append(data)
    import itertools
    recommended_articles.sort()
    recommended_articles= list(recommended_articles for recommended_articles,_ in itertools.groupby(recommended_articles))
    article_data=[]
    for recommended in recommended_articles:
        rec_list={
            'url':recommended[0],
            'title':recommended[1],
            'text':recommended[2],
            'lang':recommended[3],
            'total_events':recommended[4]
        }
        article_data.append(rec_list)
        return jsonify({
        "data": article_data,
        "status": "success"
    }), 200