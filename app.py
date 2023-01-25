# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 11:32:05 2023

Extrai dados do e-aud com o auxílio dos módulos definidos em /modules/funcoes.py 
e retorna dataframe com dados sintetizados dos monitoramentos ativos.

@author: taina.esteves
"""


import keyring
import pandas as pd
from modules.funcoes import conecta_consulta_monit, consulta_duracao_monit

#--- Entradas ---#
chave = keyring.get_password('API_EAUD', 'audin_2023')

#--- Entradas Monitoramento---#
url_monitoramento ="https://eaud.cgu.gov.br/api/auth/monitoramento"
params_monitoramento = {
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


#--- Extração de dados ---#
#armazena lista de monitoramentos não concluídos no dataframe monitoramentos_ativos
monitoramentos_ativos = conecta_consulta_monit(chave, url_monitoramento, params_monitoramento)

#cria dataframe com colunas de data de início e final para popular com informaçoes dos monitoramentos ativos
periodo_realizacao = pd.DataFrame(columns=['dataRealizadaInicio', 'dataRealizadaFim'])

#loop que coleta informações de duração dos monitoramentos ativos
for i, data  in monitoramentos_ativos.iterrows():
    periodo_moni_interacao = consulta_duracao_monit(i, chave)
    #print(i)
    periodo_realizacao = periodo_realizacao.append(periodo_moni_interacao)

#mescla informações de duração com outros dados dos monitoramentos ativos    
resumo_monitoramentos = periodo_realizacao.join(monitoramentos_ativos)
