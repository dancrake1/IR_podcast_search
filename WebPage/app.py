import pandas as pd
import utils as ut
import os
from flask import Flask, render_template, request, jsonify, json, url_for, abort, redirect, session,flash
import pyterrier as pt
os.environ["JAVA_HOME"] = "/Library/Java/JavaVirtualMachines/jdk-20.jdk/Contents/Home"

#pyterrier configs
if not pt.started():
    pt.init()


# index = pd.read_csv('BM25_data.csv')
# data = pd.read_csv('/Users/danielcrake/Desktop/Masters/Year 2/Information Retrieval /Assignment/metadata.tsv', sep = '\t')
data = pd.read_pickle('/Users/danielcrake/Desktop/Masters/Year 2/Information Retrieval /Assignment/metadata.pkl')

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = '{Your Secret Key}'

'''
'''
@app.route("/", methods=["POST", "GET"])
def login():

    columns = ['show_name', 'episode_name', 'episode_description']
    if request.method == 'POST':
        query = request.form['query'].strip()
        processed_query = ut.pre_process(query)

        #indexed data
        index_ref = pt.IndexRef.of('./pd_index')
        searcher = pt.BatchRetrieve(index_ref, wmodel='DFReeKLIM')
        results = searcher.search(processed_query)

        docno_list = results.loc[:4, 'docid'].to_list()
        outputs = data.loc[data['docno'].isin(docno_list), columns]
        outputs = outputs.to_dict()

        # query_words = processed_query.split(' ')
        # top_results = index[query_words].sum(axis = 1).sort_values(ascending = False).index[:5].tolist()
        # outputs = data.loc[top_results, columns]
        # outputs = outputs.to_dict()

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
    description = outputs['episode_description'].to_list()
    episode = outputs['episode_name'].to_list()

    return render_template("quey_result.html",
                           query = processed_query,
                           show = show,
                           description = description,
                           episode = episode)

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000, debug=True)
