import requests
import json
import sys
from flask import Flask, render_template, Response, request, jsonify

# from flask_cors import CORS, cross_origin

# app = Flask(__name__)
# CORS(app)

""" --------------- GET ENDPOINTS SUPESP --------------- """


def consulta_detran_veiculo_placa(placa, token):
    base = 'https://spca.sspds.ce.gov.br/prod/api/veiculo?value='
    url = base + placa

    auxheaders = 'Bearer ' + token
    headers = {'Authorization': auxheaders}

    try:
        return requests.get(url, headers=headers)
    except:
        print("Erro de conexao com o endpoint -> civil detran")
        exit()


def consulta_denatran_veiculo_placa(placa, token):
    base = 'https://spca.sspds.ce.gov.br/prod/api/veiculo/denatran?value='
    url = base + placa

    auxheaders = 'Bearer ' + token
    headers = {'Authorization': auxheaders}
    try:
        return requests.get(url, headers=headers)
    except:
        print("Erro de conexao com o endpoint -> veiculo denatran")
        exit()


def consulta_civil_rg(rg, token):
    base = 'https://spca.sspds.ce.gov.br/prod/api/identificacaoCivil?rg='
    url = base + str(rg)

    auxheaders = 'Bearer ' + token
    headers = {'Authorization': auxheaders}
    try:
        return requests.get(url, headers=headers)
    except:
        print("Erro de conexao com o endpoint -> civil rg")
        exit()


def consulta_criminal_fonetica(body, token):
    url = 'https://spca.sspds.ce.gov.br/prod/api/identificacaoCriminal'

    auxheaders = 'Bearer ' + token
    headers = {
                'Content-Type': 'application/json',
                'Authorization': auxheaders
              }

    try:
        return requests.post(url, data=json.dumps(body), headers=headers)
    except:
        print("Erro de conexao com o endpoint -> criminal fonetica")
        exit()


def consulta_criminal_id(id_criminal, token):
    base = 'https://spca.sspds.ce.gov.br/prod/api/identificacaoCriminal?id='
    url = base + str(id_criminal)

    auxheaders = 'Bearer ' + token
    headers = {'Authorization': auxheaders}
    try:
        return requests.get(url, headers=headers)
    except:
        print("Erro de conexao com o endpoint -> criminal id")
        exit()


""" ------------------- ENCAPSULATE ON JSON ------------------- """


def split_date(data):
    dia = data[0:2]
    mes = data[2:4]
    ano = data[4:]
    return dia + '/' + mes + '/' + ano


def consulta_textual_veiculo_denatran(placa, token):
    req = consulta_denatran_veiculo_placa(placa, token)

    json_denatran = json.loads(req.text)

    if req.status_code == 200:
        dict_denatran = {}

        keys_denatran = {
                        'proprietario': 'nomeProprietario',
                        'cpf': 'cpfCgcProprietario',
                        'renavam': 'codigoRenavam',
                        'placa': 'placaUnica',
                        'chassi': 'chassi',
                        'combustivel': 'nomeCombustivel',
                        'categoria': 'nomeCategoria',
                        'qtdPassageiros': 'capacidadePassageiros',
                        'numMotor': 'numeroMotor',
                        'marca': 'descricaoMarcaModelo',
                        'corVeiculo': 'nomeCor',
                        'carroceria': 'nomeTipoCarroceria',
                        'numDocumento': 'numDocumento',
                        'potencia': 'potenciaVeiculo',
                        'cep': 'numCep',
                        'municipio': 'nomeMunicipio',
                        'anoExercicio': 'anoExercicio',
                        'dataLicenciamento': 'dataLicenciamento',
                        'debitoLicenciamento': 'debitoLicenciamento',
                        'isentoIpva': 'isentoIpva',
                        'debitoIpva': 'debitoIpva',
                        'qtdMultas': 'indicadorMultaExigivelRenainf',
                        'qtdRestricoes': 'indicadorRestricaoRfb'
                    }

        for key, value in keys_denatran.items():
            try:
                dict_denatran[key] = json_denatran[value]
            except:
                dict_denatran[key] = '-'

        dict_denatran['ano_Fabricacao_Modelo'] = json_denatran['anoFabricacao'] + ' / ' + json_denatran['anoModelo']
        dict_denatran['ano_Especie_Tipo'] = json_denatran['nomeEspecie'] + ' / ' + json_denatran['nomeTipo']
        dict_denatran['numCilindradas'] = json_denatran['cilindradas'] + ' cm3'
        try:
            dict_denatran['endereco_Completo'] = json_denatran['nomeEndereco'] + ', ' + json_denatran['numEndereco'] + ' - ' +\
                                                 json_denatran['nomeBairro']
        except:
            dict_denatran['endereco_Completo'] = '-'

        dict_denatran['dataAlteracao'] = split_date(json_denatran['dataUltimaAtualizacao'])
        try:
            dict_denatran['nomeProprietarioAnterior'] = json_denatran['nomeProprietarioAnterior'] + ' - ' + \
                                                       json_denatran['nomeUfAnterior']
        except:
            dict_denatran['nomeProprietarioAnterior'] = '-'

        return dict_denatran
    else:
        return json_denatran


