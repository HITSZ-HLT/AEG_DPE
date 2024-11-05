"Credit to GOT Paper https://arxiv.org/abs/2308.09687"
from examples.arg_writing.writing_llama2 import  (
    ArgWritingParser, 
    gotDPE,
    io, cot, tot)
from examples.arg_writing.prompt import ArgWritingPrompter_en,ArgWritingPrompter_zh
from planning_of_thoughts import controller, operations
from typing import Dict, List, Callable, Union
import csv
import datetime
import pandas as pd
import logging
import json
from tqdm import tqdm
from datasets import load_dataset,load_metric
import argparse
import os
import glob

def parse_dataset(dataset_name = str):
    """_summary_

    Args:
        dataset_name (_type_, optional): _description_. Defaults to str.
    Return:
        tran_file, dev_file, test_file
    """
    assert dataset_name in ["en_ArgEssay","zh_ArgEssay","en_NYT","zh_News"]
    if dataset_name in ["en_ArgEssay"]:
        return (f"data/{dataset_name}/ef_train.csv", f"data/{dataset_name}/ef_dev.csv", f"data/{dataset_name}/ef_test.csv"), "csv"
    elif dataset_name in ["zh_ArgEssay","en_NYT","zh_News"]:
        return (None, None, f"data/{dataset_name}/sample_test.json"), "json"
    else:
        raise NotImplementedError

