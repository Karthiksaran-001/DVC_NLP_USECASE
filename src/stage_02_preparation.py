import argparse
import os
import shutil
from tqdm import tqdm
import logging
from src.utils.common import read_yaml, create_directories
from src.utils.data_mng import process_posts
import random

STAGE = "One" ## <<< change stage name 

logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )


def load_data(config_path, params_path):
    config = read_yaml(config_path)
    params = read_yaml(params_path)
    
    source_data = config["source_download_dir"]
    input_data = os.path.join(source_data["data_dir"] , source_data["data_file"])

    split = params["prepare"]["split"]
    seed = params["prepare"]["seed"]
    random.seed(seed)

    artificats = config["artifacts"]
    prepare_data_dir_path = os.path.join(artificats["ARTIFACTS_DIR"] , artificats["PREPARED_DATA"])
    create_directories([prepare_data_dir_path])
    train_data_path = os.path.join(prepare_data_dir_path , artificats["TRAIN_DATA"])
    test_data_path =  os.path.join(prepare_data_dir_path , artificats["TEST_DATA"])
    
    encode = params["prepare"]["encode"]
    with open(input_data , encoding=encode) as fd_in:
        with open(train_data_path , "w" , encoding=encode) as fd_out_train:
            with open(test_data_path , "w" , encoding=encode) as fd_out_test:
                process_posts(fd_in , fd_out_train , fd_out_test , "<python>" , split)





if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="configs/config.yaml")
    args.add_argument("--params", "-p", default="params.yaml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        load_data(config_path=parsed_args.config, params_path=parsed_args.params)
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e