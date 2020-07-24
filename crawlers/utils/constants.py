"""

"""

DATA_LINKS = [
    #    "http://stf.jus.br/portal/jurisprudencia/listarConsolidada.asp?base=baseAcordaos&"
    #    "base=baseRepercussao&base=baseSumulasVinculantes&base=baseSumulas&base=basePresidencia&"
    #    "url=&txtPesquisaLivre=consumidor",
    "http://stf.jus.br/portal/jurisprudencia/listarConsolidada.asp?"
    "base=baseAcordaos&base=baseRepercussao&base=baseSumulasVinculantes&"
    "base=baseSumulas&base=basePresidencia&url=&txtPesquisaLivre=a%C3%A7%C3%A3o%20ou%20"
    "agravante%24%20ou%20liminar%24%20ou%20mandato%24%20ou%20cautelar%24%20ou%20peti%C3%A7%24%20ou%20"
    "embargo%24%20ou%20crime%24%20ou%20dolo%24%20ou%20ementa%24%20ou%20apela%C3%A7%24%20ou%20"
    "justi%C3%A7a%24%20ou%20jur%C3%ADdico%24%20ou%20julgador%24%20ou%20stf%20ou%20lei%24%20ou%20"
    "processo%24%20ou%20juiz%24%20ou%20tribuna%24%20ou%20consumidor%24%20ou%20constituciona%24%20ou"
    "%20inconstituciona%24%20ou%20recurso%24%20ou%20ac%C3%B3rd%C3%A3o%24%20ou%20repercuss%C3%A3o%20ou%20r%C3%"
    "A9u%20ou%20juizad%24",
    # "http://stf.jus.br/portal/jurisprudencia/listarConsolidada.asp?base=baseAcordaos&base=baseRepercussao&base="
    # "baseSumulasVinculantes&base=baseSumulas&base=basePresidencia&url=&txtPesquisaLivre=lei"
]

BASE_URL_STF_JURISPR = "http://stf.jus.br/portal/jurisprudencia/"
BASE_URL_INTEIRO_TEOR = "http://stf.jus.br/portal/"

ACORDAOS = "acordaos/"
REPERCUSSAO_GERAL = "repercussao_geral/"
MONOCRATICA = "monocratica/"

DATA_CASES = "data/cases"

"""
Main URLs
Para acórdãos entre 2009 e 2020
http://stf.jus.br/portal/jurisprudencia/listarJurisprudencia.asp?s1=%28%40JULG+%3E%3D+20090101%29%28%40JULG+%3C%3D+20210101%29&base=baseAcordaos&url=http://tinyurl.com/tbxzngt

Para acórdaos entre 1950 e 2009
http://stf.jus.br/portal/jurisprudencia/listarJurisprudencia.asp?s1=%28ACAO+OU+AGRAVANTE%24+OU+LIMINAR%24+OU+MANDATO%24+OU+CAUTELAR%24+OU+PETIC%24+OU+EMBARGO%24+OU+CRIME%24+OU+DOLO%24+OU+EMENTA%24+OU+APELAC%24+OU+JUSTICA%24+OU+JURIDICO%24+OU+JULGADOR%24+OU+STF+OU+LEI%24+OU+PROCESSO%24+OU+JUIZ%24+OU+TRIBUNA%24+OU+CONSUMIDOR%24+OU+CONSTITUCIONA%24+OU+INCONSTITUCIONA%24+OU+RECURSO%24+OU+ACORDAO%24+OU+REPERCUSSAO+OU+REU+OU+JUIZAD%24%29&base=baseAcordaos&url=http://tinyurl.com/r52lono
"""

# ============================================================= #
#                              TJ-SC                            #
# ============================================================= #
DT_INIT_TEXT = "11/01/1920"
DT_FINISH_TEXT = "12/02/2021"

X_PATH_TJ_DT_INIT = "//*[@id=\"dtini\"]"
X_PATH_TJ_DT_FINISH = "//*[@id=\"dtfim\"]"

