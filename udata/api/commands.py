# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import os

import click

from flask import json, current_app
from flask_restplus import schemas

from udata.api import api
from udata.commands import cli, success, exit_with_error

log = logging.getLogger(__name__)


@cli.group('api')
def grp():
    '''API related operations'''
    pass


def json_to_file(data, filename, pretty=False):
    '''Dump JSON data to a file'''
    kwargs = dict(indent=4) if pretty else {}
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    dump = json.dumps(api.__schema__, **kwargs)
    with open(filename, 'wb') as f:
        f.write(dump.encode('utf-8'))


@grp.command()
@click.argument('filename')
@click.option('-p', '--pretty', is_flag=True, help='Pretty print')
def swagger(filename, pretty):
    '''Dump the swagger specifications'''
    json_to_file(api.__schema__, filename, pretty)


@grp.command()
@click.argument('filename')
@click.option('-p', '--pretty', is_flag=True, help='Pretty print')
@click.option('-u', '--urlvars', is_flag=True, help='Export query strings')
@click.option('-s', '--swagger', is_flag=True,
              help='Export Swagger specifications')
def postman(filename, pretty, urlvars, swagger):
    '''Dump the API as a Postman collection'''
    data = api.as_postman(urlvars=urlvars, swagger=swagger)
    json_to_file(data, filename, pretty)


@grp.command()
def validate():
    '''Validate the Swagger/OpenAPI specification with your config'''
    with current_app.test_request_context():
        schema = json.loads(json.dumps(api.__schema__))
    try:
        schemas.validate(schema)
        success('API specifications are valid')
    except schemas.SchemaValidationError as e:
        exit_with_error('API specifications are not valid', e)
