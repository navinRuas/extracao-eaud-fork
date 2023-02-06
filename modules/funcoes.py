import requests
import json
import pandas as pd
#from pandas import json_normalize
import logging

#--- Função para conexão da API ---#
def conecta_API(chave, url, params):
    headers = {'chave-api':chave}

    try:
        response_API = requests.get(url=url, headers=headers, params=params)
        response_json = json.loads(response_API.text)
        df_tarefas = pd.DataFrame(response_json)
        
        if response_API.status_code != 200:
            logging.info('Erro na execução da API que busca lista de tarefas, URL = '+url)
            return []
    
        if df_tarefas.empty:
            print ('vazio')

            logging.info('Não há tarefas compatíveis com os filtros aplicados')
            return []

    except Exception as e:
        logging.error('Ocorreu erro de conexão com a API' + str(e))
        SystemExit()
        
    print ('funciona')
    return response_json

#--- Função para conexão da API e consulta de atividades em monitoramento ---#
def conecta_consulta_monit(chave, url, parametros):
    response_json = conecta_API(chave, url, parametros)
    df_tarefas = pd.DataFrame(response_json['data'])
    df_tarefas = df_tarefas[['id','estado','titulo', 'siglaUnidadeAuditada', 'unidadesDeAuditoria', 'dtLimite', 'listaTiposUltimaManifestacao', 'listaTiposUltimoPosicionamento']]
    df_tarefas = df_tarefas.set_index('id')

    return df_tarefas


#--- define parametro de coleta de informaçoes de tarefa ---#
def coleta_params_idtarefa (idTarefa):
    params_coleta_idtarefa = {
        id: idTarefa
    }    
    return params_coleta_idtarefa
     
#--- Função para conexão da API e consulta de detalhes de duração da tarefa ---#
def consulta_duracao_tarefa(idTarefa: int, chave):
    
    #dados para conexão API
    url_duracao ="https://eaud.cgu.gov.br/api/auth/tarefa/"+str(idTarefa)+"/periodo-realizacao"
    params_coleta_monitoramento = coleta_params_idtarefa(idTarefa)

    headers = {'chave-api':chave}

    response_API = requests.get(url=url_duracao,headers=headers, params=params_coleta_monitoramento)
    response_json = json.loads(response_API.text)
    
    df_tarefas = pd.DataFrame(response_json, index=[idTarefa])
    df_tarefas[['dataRealizadaInicio', 'dataRealizadaFim']] = df_tarefas[['dataRealizadaInicio', 'dataRealizadaFim']].apply(pd.to_datetime)

    return df_tarefas

#--- define parametro de coleta de informaçoes de interacoes da tarefa ---#
def coleta_params_interacao (idTarefa):
    params_interacao = {
      "direcaoOrdenacao": "DESC",
      "tamanhoPagina": 1000,
      "offset": 0,
      "idTarefa": idTarefa,
      "administradorDaTarefa": 'True'    
    }  
    return params_interacao

#--- Função para conexão da API e consulta de atividades em monitoramento ---#
def consulta_qtd_interacoes(idTarefa, chave):

    #dados para conexão API
    url_interacao ="https://eaud.cgu.gov.br/api/auth/tarefa/{idTarefa}/interacao/listar"
    params_interacao = coleta_params_interacao(idTarefa)

    response_json = conecta_API(chave, url_interacao, params_interacao)
    df_interacoes = pd.DataFrame(response_json)
    #df_interacoes[['dataRealizadaInicio', 'dataRealizadaFim']] = df_interacoes[['dataRealizadaInicio', 'dataRealizadaFim']].apply(pd.to_datetime)

    return df_interacoes
