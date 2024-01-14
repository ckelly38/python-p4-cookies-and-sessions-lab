#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0;
    #print(session['page_views']);
    return make_response({'message': '200: Successfully cleared session data.'}, 200);

@app.route('/articles')
def index_articles():
    return make_response([a.to_dict() for a in Article.query.all()], 200);

@app.route('/articles/<int:id>')
def show_article(id):
    #print(session.keys());
    #print(session.values());
    #print(len(session.keys()));
    #session["page_views"] = -1;
    #print("page_views" in session.keys());
    try:
        session["page_views"] = (session["page_views"] + 1) or 0;
    except Exception as err:
        #print("set page_views to zero!");
        session["page_views"] = 1;
    #print(session["page_views"]);
    #print(session.get("page_views"));
    #print(type(session["page_views"]));
    #print((3 < session["page_views"]));
    if (3 < session["page_views"]):
        session["page_views"] = 4;
        #print("sent out error max views reached!");
        return make_response({"message": "Maximum pageview limit reached"}, 401);
    else:
        #print("printed out the article!");
        return make_response(Article.query.filter_by(id=id).first().to_dict(), 200);

if __name__ == '__main__':
    app.run(port=5555)