X_PATH_TJ_CHECK_INTEIRO_TEOR = "/html/body/div[8]/div[2]/fieldset/form/div/table[1]/tbody/tr/td[2]/span[1]"
X_PATH_TJ_CHECK_AC_TJ = "/html/body/div[8]/div[2]/fieldset/form/div/table[2]/tbody/tr[1]/td[1]/span"
X_PATH_TJ_CHECK_AC_CONSELHO = "/html/body/div[8]/div[2]/fieldset/form/div/table[2]/tbody/tr[2]/td[1]/span"
X_PATH_TJ_CHECK_AC_TURMAS_REC = "/html/body/div[8]/div[2]/fieldset/form/div/table[2]/tbody/tr[3]/td[1]/span"
X_PATH_TJ_CHECK_DESPACHO_VP = "/html/body/div[8]/div[2]/fieldset/form/div/table[2]/tbody/tr[1]/td[2]/span"
X_PATH_TJ_CHECK_MC_TJ = "/html/body/div[8]/div[2]/fieldset/form/div/table[2]/tbody/tr[2]/td[2]/span"
X_PATH_TJ_CHECK_MC_REC = "/html/body/div[8]/div[2]/fieldset/form/div/table[2]/tbody/tr[3]/td[2]/span"

X_PATH_TJ_AC_CHECKS = [
    X_PATH_TJ_CHECK_AC_TJ,
    X_PATH_TJ_CHECK_AC_CONSELHO,
    X_PATH_TJ_CHECK_AC_TURMAS_REC
]

X_PATH_TJ_MN_CHECKS = [
    X_PATH_TJ_CHECK_MC_TJ,
    X_PATH_TJ_CHECK_MC_REC
]

X_PATH_CBOX_NUM_RES = "//*[@id=\"ps_select\"]"
X_PATH_TJ_BT_SEARCH = "/html/body/div[8]/div[2]/fieldset/form/div/input[2]"
X_PATH_TJ_BT_CLOSE_FT = "/html/body/div[13]/div[2]/div/div[1]/a"
X_PATH_TJ_FULL_TEXT = "/html/body/div[12]/div[2]/div/div[2]/div"
X_PATH_TJ_BT_PDF = "/html/body/div[8]/div[2]/span/div[4]/div/div[1]/div[1]/a"

PATH_TJ_FILES_AC = "data/tj_sc/" + ACORDAOS
PATH_TJ_FILES_MN = "data/tj_sc/" + MONOCRATICA
PATH_TJ_FILES = "../data/tj_sc/acordaos/links/"

# ============================================================= #
#                             STJ-SC                            #
# ============================================================= #

# Dates
X_PATH_STJ_DT_INIT = "//*[@id=\"data_inicial\"]"
X_PATH_STJ_DT_FINISH = "//*[@id=\"data_final\"]"

# Checkbox todos os tipos de processos
X_PATH_STJ_CHECK_TODAS = "//*[@id=\"todas\"]"

X_PATH_STJ_BT_SEARCH = "/html/body/div[2]/div[6]/div/div/div[3]/div[2]/div/div/div[2]/div[2]/form/div[17]/input[1]"
X_PATH_STJ_BT_AC_REP = "/html/body/div[2]/div[6]/div/div/div[3]/div[2]/div/div/div/div[3]/div[1]/div/span[2]/a"
X_PATH_STJ_BT_MONO = "/html/body/div[2]/div[6]/div/div/div[3]/div[2]/div/div/div/div[3]/div[6]/div/span[2]/a"
X_PATH_STJ_BT_AC = "/html/body/div[2]/div[6]/div/div/div[3]/div[2]/div/div/div/div[3]/div[5]/div/span[2]/a"
X_PATH_STJ_BT_VOLTAR = "/html/body/div[2]/div[6]/div/div/div[3]/div[2]/div/div/div/div[2]/a"
X_PATH_STJ_LIST_DOC = "//*[@id=\"listadocumentos\"]"
X_PATH_STJ_PRINT = "/html/body/div[2]/div[6]/div/div/div[3]/div[2]/div/div/div/div[3]/div[1]/div[1]/a[4]"
X_PATH_STJ_INTEIRO_TEOR = "/html/body/div[2]/div[6]/div/div/div[3]/div[2]/div/div/div/div[3]/div[1]/div[1]/a[1]"
X_PATH_STJ_IT_PT_12 = "/html/body/div[2]/div[6]/div/div/div[3]/div[2]/div/div/table/tbody/tr[2]/td[2]/a"
X_PATH_STJ_IT_PT_1 = "/html/body/div[2]/div[6]/div/div/div[3]/div[2]/div/div/div/form/ol/li/b/a"
X_PATH_STJ_IT_PT_2 = "/html/body/div[1]/a"
X_PATH_STJ_BT_NEXT_PAGE_1 = "/html/body/div[2]/div[6]/div/div/div[3]/div[2]/div/div/div/form/div/a[2]"
X_PATH_STJ_BT_NEXT_PAGE_2 = "/html/body/div[2]/div[6]/div/div/div[3]/div[2]/div/div/div/form/div/a[4]"

