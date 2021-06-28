from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px

import csv, re, operator

# from textblob import TextBlob

app = Flask(__name__)

person = {
    'name': '你好，我是李白',
    'first_name': '李',
    'last_name': '白',
    'address': '湖北省黄石市',
    'tel': '123456',
    'email': '12345@qq.com',
    # 'web': 'https://github.com',
    'web1': 'https://www.cnblogs.com/sowhat1412/p/12734246.html',
    'web2': 'https://dashboard.heroku.com',
    'web3': 'https://dashboard.heroku.com',
    'introduce': '性格开朗，乐于助人',
    'description': '',
    'hobby': '电子游戏 ',
    'social_media': [
        {
            'link': 'https://www.facebook.com/nono',
            'icon': 'fa-facebook-f'
        },
        {
            'link': 'https://github.com/nono',
            'icon': 'fa-github'
        },
        {
            'link': 'linkedin.com/in/nono',
            'icon': 'fa-linkedin-in'
        },
        {
            'link': 'https://twitter.com/nono',
            'icon': 'fa-twitter'
        }
    ],
    'img': 'img/img_nono.jpg',
    'experiences': [
        {
            'company': '某公司',
            'timeframe': '2019.1-2020.1',
            'job': '前端',
            'description': '网页'
        },
        {
            'company': '某某公司',
            'timeframe': '2020.1-2021.1',
            'job': '后端',
            'description': '商城'
        },
        {
            'company': '某某某公司',
            'timeframe': '2020.1-2021.6',
            'job': '全栈',
            'description': '购物程序'
        },
    ],
    'education': [
        {
            'university': 'Paris Diderot',
            'degree': 'Projets informatiques et Startégies d\'entreprise (PISE)',
            'description': 'Gestion de projets IT, Audit, Programmation',
            'mention': 'Bien',
            'timeframe': '2015 - 2016'
        },
        {
            'university': 'Paris Dauphine',
            'degree': 'Master en Management global',
            'description': 'Fonctions supports (Marketing, Finance, Ressources Humaines, Comptabilité)',
            'mention': 'Bien',
            'timeframe': '2015'
        },
        {
            'university': 'Lycée Turgot - Paris Sorbonne',
            'degree': 'CPGE Economie & Gestion',
            'description': 'Préparation au concours de l\'ENS Cachan, section Economie',
            'mention': 'N/A',
            'timeframe': '2010 - 2012'
        }
    ],
    'programming_languages': {
        'HMTL': ['fa-html5', '100'],
        'CSS': ['fa-css3-alt', '100'],
        'SASS': ['fa-sass', '90'],
        'JS': ['fa-js-square', '90'],
        'Wordpress': ['fa-wordpress', '80'],
        'Python': ['fa-python', '70'],
        'Mongo DB': ['fa-database', '60'],
        'MySQL': ['fa-database', '60'],
        'NodeJS': ['fa-node-js', '50']
    },
    'languages': {'French': 'Native', 'English': 'Professional', 'Spanish': 'Professional',
                  'Italian': 'Limited Working Proficiency'},
    'interests': ['Dance', 'Travel', 'Languages']
}


@app.route('/')
def cv(person=person):
    return render_template('indexa.html', person=person)


@app.route('/callback', methods=['POST', 'GET'])
def cb():
    return gm(request.args.get('data'))


@app.route('/chart')
def first_bar():
    return render_template('first_bar.html', graphJSON=gm())


@app.route('/chart1')
def first_boxplot():
    return render_template('first_boxplot.html', graphJSON=gm())


@app.route('/chart2')
def first_effectscatter():
    return render_template('first_effectscatter.html', graphJSON=gm())


@app.route('/chart3')
def first_funnel():
    return render_template('first_funnel.html', graphJSON=gm())


@app.route('/chart4')
def first_line():
    return render_template('first_line.html', graphJSON=gm())


@app.route('/chart5')
def first_map():
    return render_template('first_map.html', graphJSON=gm())


@app.route('/chart6')
def first_pie():
    return render_template('first_pie.html', graphJSON=gm())


@app.route('/chart7')
def first_polar():
    return render_template('first_polar.html', graphJSON=gm())


@app.route('/chart8')
def first_scatter():
    return render_template('first_scatter.html', graphJSON=gm())


@app.route('/chart9')
def first_worldcloud():
    return render_template('first_worldcloud.html', graphJSON=gm())


def gm(country='United Kingdom'):
    df = pd.DataFrame(px.data.gapminder())

    fig = px.line(df[df['country'] == country], x="year", y="gdpPercap")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


@app.route('/senti')
def main():
    text = ""
    values = {"positive": 0, "negative": 0, "neutral": 0}

    with open('ask_politics.csv', 'rt') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for idx, row in enumerate(reader):
            if idx > 0 and idx % 2000 == 0:
                break
            if 'text' in row:
                nolinkstext = re.sub(
                    r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''',
                    '', row['text'], flags=re.MULTILINE)
                text = nolinkstext

            blob = TextBlob(text)
            for sentence in blob.sentences:
                sentiment_value = sentence.sentiment.polarity
                if sentiment_value >= -0.1 and sentiment_value <= 0.1:
                    values['neutral'] += 1
                elif sentiment_value < 0:
                    values['negative'] += 1
                elif sentiment_value > 0:
                    values['positive'] += 1

    values = sorted(values.items(), key=operator.itemgetter(1))
    top_ten = list(reversed(values))
    if len(top_ten) >= 11:
        top_ten = top_ten[1:11]
    else:
        top_ten = top_ten[0:len(top_ten)]

    top_ten_list_vals = []
    top_ten_list_labels = []
    for language in top_ten:
        top_ten_list_vals.append(language[1])
        top_ten_list_labels.append(language[0])

    graph_values = [{
        'labels': top_ten_list_labels,
        'values': top_ten_list_vals,
        'type': 'pie',
        'insidetextfont': {'color': '#FFFFFF',
                           'size': '14',
                           },
        'textfont': {'color': '#FFFFFF',
                     'size': '14',
                     },
    }]

    layout = {'title': '<b>意见挖掘</b>'}

    return render_template('sentiment.html', graph_values=graph_values, layout=layout)


if __name__ == '__main__':
    app.run(debug=True, port=5000, threaded=True)
