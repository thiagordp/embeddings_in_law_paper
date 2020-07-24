"""
@description:
    Crawler to capture metadata from jurisprudence procedures.
@author:
    Thiago R. Dal Pont and E-GOV researchers
@group:
    E-GOV Research Group

@available_metadata:

"""
import datetime
import random
import time
import traceback

import jsonlines
import tqdm
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import numpy as np

import utils
import unicodedata

from utils import file_utils
from utils.constants import *


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


def write_metadata_output(metadata_json, error):
    if error:
        file_name = PROC_METADATA_OUTPUT_FILE.replace("@", "stj_error").replace("$", "00")
    else:
        file_name = PROC_METADATA_OUTPUT_FILE.replace("@", "stj").replace("$", "00")

    with jsonlines.open(file_name, mode="a") as writer:
        writer.write(metadata_json)


def process_header(text):
    for char in "./*:;|\\()":
        text = text.replace(char, " ")
    for i in range(10):
        text = text.replace("  ", " ")

    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8")
    text = text.strip().lower().replace(" ", "_")

    key_dict = {
        "numero_unico": "num_unico"
    }

    return text


def search_metadata(driver, metadata_json):
    finished = False
    num_registro = ""
    num_unico = ""
    # print("---------------------------------------------------------------------------------------------------")

    advogados = list()
    procuradores = list()
    embargantes = list()
    recorridos = list()
    recorrentes = list()
    agravantes = list()
    interessados = list()
    reus = list()
    requerentes = list()
    agravos = list()
    embargados = list()
    exequentes = list()
    autores = list()
    impetrados = list()
    pacientes = list()
    impetrantes = list()
    suscitados = list()
    reclamantes = list()
    missing_list = list()
    requeridos = list()
    reclamados = list()
    representados_por = list()
    suscitantes = list()
    fases = list()
    peticoes = list()
    pautas = list()

    descricao_erro = ""

    i = 0
    for i in range(3):
        try:
            num_registro = metadata_json["num_registro"]
            num_unico = metadata_json["num_unico"]

            # print(num_registro, num_unico)

            # If both id keys are empty, just write the dict to output metadata file.
            if metadata_json["erro"]:
                write_metadata_output(metadata_json, error=True)
                return None

            driver.get(BASE_URL_STJ_METADATA)
            time.sleep(2)

            if num_registro is not None:
                input_obj = driver.find_element_by_xpath(X_PATH_STJ_INPUT_NUM_REGISTRO)
                input_text = num_registro
            elif num_unico is not None:
                input_obj = driver.find_element_by_xpath(X_PATH_STJ_INPUT_NUM_UNICO)
                input_text = num_unico
            else:
                return None

            for char in "/-.":
                input_text = input_text.replace(char, "")
            input_obj.send_keys("")
            time.sleep(0.5)
            input_obj.send_keys(input_text)
            time.sleep(0.5)
            input_obj.send_keys(Keys.RETURN)
            time.sleep(1)

            ####################################################################################################################
            #                                                   Get MetaInfo                                                   #
            ####################################################################################################################

            # ------------------------------------------------- Detalhes tab --------------------------------------------------#
            bloco_1 = None
            linha_objs = None
            for not_ok_index in range(25):
                try:
                    bloco_1 = driver.find_element_by_xpath(X_PATH_STJ_BLOCOS)
                    linha_objs = bloco_1.find_elements_by_xpath(X_PATH_STJ_LINHA_DETALHES)
                    break
                except:
                    time.sleep(0.1)
                    pass

            for linha in linha_objs:
                tokens = linha.text.replace(":", "").strip().split("\n")
                if len(tokens) != 2:
                    continue

                header = process_header(tokens[0])
                content = tokens[1].strip().upper()

                # print(header, "|", content)
                if header.find("advog") != -1:
                    advogados.append(content)
                elif header.find("procurador") != -1:
                    procuradores.append(content)
                elif header.find("embargante") != -1:
                    embargantes.append(content)
                elif header.find("recorrido") != -1:
                    recorridos.append(content)
                elif header.find("recorrente") != -1:
                    recorrentes.append(content)
                elif header.find("agravante") != -1:
                    agravantes.append(content)
                elif header.find("interes") != -1:
                    interessados.append(content)
                elif header.find("reu") != -1:
                    reus.append(content)
                elif header.find("requerente") != -1:
                    requerentes.append(content)
                elif header.find("agravado") != -1:
                    agravos.append(content)
                elif header.find("embargado") != -1:
                    embargados.append(content)
                elif header.find("exequente") != -1:
                    exequentes.append(content)
                elif header.find("autor") != -1:
                    autores.append(content)
                elif header.find("impetrado") != -1:
                    impetrados.append(content)
                elif header.find("paciente") != -1:
                    pacientes.append(content)
                elif header.find("impetrante") != -1:
                    impetrantes.append(content)
                elif header.find("suscitado") != -1:
                    suscitados.append(content)
                elif header.find("reclamante") != -1:
                    reclamantes.append(content)
                elif header.find("requerido") != -1:
                    requeridos.append(content)
                elif header.find("reclamado") != -1:
                    reclamados.append(content)
                elif header.find("repr_por") != -1:
                    representados_por.append(content)
                elif header.find("suscitantes") != -1:
                    suscitantes.append(content)

                else:
                    header = header.replace("numero_unico", "num_unico")
                    if header in metadata_json.keys():
                        missing_list.append(header)
                        missing_list = list(set(missing_list))

                    header = process_header(header)
                    metadata_json[header] = content

            if (len(missing_list) > 0 and "num_unico" not in missing_list) or len(missing_list) > 1:
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "\tMissing: ", missing_list)
            # ------------------------------------------------------------------------------- #
            fases_obj = driver.find_element_by_xpath(X_PATH_STJ_FASES_FRAME)
            fases_obj.find_element_by_link_text("Fases").click()
            time.sleep(0.1)

            blocos_obj = driver.find_element_by_xpath(X_PATH_STJ_BLOCOS_FASES)
            linha_objs = blocos_obj.find_elements_by_xpath(X_PATH_STJ_LINHA_FASES)

            for linha in linha_objs:
                text = linha.text

                if text.strip() == "":
                    continue

                date = text[0:10].strip()
                hour = text[10:15].strip()
                content = text[15:].strip().upper()

                fase_dict = dict()
                fase_dict["data"] = date
                fase_dict["hora"] = hour
                fase_dict["descricao"] = content

                fases.append(fase_dict)

            # ------------------------------------------------------------------------------- #
            peticoes_obj = driver.find_element_by_xpath(X_PATH_STJ_PETICOES_FRAME)
            peticoes_obj.find_element_by_link_text("Petições").click()
            time.sleep(0.1)

            blocos_obj = driver.find_element_by_xpath(X_PATH_STJ_BLOCOS_PETICOES)
            linhas = blocos_obj.find_elements_by_xpath(X_PATH_STJ_LINHA_PETICOES)

            for linha in linhas:
                num = linha.find_element_by_class_name(X_PATH_STJ_PETICOES_LINHA_NUM).text
                tipo = linha.find_element_by_class_name(X_PATH_STJ_PETICOES_LINHA_TIPO).text
                data_protocolo = linha.find_element_by_class_name(X_PATH_STJ_PETICOES_LINHA_DATA_PROTOCOLO).text
                data_processamento = linha.find_element_by_class_name(X_PATH_STJ_PETICOES_LINHA_DATA_PROCESSAMENTO).text
                quem = linha.find_element_by_class_name(X_PATH_STJ_PETICOES_LINHA_QUEM).text

                peticao_dict = dict()
                peticao_dict["num_peticao"] = num.strip().upper()
                peticao_dict["tipo_peticao"] = tipo.strip().upper()
                peticao_dict["data_protoc_peticao"] = data_protocolo.strip().upper()
                peticao_dict["data_proces_peticao"] = data_processamento.strip().upper()
                peticao_dict["quem_peticao"] = quem.strip().upper()

                peticoes.append(peticao_dict)
            # ------------------------------------------------------------------------------- #
            driver.find_element_by_link_text("Pautas").click()
            pautas_obj = driver.find_element_by_xpath(X_PATH_STJ_PAUTAS_FRAME)

            linhas_obj = pautas_obj.find_elements_by_class_name("clsBlocoPautaLinha")

            for linha_obj in linhas_obj:
                attributes = linha_obj.find_elements_by_tag_name("span")

                data_sessao = attributes[0].text.strip().upper()
                hora_sessao = attributes[1].text.strip().upper()
                orgao_sessao = attributes[2].text.strip().upper()

                pauta_dict = dict()
                pauta_dict["data_sessao_pauta"] = data_sessao
                pauta_dict["hora_sessao_pauta"] = hora_sessao
                pauta_dict["orgao_sessao_pauta"] = orgao_sessao
                pautas.append(pauta_dict)

            finished = True
            break
        except Exception as e:
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "\tError: ", num_unico, num_registro, e)
            descricao_erro = str(e) + "\n\n" + traceback.format_exc()
            time.sleep(1 + i * 5)

    metadata_json["erro"] = not finished

    if not finished:
        metadata_json["descricao_erro"] = descricao_erro
        write_metadata_output(metadata_json, error=True)
    else:
        metadata_json["advogados"] = advogados
        metadata_json["procuradores"] = procuradores
        metadata_json["embargantes"] = embargantes
        metadata_json["recorridos"] = recorridos
        metadata_json["recorrentes"] = recorrentes
        metadata_json["agravantes"] = agravantes
        metadata_json["interessados"] = interessados
        metadata_json["reus"] = reus
        metadata_json["requerentes"] = requerentes
        metadata_json["agravos"] = agravos
        metadata_json["embargados"] = embargados
        metadata_json["exequentes"] = exequentes
        metadata_json["autores"] = autores
        metadata_json["impetrados"] = impetrados
        metadata_json["pacientes"] = pacientes
        metadata_json["impetrantes"] = impetrantes
        metadata_json["suscitados"] = suscitados
        metadata_json["reclamantes"] = reclamantes
        metadata_json["requeridos"] = requeridos
        metadata_json["reclamados"] = reclamados
        metadata_json["representados_por"] = representados_por
        metadata_json["suscitantes"] = suscitantes
        metadata_json["fases"] = fases
        metadata_json["peticoes"] = peticoes
        metadata_json["pautas"] = pautas

        write_metadata_output(metadata_json, error=False)

    # print(metadata_json)