PATH_BASE_DATASET = "/media/trdp/Arquivos/Studies/Msc/Thesis/Experiments/Datasets/law_embeddings_database/"
# PATH_BASE_DATASET = "/home/egov/Documentos/Experiments/Datasets/law_embeddings_database/"
PATH_DOWNLOAD_AC = PATH_BASE_DATASET + "stj/cases/acordaos/"
PATH_DOWNLOAD_MC = PATH_BASE_DATASET + "stj/cases/monocratica/"

# ============================================================= #
#                             JUS_BRAZIL                         #
# ============================================================= #
BASE_URL_JUSBRASIL = "https://www.jusbrasil.com.br/jurisprudencia/busca?q=" \
                     "transporte+%28a%C3%A9reo+OR+a%C3%A9rea%29+%28consumidor+OR+consumo%29&" \
                     "idtopico=T10000010&dateFrom=@date_from&dateTo=@date_toT23%3A59%3A59"

# ============================================================= #
#                          STF METADATA                         #
# ============================================================= #

PROC_NUMBER_INPUT_FILE = "data/metadata/metadados_@_$.jsonl"
PROC_METADATA_OUTPUT_FILE = "data/metadata/metadata_completo_@_$.jsonl"
BASE_URL_STF_METADATA = "http://portal.stf.jus.br/"
X_PATH_STF_INPUT_SEARCH_BOX = "//*[@id=\"pesquisaPrincipalClasseNumero\"]"
X_PATH_STF_METADATA_BUTTON_SEARCH = "//*[@id=\"btnPesquisar\"]"
X_PATH_STF_LIST_RELATED_PROC = "/html/body/div[1]/section[2]/div/div[2]/div/div/div/div/table"
X_PATH_STF_PHYSICAL_DIGITAL_TYPE = "/html/body/div[1]/section[2]/div/div[2]/div/div/div/div/div[1]/" \
                                   "div[1]/div[1]/div/span[1]"
# Infos in the header
X_PATH_STF_NIVEL_RESTRICAO = "/html/body/div[1]/section[2]/div/div[2]/div/div/div/div/div[1]/div[1]/div[1]/div/span[2]"
X_PATH_STF_NUMERO_UNICO_PROC = "/html/body/div[1]/section[2]/div/div[2]/div/div/div/div/div[1]/div[1]/div[2]"
X_PATH_STF_PROC_CLASSE = "/html/body/div[1]/section[2]/div/div[2]/div/div/div/div/div[2]/div[1]/div/div[1]"
X_PATH_STF_ORIGEM = "//*[@id=\"descricao-procedencia\"]"
X_PATH_STF_RELATOR = "/html/body/div[1]/section[2]/div/div[2]/div/div/div/div/div[2]/div[1]/div/div[3]"
X_PATH_STF_REDATOR = "/html/body/div[1]/section[2]/div/div[2]/div/div/div/div/div[2]/div[1]/div/div[4]"
X_PATH_STF_REL_LAST_INCIDENT = "/html/body/div[1]/section[2]/div/div[2]/div/div/div/div/div[2]/div[1]/div/div[5]"
X_PATH_STF_INFO_1_HEAD = "/html/body/div[1]/section[2]/div/div[2]/div/div/div/div/div[2]/div[1]/div/div[6]/div[1]/div[1]/div[1]"
X_PATH_STF_INFO_1 = "/html/body/div[1]/section[2]/div/div[2]/div/div/div/div/div[2]/div[1]/div/div[6]/div[1]/div[1]/div[2]"
X_PATH_STF_INFO_2_HEAD = "/html/body/div[1]/section[2]/div/div[2]/div/div/div/div/div[2]/div[1]/div/div[6]/div[1]/div[2]/div[1]"
X_PATH_STF_INFO_2 = "/html/body/div[1]/section[2]/div/div[2]/div/div/div/div/div[2]/div[1]/div/div[6]/div[1]/div[2]/div[2]"
X_PATH_STF_INFO_3_HEAD = "/html/body/div[1]/section[2]/div/div[2]/div/div/div/div/div[2]/div[1]/div/div[6]/div[1]/div[3]/div[1]"
X_PATH_STF_INFO_3 = "/html/body/div[1]/section[2]/div/div[2]/div/div/div/div/div[2]/div[1]/div/div[6]/div[1]/div[3]/div[2]"
X_PATH_STF_INFO_4_HEAD = "/html/body/div[1]/section[2]/div/div[2]/div/div/div/div/div[2]/div[1]/div/div[6]/div[1]/div[4]/div[1]"
X_PATH_STF_INFO_4 = "/html/body/div[1]/section[2]/div/div[2]/div/div/div/div/div[2]/div[1]/div/div[6]/div[1]/div[4]/div[2]"

