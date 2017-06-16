# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, redirect, url_for, session
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from blockchain import blockexplorer as be
from blockchain import statistics
from blockchain.exceptions import APIException
from datetime import datetime
from forms import SearchForm
import config

bootstrap = Bootstrap()
app = Flask(__name__)
moment = Moment(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        blocks = be.get_blocks()[:5]
    except APIException as e:
        print('Sorry, an API error has occurred ' + str(e))

    return render_template(
        'index.html',
        blocks=blocks,
        stats=get_stats(),
        current_time=datetime.now()
    )


@app.route('/blocks', methods=['GET', 'POST'])
def blocks():
    try:
        blocks = be.get_blocks()
        block_count = len(blocks)
    except APIException as e:
        print('Sorry, an API error has occurred ' + str(e))

    return render_template(
        'blocks.html',
        blocks=blocks,
        block_count=block_count
    )


@app.route('/block/<string:block>', methods=['GET', 'POST'])
def block(block):
    try:
        block = be.get_block(block)
    except APIException as e:
        print('Error ' + str(e))

    return render_template(
        'block.html',
        block=block
    )


@app.route('/block/<int:height>', methods=['GET', 'POST'])
def get_block_height(height):
    try:
        blocks = be.get_block_height(height)
        stats = get_stats()
        block_count = len(blocks)
    except APIException as e:
        print('Error ' + str(e))

    return render_template(
        'blocks_by_height.html',
        blocks=blocks,
        stats=stats,
        block_count=block_count
    )


@app.route('/block/<int:btime>', methods=['GET', 'POST'])
def get_block_by_time(btime):
    pass


@app.route('/tx/<string:tx>', methods=['GET', 'POST'])
def transaction(tx):
    pass


@app.route('/pools', methods=['GET', 'POST'])
def pools():
    pass


@app.route('/pool/<string:pool>', methods=['GET', 'POST'])
def pool(pool):
    pass


@app.route('/api', methods=['GET'])
def api_docs():
    pass


@app.route('/login', methods=['GET', 'POST'])
def login(username, password):
    pass


@app.route('/search', methods=['POST'])
def search():
    form = SearchForm(request.form)

    if request.method == 'POST' and form.validate():
        search = request.form['search'].strip()
        return redirect(url_for('results', query=search))
    else:
        return redirect(url_for('index'))


@app.route('/results/<string:query>', methods=['GET', 'POST'])
def results(query):
    search_results = None
    type = None

    form = SearchForm(request.form)
    if request.method == 'POST' and form.validate():
        if len(query) > 63:
            try:
                search_results = be.get_block(query)
                type = 'Block Info'
            except APIException as e:
                print('An API error has occurred ' + str(e))
        elif len(query) > 33:
            try:
                search_results = be.get_address(query)
                type = 'Address Info'
            except APIException as e:
                print('Error ' + str(e))
        else:
            try:
                search_results = be.get_block_height(query)
                type = 'Block Height Info'
            except APIException as e:
                print('Error ' + str(e))

    return render_template(
        'results.html',
        query=query,
        search_results=search_results,
        type=type
    )


def get_stats():
    stats = statistics.get()
    return stats


@app.template_filter('datetime')
def convert_unixtime(unixtime, format='medium'):
    n = datetime.fromtimestamp(
        int(unixtime)).strftime('%Y-%m-%d %H:%M:%S')
    return n


if __name__ == '__main__':
    app.run(
        port=config.PORT,
        debug=config.DEBUG
    )