def div_metadata_file(file_path):
    print(file_path)
    metadatas = list()
    with jsonlines.open(file_path) as f:
        for process_json in tqdm.tqdm(f.iter()):
            metadatas.append(process_json)

    arrays = np.array_split(metadatas, 4)

    for i, split_array in tqdm.tqdm(enumerate(arrays)):
        arr = list(split_array)
        file_name = PROC_NUMBER_INPUT_FILE.replace("@", "stj").replace("$", str(i).zfill(2))
        with jsonlines.open(file_name, mode="a") as writer:
            for line in arr:
                string = str(line)
                writer.write(line)


def metadata_acquisition():
    print("--------------------------------------------------------")
    print("-                 STJ METADATA EXTRACTION              -")
    print("--------------------------------------------------------")

    # div_metadata_file(PROC_NUMBER_INPUT_FILE.replace("@", "stj").replace("_$", ""))

    num_file = "00"
    tribunal = "stj"
    source_metadatas = list()

    output_file = PROC_METADATA_OUTPUT_FILE.replace("@", tribunal).replace("$", num_file)
    output_file_error = PROC_METADATA_OUTPUT_FILE.replace("@", tribunal + "_error").replace("$", num_file)
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "\tCleaning output files:", output_file, output_file_error)

    file_utils.clear_file(output_file)
    file_utils.clear_file(output_file_error)

    input_file = PROC_NUMBER_INPUT_FILE.replace("@", tribunal).replace("$", num_file)
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "\tReading Input File:", input_file)

    # Load Process Numbers from Pablo's Extraction Code Output
    with jsonlines.open(input_file) as f:
        for process_json in tqdm.tqdm(f.iter()):
            source_metadatas.append(process_json)

    random.shuffle(source_metadatas)
    print("Searching")

    # Start Firefox browser
    driver = webdriver.Firefox()

    # Send request to STF page.
    driver.get(BASE_URL_STJ_METADATA)

    count_reg = count_unico = 0
    for metadata in tqdm.tqdm(source_metadatas):
        try:
            if random.random() < 0.1:
                driver.close()
                driver.quit()
                driver = webdriver.Firefox()

            num_registro = metadata["num_registro"]
            num_unico = metadata["num_unico"]

            if num_unico is None:
                count_unico += 1
            if num_registro is None:
                count_reg += 1

            if num_unico is None and num_registro is None:
                metadata["erro"] = True
            else:
                metadata["erro"] = False

            search_metadata(driver, metadata)
        except Exception as e:
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "\t", e)

    print(count_unico, count_reg)
    driver.close()
    driver.quit()


if __name__ == "__main__":
    metadata_acquisition()
