from flask import Flask, jsonify, request
from flasgger import Swagger
import pampo

try:
    import simplejson as json
except ImportError:
    import json
try:
    from http import HTTPStatus
except ImportError:
    import httplib as HTTPStatus




app = Flask(__name__)

app.config['SWAGGER'] = {
    'title': 'Pampo API Explorer',
    'uiversion': 3
}
swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec_pampo',
            "route": '/flasgger_static/apispec_pampo.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}
swagger = Swagger(app,config=swagger_config)

@swagger.validate('content')
@app.route('/pampo',methods=['POST'])
def handle_pampo():
    """Example endpoint return a list of keywords using YAKE
    ---
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
        - name: content
          in: body
          description: content object
          required: true
          schema:
            $ref: '#/definitions/content'
    requestBody:
        description: Optional description in *Markdown*
        required: true
        content:
          application/json:
            schema:
              id: content
              type: object
    responses:
      200:
        description: Extract NamedEntities from input text
        schema:
            $ref: '#/definitions/result'
    definitions:
      content:
        description: content object
        properties:
          text:
            type: string
        required:
          - text
        example:   # Sample object
            text: A aldeia piscatória de Alvor está situada no estuário do Rio Alvor e apesar da evolução constante do turismo no Algarve, mantém a sua arquitetura baixa e encanto da cidade velha, com ruas estreitas de paralelepípedos que nos levam até à Ria de Alvor, uma das belezas naturais mais impressionantes de Portugal. Há muitos hotéis em Alvor por onde escolher e adequar às exigências das suas férias, quanto a gosto e orçamento, bem como uma série de alojamento autossuficiente para aqueles que preferem ter um pouco mais de liberdade durante a sua estadia na Região de Portimão. Há muito para fazer e descobrir em Alvor, quer seja passar os seus dias descobrindo a rede de ruas desta encantadora vila de pescadores, explorar as lojas, ir para a praia para se divertir entre brincadeiras na areia e mergulhos no mar, ou descobrir a flora e fauna da área classificada da Ria de Alvor. O charme de Alvor não se esgota na Vila. Ficar hospedado em Alvor vai proporcionar-lhe momento mágicos entre paisagens de colinas, lagoas rasas e vistas panorâmicas sobre o Oceano Atlântico. Terá oportunidade de praticar o seu swing num dos campos de golfe de classe mundial e explorar as principais atrações históricas e alguns dos segredos mais bem escondidos do Algarve, nas proximidades, em Portimão e Mexilhoeira Grande. Consulte a lista dos nossos parceiros e escolha o hotel em Alvor, onde ficar durante as suas férias no Algarve.
      result:
        type: array
        items:
			type: string
    """

    try:
        assert request.json["text"] , "Invalid text"
        text = request.json["text"]

        my_pampo = pampo.extract_entities(text)

        result  = my_pampo

        return jsonify(result), HTTPStatus.OK
    except Exception as e:
        return jsonify(str(e)), HTTPStatus.BAD_REQUEST

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8002)