def run(
    # data: List,
    methods: List[Callable[[], operations.GraphOfOperations]],
    budget: float,
    args
) -> float:
    """
    Controller function that executes each specified method for each specified
    sample while the budget is not exhausted.

    :param data_ids: Indices of the sample to be run.
    :type data_ids: List[int]
    :param methods: List of functions to generate Graphs of Operations.
    :type methods: Each function generates a Graph of Operation.
    :param budget: Language model budget for the execution in dollars.
    :type budget: float
    :param lm_name: Name of the language model to be used.
    :type lm_name: str
    :return: Spent budget in dollars.
    :rtype: float
    """
    lm_name = args.backend
    orig_budget = budget
    # checkpoint_id = 0
    # selected_data = data
    if args.resume_path is not None:
        folder_name = args.resume_path
        assert os.path.exists(folder_name)
        # get test_id check point
        file_saved = glob.glob(f"{folder_name}/*/*.json")
        # checkpoint_id = max([int(f.split('/')[-1].split(".")[0]) for f in file_saved])
    else:
        if not os.path.exists(args.output_dir):
            os.makedirs(args.output_dir)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        extra_info = f"{lm_name}_{'-'.join([method.__name__ for method in methods])}"
        folder_name =  os.path.join(args.output_dir,args.dataset_name,f"{extra_info}_{timestamp}") 
        os.makedirs(os.path.join(os.path.dirname(__file__), folder_name))
        for method in methods:
            os.makedirs(
                os.path.join(os.path.dirname(__file__), folder_name, method.__name__)
            )
    
    config = {
        "data": args.dataset_name,
        "methods": [method.__name__ for method in methods],
        "lm": lm_name,
        "budget": budget,
    }
    with open(
        os.path.join(os.path.dirname(__file__), folder_name, "config.json"), "w"
    ) as f:
        json.dump(config, f)
        
    # save model config
    with open(
        os.path.join(os.path.dirname(__file__), folder_name, "model_config.json"), "w"
    ) as f:
        model_config = json.load(open("planning_of_thoughts/controller/config.json",'r'))
        json.dump(model_config, f, indent=2)
    
    # save param config
    with open(
        os.path.join(os.path.dirname(__file__), folder_name, "param_config.json"), "w"
    ) as f:
        param_config = args.__dict__
        json.dump(param_config, f, indent=2)
        
    logging.basicConfig(
        filename=f"{folder_name}/log.log",
        filemode="w",
        format="%(name)s - %(levelname)s - %(message)s",
        level=logging.DEBUG,
        encoding='utf8'
    )


    data_files = {}    
    if args.dataset_name is not None:
        train_dev_test, extension = parse_dataset(args.dataset_name)
        _,_,data_files["test"] = train_dev_test
    else:
        if args.train_file is not None:
            data_files["train"] = args.train_file
            extension = args.train_file.split(".")[-1]
        if args.validation_file is not None:
            data_files["validation"] = args.validation_file
            extension = args.validation_file.split(".")[-1]
        if args.test_file is not None:
            data_files["test"] = args.test_file
            extension = args.test_file.split(".")[-1]

    raw_datasets = load_dataset(
        extension,
        data_files=data_files,
        cache_dir=args.cache_dir,
        use_auth_token=True ,
    )
    # only run on test
    selected_data = raw_datasets["test"][args.prompt_column][:args.max_predict_samples]
    if lm_name == "chatgpt":
        lm = controller.ChatGPT(
            "planning_of_thoughts/controller/config.json",
            model_name=lm_name,
            cache=True,
        )
    elif lm_name == "llama7b-hf":
        assert args.dataset_name.startswith("en")
        lm = controller.Llama2HF(
            "planning_of_thoughts/controller/config.json",
            model_name=lm_name,
            cache=True,
        )
    elif lm_name == "Baichuan2-7B":
        assert args.dataset_name.startswith("zh")
        lm = controller.Baichuan(
            "planning_of_thoughts/controller/config.json",
            model_name=lm_name,
            cache=True,
        )
    else:
        raise NotImplementedError

    if args.dataset_name.startswith("zh"):
        ArgWritingPrompter = ArgWritingPrompter_zh
    elif args.dataset_name.startswith("en"):
        ArgWritingPrompter = ArgWritingPrompter_en
    for id,data in tqdm(enumerate(selected_data),total=args.max_predict_samples):
        logging.info(f"Running data {data}")
        if budget <= 0.0:
            logging.error(
                f"Budget has been depleted, stopping. Data {data} has not been run."
            )
            break
        for method in methods:
            logging.info(f"Running method {method.__name__}")
            path = os.path.join(
                os.path.dirname(__file__),
                folder_name,
                method.__name__,
                f"{id}.json",
            )
            if os.path.exists(path):
                logging.info(f"SKIP  path exists: {path} ")
                continue
            
            logging.info(f"Budget left: {budget}")
            if budget <= 0.0:
                logging.error(
                    f"Budget has been depleted, stopping. Method {method.__name__} has not been run."
                )
                break

            operations_graph = method()
            if method.__name__ not in ['gotDPE',"gotDPE_wo_overriding_rebuttal"]:
                argument_relation_prompt = "Simple"
            else:
                argument_relation_prompt = args.argument_relation_prompt
            executor = controller.Controller(
                lm,
                operations_graph,
                ArgWritingPrompter(argument_relation_prompt=argument_relation_prompt,ablation_method=method.__name__ ),
                ArgWritingParser(),
                {
                    "original": data,
                    "current": "",
                    "phase": 0,
                    "method": method.__name__,
                    "type":"topicPrompt"
                },
            )
            retry_times = 3
            while retry_times:
                try:
                    executor.run()
                    break
                except Exception as e:
                    retry_times -=1
                    logging.error(f"Exception: {e}")
            if retry_times<0:
                raise e
            executor.output_graph(path)
            budget = orig_budget - lm.cost

    return orig_budget - lm.cost

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    
    args.add_argument('--backend',type=str,choices=['chatgpt','llama7b-hf','Baichuan2-7B'],default="chatgpt")
    args.add_argument('--method',type=str,choices=['gotDPE','tot','io','cot'],default="io")
    
    args.add_argument("--dataset_name",type=str,choices=["en_ArgEssay","zh_ArgEssay","en_NYT","zh_News"],default="en_NYT")
    args.add_argument("--output_dir",type=str,default="./results")
    
    args.add_argument("--prompt_column",type=str,default="instruction")
    args.add_argument("--response_column",type=str,default="article_content")
    
    args.add_argument("--train_file",type=str,default=None)
    args.add_argument("--validation_file",type=str,default=None)
    args.add_argument("--test_file",type=str,required=False,default="data/en_ArgEssay/ef_test.csv")
    args.add_argument("--overwrite_cache",type=bool,default=True)
    args.add_argument("--preprocessing_num_workers",type=int,default=4)
    
    args.add_argument("--max_train_sample",type=int,default=0)
    args.add_argument("--max_eval_samples",type=int,default=0)
    args.add_argument("--max_predict_samples",type=int,default=50)
    
    args.add_argument("--cache_dir",type=str,default="cache")
    
    args.add_argument("--resume_path",type=str,default=None)
    
    args.add_argument("--argument_relation_prompt",type=str,choices=["Simple","sLink","Component","Relation","CR"],default="CR")
    
    args = args.parse_args()

    

    approaches = {
        "gotDPE":[gotDPE],
        "tot":[tot],
        "cot":[cot],
        "io":[io],
        }
    approaches = [app for app in approaches[args.method] ]
    budget = 30
    spent = run( approaches, budget, args)
