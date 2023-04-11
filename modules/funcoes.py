# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 17:32:38 2023

Contém funções que extraem dados de monitoramento e interações de tarefas do e-aud.

@author: taina.esteves
"""
import requests
import json
import pandas as pd
#from pandas import json_normalize
import logging
#from datetime import datetime


#--- Função para conexão da API ---#
def conecta_API(chave, url, params):
        
    try:
        headers = {'chave-api':chave}
        response_API = requests.get(url=url, headers=headers, params=params)
        response_json = json.loads(response_API.text)
        df_tarefas = pd.DataFrame(response_json['data'])
        
        if response_API.status_code != 200:
            logging.info('Erro na execução da API que busca lista de tarefas, URL = '+url)
            return []
    
        if df_tarefas.empty:
            logging.info('Consulta à API não retornou resultados')

            logging.info('Não há tarefas compatíveis com os filtros aplicados')
            return []

    except Exception as e:
        logging.error('Ocorreu erro de conexão com a API: ' + str(e))
        quit()
        
    print ('funciona')
    return response_json


#--- Função para conexão da API e consulta de atividades em monitoramento ---#
def conecta_consulta_monit(chave, url, parametros):
    response_json = conecta_API(chave, url, parametros)
    
    df_tarefas = pd.DataFrame(response_json['data'])
    df_tarefas = df_tarefas[['id','estado','titulo', 'siglaUnidadeAuditada', 'unidadesDeAuditoria', 'dtLimite', 'listaTiposUltimaManifestacao', 'listaTiposUltimoPosicionamento']]
    df_tarefas = df_tarefas.set_index('id')
    df_tarefas = df_tarefas.astype('string')
    df_tarefas['dtLimite'] = pd.to_datetime(df_tarefas['dtLimite'])
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
    params_coleta_idtarefa = coleta_params_idtarefa(idTarefa)
    headers = {'chave-api':chave}
    response_API = requests.get(url=url_duracao, headers=headers, params=params_coleta_idtarefa)
    response_json = json.loads(response_API.text)
    
    df_tarefas = pd.DataFrame(response_json, index=[idTarefa])
    df_tarefas[['dataRealizadaInicio', 'dataRealizadaFim']] = df_tarefas[['dataRealizadaInicio', 'dataRealizadaFim']].apply(pd.to_datetime)
    df_tarefas.index.name = 'id'
    return df_tarefas
 
#--- define parametro de coleta de informaçoes de interacoes da tarefa ---#
def coleta_params_interacao (idTarefa):
    params_interacao = {
      "direcaoOrdenacao": "DESC",
      "tamanhoPagina": 1000,
      "offset": 0,
      "idTarefa": idTarefa   
    }  
    return params_interacao

#--- Função para conexão da API e consulta de atividades em monitoramento ---#
def consulta_interacoes(idTarefa, chave):

    #dados para conexão API
    url_interacao ="https://eaud.cgu.gov.br/api/auth/tarefa/{idTarefa}/interacao/listar"
    params_interacao = coleta_params_interacao(idTarefa)
    headers = {'chave-api':chave}
    response_API = requests.get(url=url_interacao, headers=headers, params=params_interacao)
    response_json = json.loads(response_API.text)
    df_interacoes = pd.DataFrame(response_json)
    df_interacoes = df_interacoes[['id', 'idTarefa','data', 'tipoInteracao', 'autor','unidadeAutor']]
    df_interacoes = df_interacoes.set_index('idTarefa')
    df_interacoes['data'] = df_interacoes['data'].apply(pd.to_datetime)
    print (idTarefa)
    
    return df_interacoes