def consulta_textual_veiculo_detran(placa, token):
    req = consulta_detran_veiculo_placa(placa, token)

    json_detran = json.loads(req.text)

    if req.status_code == 200:
        dict_detran = {}

        keys_detran = {
                      'proprietario': 'nomeProprietario',
                      'cpf': 'cpfCgcProprietario',
                      'renavam': 'renavam',
                      'placa': 'placa',
                      'chassi': 'chassi',
                      'combustivel': 'nomeCombustivel',
                      'categoria': 'nomeCategoria',
                      'qtdPassageiros': 'qtdPassageiros',
                      'numMotor': 'numMotor',
                      'marca': 'nomeMarca',
                      'corVeiculo': 'nomeCor',
                      'carroceria': 'nomeCarroceria',
                      'numDocumento': 'numDocumento',
                      'potencia': 'numPotencia',
                      'cep': 'numCep',
                      'municipio': 'nomeMunicipio',
                      'anoExercicio': 'anoExercicio',
                      'dataLicenciamento': 'dataLicenciamento',
                      'debitoLicenciamento': 'debitoLicenciamento',
                      'isentoIpva': 'isentoIpva',
                      'debitoIpva': 'debitoIpva',
                      'qtdMultas': 'qtdMultas',
                      'qtdRestricoes': 'qtdRestricoes'
                    }


        for key, value in keys_detran.items():
            try:
                dict_detran[key] = json_detran[value]
            except:
                dict_detran[key] = '-'

        dict_detran['ano_Fabricacao_Modelo'] = json_detran['anoFabricacao'] + ' / ' + json_detran['anoModelo']
        dict_detran['ano_Especie_Tipo'] = json_detran['nomeEspecie'] + ' / ' + json_detran['nomeTipo']
        dict_detran['numCilindradas'] = json_detran['numCilindradas'] + ' cm3'
        dict_detran['endereco_Completo'] = json_detran['nomeEndereco'] + ', ' + json_detran['numEndereco'] + ' - ' + \
                                           json_detran['nomeBairro']
        dict_detran['dataAlteracao'] = split_date(json_detran['dataAlteracao'])
        dict_detran['nomeProprietarioAnterior'] = json_detran['nomeProprietarioAnterior'] + ' - ' + \
                                                  json_detran['nomeUfAnterior']

        return dict_detran
    else:
        return json_detran


def create_output_json_civil_criminal(civil_data, criminal_data):
    dict_civil = {}
    list_criminal = []

    keys_civil = {
        'nome': 'denominacao',
        'rg': 'numRg',
        'cpf': 'cpf',
        'data_nascimento': 'placa',
        'sexo': 'sexo',
        'nomeMae': 'descricaoMae',
        'nomePai': 'descricaoPai',
        'estado_civil': 'estadoCivil',
        'escolaridade': 'grauInstrucao',
    }

    for key, value in keys_civil.items():
        try:
            dict_civil[key] = civil_data[value]
        except:
            dict_civil[key] = '-'

    try:
        endereco = civil_data['endereco']
    except:
        endereco = '-'

    try:
        bairro = civil_data['bairro']
    except:
        bairro = '-'

    try:
        cep = civil_data['cep']
    except:
        cep = '-'

    dict_civil['endereco_completo'] = endereco + ' - ' + bairro + ' - ' + cep

    try:
        cidadeNasc = civil_data['cidadeNascimento']
    except:
        cidadeNasc = '-'

    try:
        ufNasc = civil_data['ufNascimento']
    except:
        ufNasc = '-'

    dict_civil['local_nascimento'] = cidadeNasc + ' - ' + ufNasc

    keys_criminal = {
        'cpf': 'cpf',
        'qtd_mandado_aberto': 'qtdMandatoAberto',
        'qtd_livramento_condicional': 'qtdLivramentoCondicional',
        'recapitulacao_penal': 'recapitulacaoPenalList',
        'municipio': 'municipio',
        'pais': 'pais',
        'qtd_infrator': 'qtdInfrator',
        'qtd_inquerito': 'qtdInquerito'
    }

    if type(criminal_data) is list:
        for obj_criminal in criminal_data:
            dict_criminal = {}

            for key, value in keys_criminal.items():
                try:
                    dict_criminal[key] = obj_criminal[value]
                except:
                    dict_criminal[key] = '-'

            list_criminal.append(dict_criminal)
    else:
        list_criminal.append(criminal_data)

    dict_civilcriminal = {
        'civil': dict_civil,
        'criminal': list_criminal
    }

    return dict_civilcriminal


