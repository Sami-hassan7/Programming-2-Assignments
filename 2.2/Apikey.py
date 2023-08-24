from Bio import Entrez
import ssl
import multiprocessing as mp
import time
import logging

# Configure settings to prevent certificate verification errors.
ssl._create_default_https_context = ssl._create_unverified_context

# Email and API key setup as instructed 
Entrez.email = 's.h.moon@st.hanze.nl'
api_key = '8f70d97b01baecc0f8d5b40b960351667908'


#Set up logging configuration.
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def download_article(pubmed_id, mode='parallel'):
    """
    This function concurrently downloads articles. 
    It requires a PubMed ID (pubmed_id) and the desired number of articles (amount) as inputs.
    """
    try:
        handle = Entrez.efetch(db='pubmed', id=pubmed_id, retmode='xml', api_key=api_key)
        xml_data = handle.read()
        handle.close()

        file_name = f'{mode}_{pubmed_id}.xml'
        with open(file_name, 'wb') as file:
            file.write(xml_data)
        
        logging.info(f'Successfully downloaded article {pubmed_id} in {mode} mode.')
    except Exception as e:
        logging.error(f'Error occurred while downloading article {pubmed_id}: {str(e)}')

def get_references(amount, pubmed_id):
    """
    This function gathers a collection of references for the designated article. 
    Subsequently, it employs multiprocessing to generate a worker pool, with each worker utilizing the download_article function to retrieve an article.
    """
    try:
        file = Entrez.elink(dbfrom='pubmed', db='pmc', LinkName='pubmed_pmc_refs', id=pubmed_id, api_key=api_key)
        results = Entrez.read(file)
        file.close()
        references = [link['Id'] for link in results[0]['LinkSetDb'][0]['Link']]
        
        return references[:amount]
    except Exception as e:
        logging.error(f'Error occurred while retrieving references for article {pubmed_id}: {str(e)}')
        return []

def print_duration_time(start_time, end_time, execution_desc):
    """
    Display the elapsed time by considering the start and end timestamps.

    Inputs:

        start_time (float): Initial execution time.
        end_time (float): Final execution time.
        execution_desc (str): Title for the execution.

    Outout:
        None
    """
    logging.info(f'Total time of {execution_desc} is: {end_time - start_time}')

def download_parallel(pubmed_id, amount):
    """
    The articles are stored as XML files, with their names derived from their respective PubMed IDs. 
    The duration of execution, involving both reference retrieval and parallel article downloading, is calculated and displayed.
    """
    try:
        start_time = time.time()
        references = get_references(amount, pubmed_id)
        end_time = time.time()
        print_duration_time(start_time, end_time, "getting references")
        
        start_time = time.time()
        with mp.Pool() as pool:
            pool.map(download_article, references)
        end_time = time.time()
        print_duration_time(start_time, end_time, "downloading articles in parallel")
    except Exception as e:
        logging.error(f'Error occurred during parallel downloading: {str(e)}')

def download_sequential(pubmed_id, amount):
    
    """
    This function downloads articles in a sequential manner. 
    It employs a process akin to downloadParallel, but instead of utilizing multiprocessing, 
    it employs a for loop to download each article individually, in sequence.
    """
    try:
        references = get_references(amount, pubmed_id)
        
        start_time = time.time()
        for reference in references:
            download_article(reference, "sequential")
        end_time = time.time()
        print_duration_time(start_time, end_time, "downloading articles sequentially")
    except Exception as e:
        logging.error(f'Error occurred during sequential downloading: {str(e)}')

if __name__ == '__main__': 
    logging.info("Starting the script...")
    pubmed_id = '29635200'
    amount = 10
    download_parallel(pubmed_id, amount)
    download_sequential(pubmed_id, amount)
    logging.info("Script execution completed.")
