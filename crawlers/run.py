"""

@author Thiago Raulino Dal Pont
"""
from crawler import webcrawl_stf_process, webcrawl_tjsc_process, webcrawl_stj_process, download_stf_documents, webcrawl_stf_metadata, webcrawl_stj_metadata, \
    webcrawler_jusbrasil_process


def stf_process_crawler():
    """
    Search and download jurisprudence documents from STF search webpage.
    :return: None
    """
    print("Get STF Data")

    # Search for processes and get their links.
    webcrawl_stf_process.get_process_links()
    # Using the acquired links to get the files downloaded
    download_stf_documents.download()


def stj_process_crawler():
    """
    Search and download jurisprudence documents from STJ search webpage.
    :return: None
    """
    print("Get STJ Data")
    webcrawl_stj_process.crawler()


def tjsc_process_crawler():
    """
    Search and download jurisprudence documents from TJ-SC search webpage.
    :return:
    """
    print("Get TJ-SC Data")
    webcrawl_tjsc_process.crawler()
    webcrawl_tjsc_process.download_files_tj_sc()


def jusbrasil_process_crawler():
    webcrawler_jusbrasil_process.jusbrasil_crawl()
    webcrawler_jusbrasil_process.merge_links()
    webcrawler_jusbrasil_process.download_documents()


def stf_metadata_crawler():
    """
    Search and download metadata of downloaded documents from STF
    :return:
    """
    webcrawl_stf_metadata.metadata_acquisition()


def stj_metadata_crawler():
    """
    Search and download metadata of downloaded documents from STJ
    :return:
    """
    webcrawl_stj_metadata.metadata_acquisition()


def tj_sc_metadata_crawler():
    """
    :return: 
    """
    # TODO: implement crawler
    return None


def main():
    """
    Before running this script, make sure you updated all path string in utils.constants.py according to your setup.
    Check also the crawlers' files. There will be some local paths used in those files that you also need to check.
    In this project, many libraries are required.
    As you run this script, errors will appoint missing libs and to download them, just type on terminal:
        pip install name_of_the_library
    """

    # Get documents
    stf_process_crawler()
    stj_process_crawler()
    tjsc_process_crawler()
    jusbrasil_process_crawler()

    # Get metadata from documents (only after it gets the files downloaded)
    stf_metadata_crawler()
    stj_metadata_crawler()
    tj_sc_metadata_crawler()


if __name__ == "__main__":
    main()
