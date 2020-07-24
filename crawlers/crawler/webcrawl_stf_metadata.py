"""
@description:
    Crawler to capture metadata from jurisprudence procedures.
@author:
    Thiago R. Dal Pont and E-GOV researchers
@group:
    E-GOV Research Group

@available_metadata:

"""
import random
import time

import jsonlines
import tqdm
from selenium import webdriver

import utils
from utils import file_utils
from utils.constants import *

sample_procedures_ids = [
    "965.513",
    "1.256.277",
    None,
    "1.246.033",
    "1.131.571",
    "1.166.183",
    None,
    "119.775",
    "135.653",
    "758",
]


def search_info_xpath(driver, x_path):
    try:
        data_obj = driver.find_element_by_xpath(x_path)
        data = data_obj.text
    except:
        data = ""

    return data


def format_string(text):
    for char in "\n\t":
        text = text.replace(char, " ")
    for i in range(5):
        text = text.replace("  ", " ")
    text = text.strip().upper()

    return text


def search_info_class(driver, class_name):
    try:
        data_obj = driver.find_element_by_class(class_name)
        data = data_obj.text
    except:
        data = ""

    return data


def search_page(driver, proc_id):
    print("Loaded")

    if proc_id == "":
        return None

    # Get Object
    search_input_obj = driver.find_element_by_xpath(X_PATH_STF_INPUT_SEARCH_BOX)
    # Insert Text
    search_input_obj.send_keys(proc_id)
    # Search
    btn_search_obj = driver.find_element_by_xpath(X_PATH_STF_METADATA_BUTTON_SEARCH)
    btn_search_obj.click()
    print("Searching         ", proc_id)

    time.sleep(3)
    # Enter the first link if it exists
    list_related_proc = driver.find_elements_by_xpath(X_PATH_STF_LIST_RELATED_PROC)

    if len(list_related_proc) == 0:
        print("Process not found")
        return None
    print("Process found")

    final_link = None
    links = list_related_proc[0].find_elements_by_tag_name("a")
    for link in links:
        if link.text.startswith("RE "):
            final_link = link
            break

    if final_link is None:
        print("RE Process not found")
        return None

    final_link.click()
    print("Entering process")

    ####################################################################################################################
    #                                                   Get MetaInfo                                                   #
    ####################################################################################################################
    tipo_processo = search_info_xpath(driver, X_PATH_STF_PHYSICAL_DIGITAL_TYPE)
    nivel_segredo = search_info_xpath(driver, X_PATH_STF_NIVEL_RESTRICAO)
    numero_unico = search_info_xpath(driver, X_PATH_STF_NUMERO_UNICO_PROC).lower().replace("número único:", "").strip().replace(" ", "_").replace("ú", "u")
    classe_processo = search_info_xpath(driver, X_PATH_STF_PROC_CLASSE)
    origem = search_info_xpath(driver, X_PATH_STF_ORIGEM)
    relator = search_info_xpath(driver, X_PATH_STF_RELATOR).replace("Relator:", "")
    redator = search_info_xpath(driver, X_PATH_STF_REDATOR).replace("Redator:", "").replace("Redator do acórdão:", "")
    relator_ultimo_incidente = search_info_xpath(driver, X_PATH_STF_REL_LAST_INCIDENT).replace("Relator do último incidente:", "")

    # Sometimes "relator_ultimo_incidente" returns the more info then it should and it's wrong information.
    if len(relator_ultimo_incidente.split()) > 10:
        # print("Relator too big:", relator_ultimo_incidente)
        relator_ultimo_incidente = ""

    # # The following data appears below the "Relator do documento/acórdão"
    # info_1_header = search_info_xpath(driver, X_PATH_STF_INFO_1_HEAD).upper()
    # info_1 = search_info_xpath(driver, X_PATH_STF_INFO_1).upper()
    #
    # info_2_header = search_info_xpath(driver, X_PATH_STF_INFO_2_HEAD)
    # info_2 = search_info_xpath(driver, X_PATH_STF_INFO_2).upper()
    #
    # info_3_header = search_info_xpath(driver, X_PATH_STF_INFO_3_HEAD)
    # info_3 = search_info_xpath(driver, X_PATH_STF_INFO_3).upper()
    #
    # info_4_header = search_info_xpath(driver, X_PATH_STF_INFO_4_HEAD)
    # info_4 = search_info_xpath(driver, X_PATH_STF_INFO_4).upper()

    # Info from "informações" tab
    btn_info_obj = driver.find_element_by_xpath(X_PATH_STF_BTN_INFO_TAB)
    try:
        btn_info_obj.click()
    except Exception as e:
        print("Error while entering Info tab:\t", e)

    time.sleep(1)
    list_assuntos = list()

    splits = search_info_xpath(driver, X_PATH_STF_ASSUNTO).split("\n")
    for split in splits:
        dict_assunto = dict()
        dict_assunto["assunto"] = format_string(split.replace("| |", "|"))
        list_assuntos.append(dict_assunto)
    data_protocolo = search_info_xpath(driver, X_PATH_STF_DATA_PROTOC)
    orgao_origem = search_info_xpath(driver, X_PATH_STF_ORGAO_ORIGEM)

    # TAB "Partes"
    btn_partes_obj = driver.find_element_by_xpath(X_PATH_STF_BTN_PARTES_TAB)

    try:
        btn_partes_obj.click()
    except Exception  as e:
        print("Error while entering 'Partes' tab:\t", e)

    time.sleep(1)
    partes_obj = driver.find_element_by_xpath(X_PATH_STF_TODAS_PARTES)

    partes_splits = partes_obj.text.split("\n")

    # TAB "Andamentos"
    btn_andamentos_obj = driver.find_element_by_xpath(X_PATH_STF_BTN_ANDAMENTOS_TAB)
    try:
        btn_andamentos_obj.click()
        time.sleep(1)
    except:
        pass

    list_andamentos_obj = driver.find_elements_by_class_name("andamento-item")
    list_andamentos_final = list()

    for andamento_obj in list_andamentos_obj:
        text = andamento_obj.text

        if text == "":
            continue

        splits = text.split("\n")

        andamento_dict = dict()

        data_andamento = splits[0]
        descricao_andamento = splits[1]

        try:
            comentario_andamento = splits[2]
        except:
            comentario_andamento = ""

        andamento_dict["data_andamento"] = format_string(data_andamento)
        andamento_dict["descricao_andamento"] = format_string(descricao_andamento)
        andamento_dict["comentario_andamento"] = format_string(comentario_andamento)

        list_andamentos_final.append(andamento_dict)

    # Tab "Decisões"
    btn_decisoes_obj = driver.find_element_by_xpath(X_PATH_STF_BTN_DECISOES_TAB)
    try:
        btn_decisoes_obj.click()
        time.sleep(2)
    except:
        pass

    list_frame_obj = driver.find_element_by_xpath(X_PATH_STF_DECISOES_FRAME)
    list_decisoes_obj = list_frame_obj.find_elements_by_class_name("andamento-item")
    list_decisoes_final = list()

    for decisao_obj in list_decisoes_obj:
        text = decisao_obj.text
        # print("Decisão\t", decisao_obj.text)
        splits = text.split("\n")

        data = splits[0]
        titulo = splits[1]
        julgador = splits[2]

        try:
            texto = splits[3]
        except:
            texto = ""

        decisao_dict = dict()

        decisao_dict["data_decisao"] = format_string(data)
        decisao_dict["titulo_decisao"] = format_string(titulo)
        decisao_dict["julgador_decisao"] = format_string(julgador)

        list_decisoes_final.append(decisao_dict)

    # Tab "Deslocamentos"
    btn_deslocamentos_obj = driver.find_element_by_xpath(X_PATH_STF_BTN_DESLOCAMENTOS_TAB)
    try:
        btn_deslocamentos_obj.click()
        time.sleep(2)
    except:
        pass

    deslocamentos_frame_obj = driver.find_element_by_xpath(X_PATH_STF_DESLOCAMENTOS_FRAME)
    list_deslocamentos_obj = deslocamentos_frame_obj.find_elements_by_xpath(X_PATH_STF_DESLOCAMENTOS_ITEM)

    list_deslocamentos_final = list()
    for deslocamento_obj in list_deslocamentos_obj:
        text = deslocamento_obj.text.strip()
        splits = text.split("\n")

        if len(splits) == 0:
            continue

        titulo = splits[0]
        comentario = splits[1]
        guia = splits[2]
        data = ""
        if len(splits) > 3:
            data = splits[3]

        deslocamento_dict = dict()
        deslocamento_dict["titulo_deslocamento"] = format_string(titulo)
        deslocamento_dict["comentario_deslocamento"] = format_string(comentario)
        deslocamento_dict["guia_deslocamento"] = format_string(guia)
        deslocamento_dict["data_deslocamento"] = format_string(data)

        # print(deslocamento_dict)
        list_deslocamentos_final.append(deslocamento_dict)

    # Tab "Petições"
    btn_peticoes_obj = driver.find_element_by_xpath(X_PATH_STF_BTN_PETICOES_TAB)
    try:
        btn_peticoes_obj.click()
        time.sleep(1)
    except:
        pass

    peticoes_frame_obj = driver.find_element_by_xpath(X_PATH_STF_PETICOES_FRAME)
    list_peticoes_obj = peticoes_frame_obj.find_elements_by_xpath(X_PATH_STF_PETICOES_ITEM)
    list_peticoes_final = list()

    for peticao_obj in list_peticoes_obj:
        if peticao_obj.text == "":
            continue

        text = peticao_obj.text
        numero = peticao_obj.find_element_by_class_name("processo-detalhes-bold")
        numero = numero.text
        text = text.replace(numero, "").split("\n")
        data_peticionado = text[0]
        data_recebido = text[1]

        peticao_dict = dict()

        peticao_dict["numero_peticao"] = format_string(numero)
        peticao_dict["data_peticionado_peticao"] = format_string(data_peticionado)
        peticao_dict["data_recebimento_peticao"] = format_string(data_recebido)
        # print(peticao_dict)
        list_peticoes_final.append(peticao_dict)

    # Tab "Recursos"
    btn_recursos_obj = driver.find_element_by_xpath(X_PATH_STF_BTN_RECURSOS_TAB)
    try:
        btn_recursos_obj.click()
        time.sleep(1)
    except:
        pass

    recursos_frame_obj = driver.find_element_by_xpath(X_PATH_STF_RECURSOS_FRAME)
    list_recursos_obj = recursos_frame_obj.find_elements_by_xpath(X_PATH_STF_RECURSOS_ITEM)
    list_recursos_final = list()

    for recurso_obj in list_recursos_obj:
        if recurso_obj.text == "":
            continue

        text = recurso_obj.text
        recurso_dict = dict()

        recurso_dict["titulo_recurso"] = format_string(text)
        list_recursos_final.append(recurso_dict)

    # Tab Pautas

    btn_pautas_obj = driver.find_element_by_xpath(X_PATH_STF_BTN_PAUTAS_TAB)
    try:
        btn_pautas_obj.click()
        time.sleep(1)
    except:
        pass

    pautas_frame_obj = driver.find_element_by_xpath(X_PATH_STF_PAUTAS_FRAME)
    list_pautas_obj = pautas_frame_obj.find_elements_by_xpath(X_PATH_STF_PAUTAS_ITEM)
    list_pautas_final = list()

    for pautas_obj in list_pautas_obj:
        if pautas_obj.text == "":
            continue

        splits = pautas_obj.text.split("\n")

        data_obj = pautas_obj.find_element_by_class_name("andamento-data")
        data = data_obj.text

        nome_obj = pautas_obj.find_element_by_class_name("andamento-nome")
        nome = nome_obj.text

        if len(splits) > 2:
            descricao = splits[2]
        else:
            descricao = ""

        pautas_dict = dict()
        pautas_dict["nome"] = format_string(nome)
        pautas_dict["data"] = format_string(data)
        pautas_dict["descricao"] = format_string(descricao)
        list_pautas_final.append(pautas_dict)

    ################################################################

    # print("Type process:           ", tipo_processo)
    # print("Level of Secrecy:       ", nivel_segredo)
    # print("Unique Number:          ", numero_unico)
    # print("Process Class:          ", classe_processo)
    # print("Origin:                 ", origem)
    # print("Relator:                ", relator)
    # print("Redator:                ", redator)
    # print("Relator last incident:  ", relator_ultimo_incidente)
    # print("Info 1:                 ", info_1_header, "\t|\t", info_1)
    # print("Info 2:                 ", info_2_header, "\t|\t", info_2)
    # print("Info 3:                 ", info_3_header, "\t|\t", info_3)
    # print("Info 4:                 ", info_4_header, "\t|\t", info_4)

    proc_dict = dict()
    proc_dict["num_processo"] = format_string(str(proc_id))
    proc_dict["tipo_processo"] = format_string(tipo_processo)
    proc_dict["nivel_sigilo"] = format_string(nivel_segredo)
    proc_dict["numero_unico"] = format_string(numero_unico)
    proc_dict["classe"] = format_string(classe_processo)
    proc_dict["origem"] = format_string(origem)
    proc_dict["relator"] = format_string(relator)
    proc_dict["redator"] = format_string(redator)
    proc_dict["relator_ultimo_incidente"] = format_string(relator_ultimo_incidente)
    proc_dict["assuntos"] = list_assuntos
    proc_dict["data_protocolo"] = format_string(data_protocolo)
    proc_dict["orgao_origem"] = format_string(orgao_origem)

    # Continue "Partes" processing
    header = ""
    for index in range(len(partes_splits)):
        # If it's header
        if index % 2 == 0:
            header = partes_splits[index]
        # If it's content
        elif header != "":
            header = process_header(header)
            proc_dict[header] = format_string(partes_splits[index])
            header = ""

    proc_dict["andamentos"] = list_andamentos_final
    proc_dict["decisoes"] = list_decisoes_final
    proc_dict["deslocamentos"] = list_deslocamentos_final
    proc_dict["peticoes"] = list_peticoes_final
    proc_dict["recursos"] = list_recursos_final
    proc_dict["pautas"] = list_pautas_final

    print(proc_dict)

    print("Writing to output JSON lines file...")
    with jsonlines.open(PROC_METADATA_OUTPUT_FILE, mode="a") as writer:
        writer.write(proc_dict)

    time.sleep(1)


