import keyring
#import requests
#import json
import pandas as pd
#import logging
from modules.funcoes import consulta_duracao_tarefa, conecta_API

#--- Entradas ---#
chave = keyring.get_password('API_EAUD', 'audin_2023')

#--- Entradas Monitoramento---#
url_audit ="https://eaud.cgu.gov.br/api/auth/planejamento/auditoria"
params_audit = {
  "direcaoOrdenacao": "DESC",
  "colunaOrdenacao": "id",
  "tamanhoPagina": 1000,
  "offset": 0,
      "exibirColunaPendencias": 'true',
  "incluirUnidadesInferiores": 'false',
  "apenasAbertas": 'false',
  "apenasModificadasNosUltimos30Dias": 'false',
  "contarRegistros": 'true',  
}

#--- Função para conexão da API e consulta de atividades em monitoramento ---#
def conecta_consulta_audit(chave, url, parametros):

    response_json = conecta_API(chave, url, parametros)
    df_tarefas = pd.DataFrame(response_json['data'])
    df_tarefas = df_tarefas[['id','estado','titulo', 'duracaoMeses', 'homemHora']]
    df_tarefas = df_tarefas.set_index('id')
      
    return df_tarefas

#df_consultas_audit = conecta_consulta_audit(chave, url_audit, params_audit)

#df_consultas_audit.to_excel('excel_auditorias.xlsx')

#--- define parametro de coleta de informaçoes de tarefa ---#
def coleta_params_audit (idTarefa):
    params_detalhe_audit = {
      id: idTarefa
    }    
    return params_detalhe_audit

#--- Função para consulta de detalhes de tarefas de auditoria ---#
def consulta_detalhe_audit(idTarefa: int, chave):
    #dados para conexão API
    url_detalhe_audit ="https://eaud.cgu.gov.br/api/auth/planejamento/auditoria/"+str(idTarefa)
    params_detalhe_audit = coleta_params_audit(idTarefa)
    
    response_json = conecta_API(chave, url_detalhe_audit, params_detalhe_audit)
    #print(response_API.status_code)
    df_tarefas = pd.DataFrame.from_dict(response_json, orient='index')
    df_tarefas = df_tarefas.T
    #df_tarefas[['dataRealizadaInicio', 'dataRealizadaFim']] = df_tarefas[['dataRealizadaInicio', 'dataRealizadaFim']].apply(pd.to_datetime)

    return df_tarefas

df_detalhe_audit = consulta_detalhe_audit(1394095, chave)
    
dura = consulta_duracao_tarefa(1394095, chave)