# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, redirect, flash, url_for, session
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_misaka import Misaka
from blockchain import blockexplorer as be
from blockchain import statistics
from blockchain.exceptions import APIException
from flask_qrcode import QRcode
from datetime import datetime
from forms import SearchForm, AddressSearchForm, RegistrationForm
import config

bootstrap = Bootstrap()
app = Flask(__name__)
moment = Moment(app)
QRcode(app)
Misaka(app)

app.secret_key = config.SECRET_KEY


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
        current_time=datetime.now().strftime('LLL')
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
        blocks = be.get_block_height(height)
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
        addr = be.get_address(address)
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
                    address = be.get_address(clean_addr)

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
        tx = be.get_tx(hash)
    except APIException as e:
        message = 'There has been an API Error.'
        flash(message, 'danger')
        return redirect(url_for('index'))

    return render_template(
        'transaction.html',
        tx=tx,
        current_time=datetime.now().strftime('LLL')
    )


@app.route('/pools', methods=['GET', 'POST'])
def pools():
    return render_template(
        'pools.html',
        current_time=datetime.now().strftime('LLL')
    )


@app.route('/pool/<string:pool>', methods=['GET', 'POST'])
def pool(pool):
    pass


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
        type = 'Block Height Info'
        try:
            try:
                n = int(query)
                search_results = be.get_block_height(n)
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
    stats = statistics.get()
    return stats


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
