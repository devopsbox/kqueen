from flask import abort
from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask_jwt import jwt_required, current_identity
from kqueen.models import Cluster
from uuid import UUID

import logging

logger = logging.getLogger(__name__)

api = Blueprint('api', __name__)


# error handlers
@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@api.errorhandler(500)
def not_implemented(error):
    return make_response(jsonify({'error': 'Not implemented'}), 500)


@api.route('/')
@api.route('/health')
def index():
    return jsonify({'response': 'Gutten tag!'})


# Clusters
@api.route('/clusters', methods=['GET'])
@jwt_required()
def cluster_list():
    # TODO: implement native serialization

    output = []

    for cluster in list(Cluster.list(return_objects=True).values()):
        output.append(cluster.get_dict())

    return jsonify(output)


@api.route('/clusters/<cluster_id>', methods=['GET'])
@jwt_required()
def cluster_detail(cluster_id):

    # read uuid
    try:
        object_id = UUID(cluster_id, version=4)
    except ValueError:
        abort(404)

    # load object
    try:
        obj = Cluster.load(object_id)
    except NameError:
        abort(404)

    return jsonify(obj.get_dict())


@api.route('/clusters/<cluster_id>/status', methods=['GET'])
@jwt_required()
def cluster_status(cluster_id):

    try:
        object_id = UUID(cluster_id, version=4)
    except ValueError:
        abort(404)

    # load object
    try:
        obj = Cluster.load(object_id)
    except NameError:
        abort(404)

    return jsonify(obj.status())


@api.route('/clusters/<cluster_id>/topology-data', methods=['GET'])
def cluster_topology_data(cluster_id):

    try:
        object_id = UUID(cluster_id, version=4)
    except ValueError:
        abort(404)

    # load object
    try:
        obj = Cluster.load(object_id)
    except NameError:
        abort(404)

    return jsonify(obj.topology_data())


@api.route('/clusters/<cluster_id>/kubeconfig', methods=['GET'])
@jwt_required()
def cluster_kubeconfig(cluster_id):

    try:
        object_id = UUID(cluster_id, version=4)
    except ValueError:
        abort(404)

    # load object
    try:
        obj = Cluster.load(object_id)
    except NameError:
        abort(404)

    return jsonify(obj.kubeconfig)
