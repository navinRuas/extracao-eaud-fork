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

#--- Função para conexão da API e consulta de atividades em monitoramento ---#
def conecta_consulta_monit(chave, url, parametros):
    #print(url)
    try:
        headers = {'chave-api':chave}
    
        response_API = requests.get(url=url, headers=headers, params=parametros)
        #print(response_API.status_code)
        response_json = json.loads(response_API.text)
        df_tarefas = pd.DataFrame(response_json['data'])
        df_tarefas = df_tarefas[['id','estado','titulo', 'siglaUnidadeAuditada', 'unidadesDeAuditoria', 'dtLimite', 'listaTiposUltimaManifestacao', 'listaTiposUltimoPosicionamento']]
        df_tarefas = df_tarefas.set_index('id')
        
        if response_API.status_code != 200:
            logging.info('Erro na execução da API que busca lista de monitoramentos, URL = '+url)
            return []
    
        if df_tarefas.empty:
            logging.info('Não há monitoramentos compatíveis com os filtros aplicados')
            return []

    except Exception as e:
        logging.error(' Ocorreu erro ao buscar lista de auditorias, por API' + str(e))
        quit()
    
    return df_tarefas


#define parametro de coleta de informaçoes do monitoramento
def coleta_params_monitoramento (idTarefa):
    params_coleta_monitoramento = {
      id: idTarefa
    }    
    return params_coleta_monitoramento
    
    
#--- Função para conexão da API e consulta de atividades em monitoramento ---#
def consulta_duracao_monit(idTarefa: int, chave):
    
    #dados para conexão API
    url_duracao ="https://eaud.cgu.gov.br/api/auth/tarefa/"+str(idTarefa)+"/periodo-realizacao"
    params_coleta_monitoramento = coleta_params_monitoramento(idTarefa)
    
    try:
        headers = {'chave-api':chave}
    
        response_API = requests.get(url=url_duracao, headers=headers, params=params_coleta_monitoramento)
        #print(response_API.status_code)
        response_json = json.loads(response_API.text)
        df_tarefas = pd.DataFrame(response_json, index=[idTarefa])
        df_tarefas[['dataRealizadaInicio', 'dataRealizadaFim']] = df_tarefas[['dataRealizadaInicio', 'dataRealizadaFim']].apply(pd.to_datetime)

        if response_API.status_code != 200:
            logging.info('Erro na execução da API que busca lista de monitoramentos, URL = '+url_duracao)
            return []
    
        if df_tarefas.empty:
            logging.info('Não há monitoramentos compatíveis com os filtros aplicados')
            return []

    except Exception as e:
        logging.error(' Ocorreu erro ao buscar lista de auditorias, por API' + str(e))
        quit()
    
    return df_tarefas


#define parametro de coleta de informaçoes de interacoes da tarefa
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

    try:
        headers = {'chave-api':chave}
    
        response_API = requests.get(url=url_interacao, headers=headers, params=params_interacao)
        #print(response_API.status_code)
        response_json = json.loads(response_API.text)
        df_interacoes = pd.DataFrame(response_json)
        #df_interacoes[['dataRealizadaInicio', 'dataRealizadaFim']] = df_interacoes[['dataRealizadaInicio', 'dataRealizadaFim']].apply(pd.to_datetime)

        if response_API.status_code != 200:
            logging.info('Erro na execução da API que busca lista de monitoramentos, URL = '+url_interacao)
            return []
    
        if df_interacoes.empty:
            logging.info('Não há monitoramentos compatíveis com os filtros aplicados')
            return []

    except Exception as e:
        logging.error(' Ocorreu erro ao buscar lista de auditorias, por API' + str(e))
        quit()
    
    return df_interacoes