# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, redirect, url_for, session
from flask_bootstrap import Bootstrap
from blockchain import blockexplorer as be
from blockchain import statistics
import config

bootstrap = Bootstrap()
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    blocks = be.get_blocks()[:5]
    stats = statistics.get()

    render_template(
        'index.html',
        blocks=blocks,
        stats=stats
    )


if __name__ == '__main__':
    app.run(
        port=config.PORT,
        debug=config.DEBUG
    )