# Tab buttons
X_PATH_STF_BTN_INFO_TAB = "/html/body/div[1]/section[2]/div/div[2]/div/div/div/div/div[2]/div[3]/ul/li[1]/a"
X_PATH_STF_BTN_PARTES_TAB = "/html/body/div[1]/section[2]/div/div[2]/div/div/div/div/div[2]/div[3]/ul/li[2]/a"
X_PATH_STF_BTN_ANDAMENTOS_TAB = "/html/body/div[1]/section[2]/div/div[2]/div/div/div/div/div[2]/div[3]/ul/li[3]/a"
X_PATH_STF_BTN_DECISOES_TAB = "/html/body/div[1]/section[2]/div/div[2]/div/div/div/div/div[2]/div[3]/ul/li[4]/a"
X_PATH_STF_BTN_DESLOCAMENTOS_TAB = "/html/body/div[1]/section[2]/div/div[2]/div/div/div/div/div[2]/div[3]/ul/li[6]/a"
X_PATH_STF_BTN_RECURSOS_TAB = "/html/body/div[1]/section[2]/div/div[2]/div/div/div/div/div[2]/div[3]/ul/li[8]/a"
X_PATH_STF_BTN_PAUTAS_TAB = "/html/body/div[1]/section[2]/div/div[2]/div/div/div/div/div[2]/div[3]/ul/li[9]/a"
X_PATH_STF_BTN_PETICOES_TAB = "/html/body/div[1]/section[2]/div/div[2]/div/div/div/div/div[2]/div[3]/ul/li[7]/a"

# Data inside Info tab
X_PATH_STF_ASSUNTO = "/html/body/div[1]/section[2]/div/div[2]/div/div/div/div/div[2]/div[5]/div[1]/div/div[1]/div[2]/div[2]/ul"
X_PATH_STF_DATA_PROTOC = "/html/body/div/section[2]/div/div[2]/div/div/div/div/div[2]/div[5]/div[1]/div/div[2]/div[1]/div[2]/div[2]"
X_PATH_STF_ORGAO_ORIGEM = "/html/body/div[1]/section[2]/div/div[2]/div/div/div/div/div[2]/div[5]/div[1]/div/div[2]/div[1]/div[2]/div[4]"
X_PATH_STF_NUMERO_ORIGEM = "/html/body/div[1]/section[2]/div/div[2]/div/div/div/div/div[2]/div[5]/div[1]/div/div[2]/div[1]/div[2]/div[8]"
X_PATH_STF_VOLUMES = "/html/body/div[1]/section[2]/div/div[2]/div/div/div/div/div[2]/div[5]/div[1]/div/div[2]/div[2]/div[1]/div[1]"
X_PATH_STF_FOLHAS = "/html/body/div[1]/section[2]/div/div[2]/div/div/div/div/div[2]/div[5]/div[1]/div/div[2]/div[2]/div[2]/div[1]"
X_PATH_STF_APENSOS = "/html/body/div[1]/section[2]/div/div[2]/div/div/div/div/div[2]/div[5]/div[1]/div/div[2]/div[2]/div[3]/div[1]"

