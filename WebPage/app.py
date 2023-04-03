import pandas as pd
import utils as ut
from flask import Flask, render_template, request, jsonify, json, url_for, abort, redirect, session,flash
import requests

index = pd.read_csv('BM25_data.csv')
data = pd.read_csv('/Users/danielcrake/Desktop/Masters/Year 2/Information Retrieval /Assignment/metadata.tsv', sep = '\t')

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = '{Your Secret Key}'

'''
'''
@app.route("/", methods=["POST", "GET"])
def login():

    columns = ['show_name', 'show_description', 'publisher']
    if request.method == 'POST':
        query = request.form['query'].strip()
        processed_query = ut.pre_process(query)
        query_words = processed_query.split(' ')
        top_results = index[query_words].sum(axis = 1).sort_values(ascending = False).index[:5].tolist()
        outputs = data.loc[top_results, columns]

        outputs = outputs.to_dict()
        session['outputs'] = outputs
        session['processed_query'] = processed_query

        return redirect(url_for("results"))

    return render_template("query_search.html")


@app.route("/results/", methods = ["GET", "POST"])
def results():

    outputs = session.pop('outputs', None)
    outputs = pd.DataFrame(outputs)
    processed_query = session.pop('processed_query', None)

    show = outputs['show_name'].to_list()
    description = outputs['show_description'].to_list()
    publisher = outputs['publisher'].to_list()

    return render_template("quey_result.html",
                           query = processed_query,
                           show = show,
                           description = description,
                           publisher = publisher)

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000, debug=True)