def process_header(text):
    text = text.lower()
    for char in "()./\\| ":
        text = text.replace(char, "_")

    for i in range(10):
        text = text.replace("__", "_")

    return text.strip("_")


def metadata_acquisition():
    procedures_ids = list()

    time.sleep(2)

    file_utils.clear_file(PROC_METADATA_OUTPUT_FILE.replace("@", "stf"))

    # Load Process Numbers from Pablo's Extraction Code Output
    with jsonlines.open(PROC_NUMBER_INPUT_FILE.replace("@", "stf")) as f:
        print("Reading Input File")
        for process_json in tqdm.tqdm(f.iter()):
            # procedures_ids.append(process_json["num_processo"])
            print(process_json["num_processo"])

    # Shuffle the list (optional)
    random.shuffle(sample_procedures_ids)
    procedures_ids = sample_procedures_ids

    # Start Firefox browser
    driver = webdriver.Firefox()

    # Send request to STF page.
    driver.get(BASE_URL_STF_METADATA)
    time.sleep(1)
    # Iterate through each process id
    for proc_id in tqdm.tqdm(sample_procedures_ids):
        if proc_id is None or proc_id == "":
            print("Skipping empty procedure...")
            continue

        # Remove dashes and dots
        new_id = proc_id.split("-")[0]
        new_id = new_id.replace(".", "")

        search_page(driver, new_id)

    driver.close()
    driver.quit()


if __name__ == "__main__":
    metadata_acquisition()