# Data inside "Partes" tab
X_PATH_STF_TODAS_PARTES = "//*[@id=\"todas-partes\"]"

# Data inside "Decisoes" tab
X_PATH_STF_DECISOES_FRAME = "//*[@id=\"decisoes\"]"
X_PATH_STF_DECISAO_DATA = "/html/body/div[1]/section[2]/div/div[2]/div/div/div/div/div[2]/div[5]/div[4]/div/div[1]/div/div/div/div[1]/div"
X_PATH_STF_DECISAO_TITULO = "/html/body/div[1]/section[2]/div/div[2]/div/div/div/div/div[2]/div[5]/div[4]/div/div[1]/div/div/div/div[2]/h5"
X_PATH_STF_DECISAO_JULGADOR = ""

# Data inside "Deslocamentos" tab
X_PATH_STF_DESLOCAMENTOS_FRAME = "//*[@id=\"deslocamentos\"]"
X_PATH_STF_DESLOCAMENTOS_ITEM = "//*[@class=\"col-md-12 lista-dados p-r-0 p-l-0\"]"

# Data inside "Petições" tab
X_PATH_STF_PETICOES_FRAME = "//*[@id=\"peticoes\"]"
X_PATH_STF_PETICOES_ITEM = "//*[@class=\"col-md-12 lista-dados\"]"

# Data inside "Recursos" tab
X_PATH_STF_RECURSOS_FRAME = "//*[@id=\"recursos\"]"
X_PATH_STF_RECURSOS_ITEM = "//*[@class=\"col-md-12 lista-dados\"]"

# Data inside "Pautas" tab
X_PATH_STF_PAUTAS_FRAME = "//*[@id=\"pautas\"]"
X_PATH_STF_PAUTAS_ITEM = "//*[@class=\"andamento-item\"]"

# ============================================================= #
#                          STJ METADATA                         #
# ============================================================= #
BASE_URL_STJ_METADATA = "https://ww2.stj.jus.br/processo/pesquisa/"
X_PATH_STJ_INPUT_NUM_REGISTRO = "//*[@id=\"idNumeroRegistro\"]"
X_PATH_STJ_INPUT_NUM_UNICO = "//*[@id=\"idNumeroUnico\"]"

# Data inside "Detalhes" tab
X_PATH_STJ_DATA_ATUACAO = "//*[@id=\"idDataAutuacaoCabecalho\"]"
X_PATH_STJ_BLOCOS = "//*[@id=\"idDivDetalhes\"]"
X_PATH_STJ_LINHA_DETALHES = "//*[@class=\"classDivLinhaDetalhes\"]"

# Data inside "Fases" tab
X_PATH_STJ_FASES_FRAME = "//*[@id=\"idSpanAbaFases\"]"
X_PATH_STJ_BLOCOS_FASES = "//*[@id=\"idDivFases\"]"
X_PATH_STJ_LINHA_FASES = "//*[@class=\"classDivFaseLinha\"]"

# Data inside Petições tab
X_PATH_STJ_PETICOES_FRAME = "//*[@id=\"idSpanAbaPeticoes\"]"
X_PATH_STJ_BLOCOS_PETICOES = "//*[@id=\"idDivPeticoes\"]"
X_PATH_STJ_LINHA_PETICOES = "//*[@class=\"classDivLinhaPeticoes\"]"
X_PATH_STJ_PETICOES_LINHA_NUM = "classSpanLinhaPeticoesNum"
X_PATH_STJ_PETICOES_LINHA_TIPO = "classSpanLinhaPeticoesTipo"
X_PATH_STJ_PETICOES_LINHA_DATA_PROTOCOLO = "classSpanLinhaPeticoesProtocolo"
X_PATH_STJ_PETICOES_LINHA_DATA_PROCESSAMENTO = "classSpanLinhaPeticoesProcessamento"
X_PATH_STJ_PETICOES_LINHA_QUEM = "classSpanLinhaPeticoesQuem"

# Data inside Pautas tab
X_PATH_STJ_PAUTAS_FRAME = "//*[@id=\"idDivPautas\"]"


match_keys = {
    "num_unico": "numero_unico"
}