def fluxo_textual_rg(value, token):

    global data_civil_rg, data_criminal_fonetica
    data_criminal_id = []

    # Primeira consulta (base civil por rg)
    request_civil_rg = consulta_civil_rg(value, token)

    if request_civil_rg.status_code == 200 and request_civil_rg.text != '' and request_civil_rg.text != []:
        data_civil_rg = json.loads(request_civil_rg.text)

        # Segunda consulta (base criminal por fonetica)
        try:
            name_data = data_civil_rg['denominacao']
            try:
                mother_data = data_civil_rg['descricaoMae']

                body = {
                    'nome': name_data,
                    'nomeMae': mother_data
                }

                request_criminal_fonetica = consulta_criminal_fonetica(body, token)
            except:
                try:
                    father_data = data_civil_rg['descricaoPai']

                    body = {
                        'nome': name_data,
                        'nomePai': father_data
                    }

                    request_criminal_fonetica = consulta_criminal_fonetica(body, token)
                except:
                    body = {
                        'nome': name_data
                    }

                    request_criminal_fonetica = consulta_criminal_fonetica(body, token)
        except:
            request_criminal_fonetica = {'status': 404, 'text': 'Invalid Identification in criminal phonetic!'}

        if request_criminal_fonetica.status_code == 200 and request_criminal_fonetica.text != '' and request_criminal_fonetica.text != '[]':
            data_criminal_fonetica = json.loads(request_criminal_fonetica.text)

            # Terceira consulta (base criminal id)
            try:
                for obj_crim_fonet in data_criminal_fonetica:
                    id_criminal = obj_crim_fonet['id']

                    request_criminal_id = consulta_criminal_id(id_criminal, token)

                    if request_criminal_id.status_code == 200 and request_criminal_id.text != '' and request_criminal_id.text != '[]':
                        data_criminal_id.append(json.loads(request_criminal_id.text))
            except:
                request_criminal_id = {'status': 404, 'text': 'Invalid Identification in criminal id!'}
        else:
            data_criminal_id = 'Unidentified person in the id criminal base!'
            data_criminal_fonetica = 'ERROR: Unidentified person in the phonetic criminal base!'

        # Create output json
        response_civil_criminal = create_output_json_civil_criminal(data_civil_rg, data_criminal_id)
        return response_civil_criminal

    else:
        return {'status': request_civil_rg.status_code, 'error': 'No person identified!'}


def consulta_textutal_civil(type_research, value, token):
    if type_research == 'CPF':
        print('busca relacionado ao CPF')
    elif type_research == 'CNH':
        print('busca relacionado a CNH')
    elif type_research == 'RG':
        return fluxo_textual_rg(value, token)


""" ---------------------- FLASK CONFIG ---------------------- """
app = Flask(__name__)
# CORS(app)
app.config["DEBUG"] = False


""" ------------------  ROUTES -> ENDPOINTS ------------------ """


@app.route('/api/apptatico/veiculo_placa', methods=['POST'], endpoint='api_apptatico_veiculoplaca')
def api_apptatico_veiculoplaca():
    dict_response = {}

    placa = request.json["placa"]
    token = request.json["token_access"]

    result_detran = consulta_textual_veiculo_detran(placa, token)
    result_denatran = consulta_textual_veiculo_denatran(placa, token)

    dict_response['detran'] = result_detran
    dict_response['denatran'] = result_denatran
    response = jsonify(json.loads(json.dumps(dict_response)))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/api/apptatico/textual_pessoas', methods=['POST'], endpoint='api_apptatico_textualpessoas')
def api_apptatico_textualpessoas():
    type_research = request.json["type_research"]
    value = request.json["value"]
    token = request.json["token_access"]

    result_civil = consulta_textutal_civil(type_research.upper(), value, token)

    response = jsonify(json.loads(json.dumps(result_civil)))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


""" -------------------------- MAIN -------------------------- """
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3018)
