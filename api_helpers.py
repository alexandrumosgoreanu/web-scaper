from flask import Flask, request, jsonify
from elasticsearch_helpers import query_company_data

def create_api(es):
    app = Flask('company-data')
    app.es_client = es

    @app.route('/company-info', methods=['GET'])
    def get_company_info():
        # Extract parameters from the request
        company_profile = {
            'input_name': request.args.get('company_name'),
            'input_phone': request.args.get('phone'),
            'input_website': request.args.get('website'),
            'input_facebook': request.args.get('facebook')
        }
        print(company_profile)
        response = query_company_data(es, company_profile)
        if response.hits.total.value > 0:
            company_info = response.hits[0].to_dict()   # getting the first result
            print(company_info)
            return jsonify(company_info)
        else:
            return jsonify({"message": "Company not found"}), 404
    return app
