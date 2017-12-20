# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, redirect, flash, url_for, session
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_misaka import Misaka
from blockchain import blockexplorer as be
from blockchain import statistics
from blockchain.exceptions import APIException
from flask_qrcode import QRcode
from bs4 import BeautifulSoup
from datetime import datetime
from forms import SearchForm, AddressSearchForm, RegistrationForm
import config
import requests
import collections


bootstrap = Bootstrap()
app = Flask(__name__, static_url_path='')
moment = Moment(app)
QRcode(app)
Misaka(app)

app.secret_key = config.SECRET_KEY
app.api_code = config.API_KEY

MiningPool = collections.namedtuple('MiningPool', 'rank, name, p_total, h_rate, n_blocks, e_blocks, eb_percent, '
                                                  'b_size, avg_tx_fees, tx_fees_reward')


@app.route('/', methods=['GET', 'POST'])
def index():
    blocks = []
    block_count = 0
    stats = {}

    try:
        blocks = be.get_blocks(api_code=app.api_code)[:5]
        block_count = len(blocks)
        stats = get_stats()
    except APIException as e:
        flash('Sorry, we had a problem contacting the blockchain.info API.  Please try again later.')

    return render_template(
        'index.html',
        blocks=blocks,
        block_count=block_count,
        stats=stats,
        current_time=datetime.now().strftime('LLL')
    )


@app.route('/blocks', methods=['GET', 'POST'])
def blocks():
    blocks = []
    block_count = 0

    try:
        blocks = be.get_blocks(api_code=app.api_code)
        block_count = len(blocks)
    except APIException as e:
        flash('Sorry, we had a problem contacting the blockchain.info API.  Please try again later.')

    return render_template(
        'blocks.html',
        blocks=blocks,
        block_count=block_count
    )


@app.route('/block/<string:block>', methods=['GET', 'POST'])
def block(block):
    try:
        block = be.get_block(block, api_code=app.api_code)
        transactions = block.transactions
    except APIException as e:
        print('Error ' + str(e))

    return render_template(
        'block.html',
        block=block,
        transactions=transactions,
        current_time=datetime.now().strftime('LLL')
    )


@app.route('/block/<int:height>', methods=['GET', 'POST'])
def get_block_height(height):
    try:
        blocks = be.get_block_height(height, api_code=app.api_code)
        if blocks:
            block_height = blocks[0].height
        stats = get_stats()
        block_count = len(blocks)
    except APIException as e:
        print('Error ' + str(e))

    return render_template(
        'blocks_by_height.html',
        blocks=blocks,
        stats=stats,
        block_count=block_count,
        block_height=block_height,
        current_time=datetime.now().strftime('LLL')
    )


@app.route('/address/<string:address>', methods=['GET', 'POST'])
def get_address(address):
    try:
        addr = be.get_address(address, api_code=app.api_code)
        tx = addr.transactions
    except APIException as e:
        print('Error ' + str(e))

    return render_template(
        'address.html',
        addr=addr,
        tx=tx,
        current_time=datetime.now().strftime('LLL')
    )


@app.route('/address', methods=['GET', 'POST'])
def address():
    form = AddressSearchForm(request.form)

    if request.method == 'POST':
        addr = request.form['addr'].strip()
        try:
            clean_addr = str(addr)
            if len(clean_addr) == 34:
                try:
                    address = be.get_address(clean_addr, api_code=app.api_code)

                    return render_template(
                        '_address.html',
                        address=address,
                        search_value=addr,
                        current_time=datetime.now().strftime('LLL')
                    )

                except APIException as e:
                    flash('API Error', 'warning')
                    return redirect(url_for('address'))
            else:
                message = 'The Bitcoin address is malformed.  Please check your data and try again.'
                flash(message, 'danger')
                redirect(url_for('address'))
        except (ValueError, TypeError) as err:
            message = 'An error has occurred: ' + str(err)
            flash(message, 'danger')
            return redirect(url_for('address'))
    else:
        return render_template(
            '_address.html',
            form=form,
            current_time=datetime.now().strftime('LLL')
        )


@app.route('/tx/<string:hash>', methods=['GET', 'POST'])
def tx(hash):
    try:
        tx = be.get_tx(hash, api_code=app.api_code)
        blk = be.get_block_height(tx.block_height, api_code=app.api_code)
    except APIException as e:
        message = 'There has been an API Error.'
        flash(message, 'danger')
        return redirect(url_for('index'))

    return render_template(
        'transaction.html',
        tx=tx,
        block=blk,
        current_time=datetime.now().strftime('LLL')
    )


@app.route('/pools', methods=['GET', 'POST'])
def pools():
    pools = list()
    url = config.STATS_URL
    hdr = {'user-agent': 'Mozilla/5.0 (Linux i686)'}
    r = requests.get(url, headers=hdr)
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find('table', {'class': 'pool-panel-share-table'})
    rows = table.find_all('tr')

    for idx, row in enumerate(rows):
        if idx != 0:
            columns = row.find_all('td')
            cols = [element.text.strip() for element in columns]
            pools.append([element for element in cols if element])

    return render_template(
        'pools.html',
        current_time=datetime.now().strftime('LLL'),
        pools=pools,
    )


@app.route('/pool/<string:pool>', methods=['GET', 'POST'])
def pool(pool):
    blocks = None
    block_count = None
    try:
        blocks = be.get_blocks(pool_name=pool, api_code=app.api_code)
        block_count = len(blocks)
    except APIException as e:
        message = 'Sorry, an API exception occurred ' + str(e)
        flash(message, 'danger')
        return redirect(url_for('index'))

    return render_template(
        'pool.html',
        blocks=blocks,
        pool_name=pool,
        block_count=block_count,
        current_time=datetime.now().strftime('LLL')
    )


@app.route('/api', methods=['GET'])
def api_docs():
    return render_template(
        'api.html',
        current_time=datetime.now().strftime('LLL')
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template(
        'login.html',
        current_time=datetime.now().strftime('LLL')
    )


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    return render_template(
        'register.html',
        form=form,
        current_time=datetime.now().strftime('LLL')
    )


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

    if len(query) > 63:
        try:
            search_results = be.get_block(query, api_code=app.api_code)
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
        type = 'Block Height Info'
        try:
            try:
                n = int(query)
                search_results = be.get_block_height(n, api_code=app.api_code)
            except (ValueError, TypeError) as err:
                search_results = str('Invalid query expression. ' + str(err))
                flash(search_results, 'danger')
                return redirect(url_for('index'))
        except APIException as e:
            print('Error ' + str(e))

    return render_template(
        'results.html',
        query=query,
        search_results=search_results,
        type=type,
        current_time=datetime.now().strftime('LLL')
    )


def get_stats():
    stats = statistics.get(api_code=app.api_code)
    return stats


@app.errorhandler(404)
def page_not_found(e):
    return render_template(
        '404.html'
    ), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template(
        '500.html'
    ), 500


@app.template_filter('datetime')
def convert_unixtime(unixtime, format='medium'):
    n = datetime.fromtimestamp(
        int(unixtime)).strftime('%Y-%m-%d %H:%M:%S')
    return n


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=config.PORT,
        debug=config.DEBUG
    )
