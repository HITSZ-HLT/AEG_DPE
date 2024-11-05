# Copyright (c) 2023 ETH Zurich.
#                    All rights reserved.
#
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
#
# main author: Nils Blach;;

import os
import logging
import datetime
import json
import csv
from typing import Dict, List, Callable, Union
from planning_of_thoughts import controller, operations, prompter, parser
# from . import prompt
from . import utils
import re
# Education is expensive, but the consequences of a failure to educate, especially in an increasingly globalized world, are even more expensive. Do you agree or disagree? Use specific reasons and examples to support your answer. 




class ArgWritingParser(parser.Parser):

    def __init__(self) -> None:
        """
        Inits the response cache.
        """
        self.cache = {}

    def parse_aggregation_answer(
        self, states: List[Dict], texts: List[str], target_type:str
    ) -> Union[Dict, List[Dict]]:
        """
        Parse the response from the language model for an aggregation prompt.

        :param states: The thought states used to generate the prompt.
        :type states: List[Dict]
        :param texts: The responses to the prompt from the language model.
        :type texts: List[str]
        :return: The new thought states after parsing the respones from the language model.
        :rtype: Union[Dict, List[Dict]]
        :raise AssertionError: If not exactly two thought states are provided.
        """
        # aggregate into one thought
        base_state = {}
        for state in states:
            base_state = {**base_state, **state}
        new_states = []
        for text in texts:
            if state["method"].startswith("gotDPE"):
                # We expect a json which contains the four lists named "List 1" to "List 4"
                # cut everything until the opening bracket and everything after the closing bracket
                # if target_type == "essay":
                        value = text
                        logging.warning(
                            f"Prasing failed. Output directly"
                        )
                        new_state = state.copy()
                        # value = text.replace('\n','')
                        new_state["current"] = str(value.replace(' Ċ ','\n')).strip()
                        new_state["phase"] = 1
                        new_state["part"] = f"{target_type} {len(new_states)+1}"
                        new_state['type']=target_type
                        new_states.append(new_state)

        return new_states

    def parse_generate_answer(self, state: Dict, texts: List[str], target_type:str=None) -> List[Dict]:
        """
        Parse the response from the language model for a generate prompt.

        :param state: The thought state used to generate the prompt.
        :type state: Dict
        :param texts: The responses to the prompt from the language model.
        :type texts: List[str]
        :return: The new thought states after parsing the respones from the language model.
        :rtype: List[Dict]
        """
        new_states = []
        for text in texts:
            if state["method"].startswith("gotDPE"):
                assert target_type is not None
                # We expect a json which contains the four lists named "List 1" to "List 4"
                # cut everything until the opening bracket and everything after the closing bracket
                try:
                    parsed_text = text.replace('\n',' Ċ ').split('<sep>')
                    for i, value in enumerate(parsed_text):
                        if len(value)<5:
                            continue
                        new_state = state.copy()
                        new_state["current"] = str(value.replace(' Ċ ','\n')).strip()
                        new_state["phase"] = 1
                        new_state["part"] = f"{target_type} {len(new_states)+1}"
                        new_state['type']=target_type
                        new_states.append(new_state)
                except Exception as e:
                    logging.error(
                        f"Could not parse step answer: {text}. Encountered exception: {e}"
                    )
            elif state["method"].startswith('io') or state["method"].startswith('tot') or state["method"].startswith('cot'):
                    new_state = state.copy()
                    new_state["current"] = text.strip()
                    new_state["phase"] = 1
                    new_state['type']=target_type
                    new_states.append(new_state)
            else: # if tot cot io ?
                parsed_text = re.findall(r'<[a-zA-Z]+.*?>(.*?)</[a-zA-Z]+.*?>',text.replace('\n',' Ċ '))
                parsed_tag = [i[1:-1].lower() for i in re.findall(r'<[a-zA-Z]+.*?>',text)]
                for i, value in enumerate(parsed_text):
                    if target_type not in parsed_tag[i]:
                        logging.warning(
                            f"Expected key to contain '{target_type}', but found {parsed_tag[i]}."
                        )
                        continue
                    new_state = state.copy()
                    new_state["current"] = str(value.replace(' Ċ ','\n')).strip()
                    new_state["phase"] = 1
                    new_state['type']=target_type
                    new_states.append(new_state)
                if len(parsed_text)==0:
                    logging.warning(
                        f"Prasing failed. Output directly"
                    )
                    new_state = state.copy()
                    value = text.replace('\n',' Ċ ')
                    new_state["current"] = str(value.replace(' Ċ ','\n')).strip()
                    new_state["phase"] = 1
                    new_state['type']=target_type
                    new_states.append(new_state)
                if len(new_states)==0:
                    logging.warning(
                        f"Prasing failed. Output directly"
                    )
                    new_state = state.copy()
                    value = text.replace('\n',' Ċ ')
                    new_state["current"] = str(value.replace(' Ċ ','\n')).strip()
                    new_state["phase"] = 1
                    new_state['type']=target_type
                    new_states.append(new_state)
        return new_states

    def parse_improve_answer(self, states: Dict, texts: List[str], target_type:str) -> Dict:
        """
        Parse the response from the language model for an improve prompt.

        :param state: The thought state used to generate the prompt.
        :type state: Dict
        :param texts: The responses to the prompt from the language model.
        :type texts: List[str]
        :return: The new thought state after parsing the responses from the language model.
        :rtype: Dict
        """
        base_state = {}
        for state in states:
            base_state = {**base_state, **state}
        new_states = []
        for text in texts:
            if base_state["method"].startswith("gotDPE"):
                # We expect a json which contains the four lists named "List 1" to "List 4"
                # cut everything until the opening bracket and everything after the closing bracket
                try:
                    parsed_text = text.replace('\n',' Ċ ').split('<sep>')
                    for i, value in enumerate(parsed_text):
                        if len(value)<5:
                            continue
                        new_state = state.copy()
                        new_state["current"] = str(value.replace(' Ċ ','\n')).strip()
                        new_state["phase"] = 1
                        new_state["part"] = f"{target_type} {len(new_states)+1}"
                        new_state['type']=target_type
                        new_states.append(new_state)
                except Exception as e:
                    logging.error(
                        f"Could not parse step answer: {text}. Encountered exception: {e}"
                    )
        return new_states
    def parse_validation_answer(self, state: Dict, texts: List[str]) -> bool:
        """
        Parse the response from the language model for a validation prompt.

        :param state: The thought state used to generate the prompt.
        :type state: Dict
        :param texts: The responses to the prompt from the language model.
        :type texts: List[str]
        :return: Whether the thought state is valid or not.
        :rtype: bool
        """
        pass

    def parse_score_answer(self, states: List[Dict], texts: List[str]) -> List[float]:
        """
        Parse the response from the language model for a score prompt.

        :param states: The thought states used to generate the prompt.
        :type states: List[Dict]
        :param texts: The responses to the prompt from the language model.
        :type texts: List[str]
        :return: The scores for the thought states.
        :rtype: List[float]
        :raise AssertionError: If the number of thought states is not one.
        """
        assert len(states) == 1, "Only one state is allowed for scoring."
        if len(states) == 1:
            # individual scoring
            if states[0]['method'].startswith("gotDPE"):
                scores = []
                for text in texts:
                    try:
                        tag = "score"
                        res = re.findall(r'<{}>(.*?)</{}>'.format(tag,tag),text.replace('\n',' Ċ '))
                        if len(res) == 1:
                            scores.append(float(res[0].split('/')[0]))
                        elif len(res) > 1:
                            logging.warning(
                                f"Found multiple redundancy scores in answer: {text}. Returning the last one."
                            )
                            scores.append(float(res[-1].split('/')[0]))
                        else:
                            logging.warning(
                                f"Could not find any redundancy score in answer: {text}. Ignoring this answer."
                            )
                    except:
                        logging.warning("parsing text failed: {}".format(text)) 
                if len(scores) == 0 :
                    logging.warning(
                        f"Could not find any valid score in any answer. Returning 0.0."
                    )
                    return [0.0]
                mean_score = utils.fmean(scores) 
                return [mean_score]
            elif states[0]['method'].startswith("tot"):
                scores = []
                for text in texts:
                    try:
                        tag = "score"
                        res = re.findall(r'<{}>(.*?)</{}>'.format(tag,tag),text.replace('\n',' Ċ '))
                        if len(res) == 1:
                            scores.append(float(res[0].split('/')[0]))
                        elif len(res) > 1:
                            logging.warning(
                                f"Found multiple redundancy scores in answer: {text}. Returning the last one."
                            )
                            scores.append(float(res[-1].split('/')[0]))
                        else:
                            logging.warning(
                                f"Could not find any redundancy score in answer: {text}. Ignoring this answer."
                            )
                    except:
                        logging.warning("parsing text failed: {}".format(text)) 
                if len(scores) == 0 :
                    logging.warning(
                        f"Could not find any valid score in any answer. Returning 0.0."
                    )
                    return [0.0]
                mean_score = utils.fmean(scores) 
                return [mean_score]
                        
    def parse_integ_answer(self, states:List[Dict], texts: List[str]) -> List[float]:
        base_state = {}
        for state in states:
            base_state = {**base_state, **state}
        new_states = []
        for text in texts:
            if state["method"].startswith("gotDPE"):
                # We expect a json which contains the four lists named "List 1" to "List 4"
                # cut everything until the opening bracket and everything after the closing bracket
                try:
                    parsed_text = re.findall(r'<[a-zA-Z]+.*?>(.*?)</[a-zA-Z]+.*?>',text.replace('\n',' Ċ '))
                    parsed_tag = [i[1:-1].lower() for i in re.findall(r'<[a-zA-Z]+.*?>',text)]
                    thought_num = len(parsed_text)
                    for i, value in enumerate(parsed_text):
                        new_state = state.copy()
                        new_state["current"] = str(value.replace(' Ċ ','\n')).strip()
                        new_state["phase"] = 1
                        new_state["part"] = f"{parsed_tag[i]} {len(new_states)+1}"
                        new_state['type']=parsed_tag[i]
                        new_states.append(new_state)
                except Exception as e:
                    logging.error(
                        f"Could not parse step answer: {text}. Encountered exception: {e}"
                    )
                    new_states=states
        if len(new_states)==0:new_states=states
        return new_states

def cot() -> operations.GraphOfOperations:
    operations_graph = operations.GraphOfOperations()
    cot_essay = operations.HeterGenerate(1,1,target_type="essay")
    operations_graph.append_operation(cot_essay)
    return operations_graph

def tot() -> operations.GraphOfOperations:
    operations_graph = operations.GraphOfOperations()
    plan_depth = 1
    for _ in range(plan_depth):
    
        plan = operations.HeterGenerate(1,5,target_type="plan")
        operations_graph.append_operation(plan)
        # sore plan
        operations_graph.append_operation(operations.Score(1,False))
        # keep plan
        operations_graph.append_operation(operations.KeepBestN(1,True))
        
    # write
    tot_essay = operations.HeterGenerate(1,1,target_type="essay")
    operations_graph.append_operation(tot_essay)
    
    return operations_graph

def io() -> operations.GraphOfOperations:
    operations_graph = operations.GraphOfOperations()
    io_essay = operations.HeterGenerate(1, 1,target_type="essay")
    operations_graph.append_operation(io_essay)
    return operations_graph

def gotDPE2() -> operations.GraphOfOperations:
    claim_num = 3
    slot_update = 2
    
    operations_graph = operations.GraphOfOperations()
    
    major_claim = operations.HeterGenerate(1, 1, target_type="majorclaim")
    operations_graph.append_operation(major_claim)  # HeterGenerate the sublists
    claims = operations.HeterGenerate(claim_num, 1, target_type="claim")
    claims.add_predecessor(major_claim)
    operations_graph.add_operation(claims)
    
    refine_majorclaim = operations.Refine(target_type="majorclaim")
    
    
    conclusion_merge = operations.HeterAggregate(1,target_type = "conclusion")
    intro_merge = operations.HeterAggregate(1,target_type = "introduction")

    final_essay_merge = operations.Combine(1,target_type = "essay") # simple combine
    
    for i in range(1, claim_num+1):
        claim_id = f"claim {i}"
        claim_list = operations.Selector(
            selector = lambda thoughts, claim_id=claim_id: [
                thought for thought in thoughts if thought.state["part"] == claim_id
            ]
        )
        claim_list.add_predecessor(claims)
        operations_graph.add_operation(claim_list)
        
        slot_plan_init = operations.Integration(target_type = "slot")
        slot_plan_init.add_predecessor(claim_list)
        operations_graph.add_operation(slot_plan_init)
        
        for _ in range(slot_update):
            slot_plan = operations.Integration(target_type='slot')
            slot_plan.add_predecessor(slot_plan_init)
            operations_graph.add_operation(slot_plan)
            slot_plan_init = slot_plan
        
        claims_of_slot = operations.Selector(
            lambda thoughts:[
                thought for thought in thoughts if thought.state['type']=='claim'
            ]
        )
        claims_of_slot.add_predecessor(slot_plan)
        operations_graph.add_operation(claims_of_slot)
        
        refine_majorclaim.add_predecessor(claims_of_slot)
        conclusion_merge.add_predecessor(claims_of_slot)   

        paragraph_merge = operations.HeterAggregate(1,target_type = "paragraph")
        paragraph_merge.add_predecessor(slot_plan)
        operations_graph.add_operation(paragraph_merge)
        
        final_essay_merge.add_predecessor(paragraph_merge)
        
    operations_graph.add_operation(refine_majorclaim)
        
    conclusion_merge.add_predecessor(refine_majorclaim)
    operations_graph.add_operation(conclusion_merge)
    
        
    intro_merge.add_predecessor(refine_majorclaim)
    operations_graph.add_operation(intro_merge)

    final_essay_merge.add_predecessor(intro_merge)
    final_essay_merge.add_predecessor(conclusion_merge)
    operations_graph.add_operation(final_essay_merge)
    return operations_graph
       
       

def gotDPE(self_rebuttal_round=1,init_claim_num=3,final_claim_num = 3) -> operations.GraphOfOperations:
    """
    Generates the Graph of Operations for the gotDPE method.

    :return: Graph of Operations
    :rtype: GraphOfOperations
    """
    
    
    operations_graph = operations.GraphOfOperations()
    evidence_num = 1
    

    major_claim = operations.HeterGenerate(1, 1, target_type="majorclaim")
    operations_graph.append_operation(major_claim)  # HeterGenerate the sublists
    claims = operations.HeterGenerate(init_claim_num, 1, target_type="claim")
    # at least selection
    claims.add_predecessor(major_claim)
    operations_graph.add_operation(claims)
    refine_majorclaim = operations.Refine(target_type="majorclaim")
    
    
    conclusion_merge = operations.HeterAggregate(1,target_type = "conclusion")
    intro_merge = operations.HeterAggregate(1,target_type = "introduction")
    
    paragraph_ranked_merge = operations.FilterN(final_claim_num)# KeepBestN
    paragraph_ranking_merge = operations.FilterN(3) # Score
    
    final_essay_merge = operations.Combine(1,target_type = "essay") # simple combine
    for i in range(1, init_claim_num+1):
        claim_id = f"claim {i}"
        claim_list = operations.Selector(
            lambda thoughts, claim_id=claim_id: [
                thought for thought in thoughts if thought.state["part"] == claim_id
            ]
        )
        claim_list.add_predecessor(claims)
        operations_graph.add_operation(claim_list)
        
        for i in range(self_rebuttal_round):
            rebuttal_1 = operations.HeterGenerate(2,1,target_type="rebuttal")
            rebuttal_1.add_predecessor(claim_list)
            operations_graph.add_operation(rebuttal_1)
            # select one or not
            
            keep_best_rebuttal = operations.FilterN(1)
            keep_best_rebuttal.add_predecessor(rebuttal_1)
            operations_graph.add_operation(keep_best_rebuttal)

            
            improve_claim_from_rebuttal_1 = operations.Refine(target_type="claim")
            improve_claim_from_rebuttal_1.add_predecessor([keep_best_rebuttal,claim_list])
            operations_graph.add_operation(improve_claim_from_rebuttal_1)
            claim_list = improve_claim_from_rebuttal_1
            
        # value claim
            
        rebuttal_2  = operations.HeterGenerate(1,1,target_type="rebuttal")
        rebuttal_2.add_predecessor(improve_claim_from_rebuttal_1)
        operations_graph.add_operation(rebuttal_2)
        
        
        keep_best_rebuttal = operations.FilterN(1)
        keep_best_rebuttal.add_predecessor(rebuttal_2)
        operations_graph.add_operation(keep_best_rebuttal)
        
        counter_rebuttal = operations.HeterAggregate(2,target_type='counter_rebuttal')
        counter_rebuttal.add_predecessor([keep_best_rebuttal,improve_claim_from_rebuttal_1])
        operations_graph.add_operation(counter_rebuttal)
        
        keep_best_counter_rebuttal = operations.FilterN(1)
        keep_best_counter_rebuttal.add_predecessor(counter_rebuttal)
        operations_graph.add_operation(keep_best_counter_rebuttal)
        
        evidence = operations.HeterGenerate(evidence_num,1,target_type = 'evidence')
        evidence.add_predecessor(improve_claim_from_rebuttal_1)
        operations_graph.add_operation(evidence)
        
        paragraph_merge = operations.HeterAggregate(1,target_type = "paragraph")
        paragraph_merge.add_predecessor([improve_claim_from_rebuttal_1,evidence,keep_best_rebuttal,keep_best_counter_rebuttal])
        operations_graph.add_operation(paragraph_merge)
        
        paragraph_ranking_merge.add_predecessor(paragraph_merge)
        
        
        
        refine_majorclaim.add_predecessor(improve_claim_from_rebuttal_1)
        conclusion_merge.add_predecessor(improve_claim_from_rebuttal_1)
        
        # final_essay_merge.add_predecessor(paragraph_merge)
    
    
    operations_graph.add_operation(paragraph_ranking_merge)
    
    paragraph_ranked_merge.add_predecessor(paragraph_ranking_merge)    
    operations_graph.add_operation(paragraph_ranked_merge)
    
    final_essay_merge.add_predecessor(paragraph_ranked_merge)
        
    operations_graph.add_operation(refine_majorclaim)
    
    intro_merge.add_predecessor(refine_majorclaim)
    operations_graph.add_operation(intro_merge)
    
    conclusion_merge.add_predecessor(refine_majorclaim)
    operations_graph.add_operation(conclusion_merge)
        
    final_essay_merge.add_predecessor(intro_merge)
    final_essay_merge.add_predecessor(conclusion_merge)
    operations_graph.add_operation(final_essay_merge)
        
    return operations_graph 

def gotDPE_wo_dia_planning(self_rebuttal_round=1,init_claim_num=3,final_claim_num = 3) -> operations.GraphOfOperations:
    """
    Generates the Graph of Operations for the gotDPE method.

    :return: Graph of Operations
    :rtype: GraphOfOperations
    """
    
    # self rebuttal 可以是rebuttal多轮
    # 也可以是多个rebuttal取其1
    
    # self_rebuttal_round = 2
    # init_claim_num = 3
    # final_claim_num = 3
    operations_graph = operations.GraphOfOperations()
    evidence_num = 1

    major_claim = operations.HeterGenerate(1, 1, target_type="majorclaim")
    operations_graph.append_operation(major_claim)  # HeterGenerate the sublists
    claims = operations.HeterGenerate(init_claim_num, 1, target_type="claim")
    # at least selection
    claims.add_predecessor(major_claim)
    operations_graph.add_operation(claims)
    refine_majorclaim = operations.Refine(target_type="majorclaim")
    
    
    conclusion_merge = operations.HeterAggregate(1,target_type = "conclusion")
    intro_merge = operations.HeterAggregate(1,target_type = "introduction")
    
    paragraph_ranked_merge = operations.FilterN(final_claim_num)# KeepBestN
    paragraph_ranking_merge = operations.FilterN(3) # Score
    
    final_essay_merge = operations.Combine(1,target_type = "essay") # simple combine
    for i in range(1, init_claim_num+1):
        claim_id = f"claim {i}"
        claim_list = operations.Selector(
            lambda thoughts, claim_id=claim_id: [
                thought for thought in thoughts if thought.state["part"] == claim_id
            ]
        )
        claim_list.add_predecessor(claims)
        operations_graph.add_operation(claim_list)
        improve_claim_from_rebuttal_1 = claim_list
       
        
        paragraph_merge = operations.HeterAggregate(1,target_type = "paragraph")
        paragraph_merge.add_predecessor([improve_claim_from_rebuttal_1])
        operations_graph.add_operation(paragraph_merge)
        
        paragraph_ranking_merge.add_predecessor(paragraph_merge)
        
        
        
        refine_majorclaim.add_predecessor(improve_claim_from_rebuttal_1)
        conclusion_merge.add_predecessor(improve_claim_from_rebuttal_1)
        
        # final_essay_merge.add_predecessor(paragraph_merge)
    
    
    operations_graph.add_operation(paragraph_ranking_merge)
    
    paragraph_ranked_merge.add_predecessor(paragraph_ranking_merge)    
    operations_graph.add_operation(paragraph_ranked_merge)
    
    final_essay_merge.add_predecessor(paragraph_ranked_merge)
        
    operations_graph.add_operation(refine_majorclaim)
    
    intro_merge.add_predecessor(refine_majorclaim)
    operations_graph.add_operation(intro_merge)
    
    conclusion_merge.add_predecessor(refine_majorclaim)
    operations_graph.add_operation(conclusion_merge)
        
    final_essay_merge.add_predecessor(intro_merge)
    final_essay_merge.add_predecessor(conclusion_merge)
    operations_graph.add_operation(final_essay_merge)
        
    return operations_graph



def gotDPE_wo_undercutting_rebuttal(self_rebuttal_round=1,init_claim_num=3,final_claim_num = 3) -> operations.GraphOfOperations:
    """
    Generates the Graph of Operations for the gotDPE method.

    :return: Graph of Operations
    :rtype: GraphOfOperations
    """
    
    operations_graph = operations.GraphOfOperations()
    evidence_num = 1

    major_claim = operations.HeterGenerate(1, 1, target_type="majorclaim")
    operations_graph.append_operation(major_claim)  # HeterGenerate the sublists
    claims = operations.HeterGenerate(init_claim_num, 1, target_type="claim")
    # at least selection
    claims.add_predecessor(major_claim)
    operations_graph.add_operation(claims)
    refine_majorclaim = operations.Refine(target_type="majorclaim")
    
    
    conclusion_merge = operations.HeterAggregate(1,target_type = "conclusion")
    intro_merge = operations.HeterAggregate(1,target_type = "introduction")
    
    paragraph_ranked_merge = operations.FilterN(final_claim_num)# KeepBestN
    paragraph_ranking_merge = operations.FilterN(3) # Score
    
    final_essay_merge = operations.Combine(1,target_type = "essay") # simple combine
    for i in range(1, init_claim_num+1):
        claim_id = f"claim {i}"
        claim_list = operations.Selector(
            lambda thoughts, claim_id=claim_id: [
                thought for thought in thoughts if thought.state["part"] == claim_id
            ]
        )
        claim_list.add_predecessor(claims)
        operations_graph.add_operation(claim_list)
        improve_claim_from_rebuttal_1 = claim_list
        for i in range(self_rebuttal_round):
            rebuttal_1 = operations.HeterGenerate(2,1,target_type="rebuttal")
            rebuttal_1.add_predecessor(claim_list)
            operations_graph.add_operation(rebuttal_1)
            # select one or not
            
            keep_best_rebuttal = operations.FilterN(1)
            keep_best_rebuttal.add_predecessor(rebuttal_1)
            operations_graph.add_operation(keep_best_rebuttal)

            
            improve_claim_from_rebuttal_1 = operations.Refine(target_type="claim")
            improve_claim_from_rebuttal_1.add_predecessor([keep_best_rebuttal,claim_list])
            operations_graph.add_operation(improve_claim_from_rebuttal_1)
            claim_list = improve_claim_from_rebuttal_1
            
        # value claim
            
        
        evidence = operations.HeterGenerate(evidence_num,1,target_type = 'evidence')
        evidence.add_predecessor(improve_claim_from_rebuttal_1)
        operations_graph.add_operation(evidence)
        
        evidence_keep = operations.FilterN(evidence_num)
        evidence_keep.add_predecessor(evidence)
        operations_graph.add_operation(evidence_keep)
        evidence = evidence_keep
        
        paragraph_merge = operations.HeterAggregate(1,target_type = "paragraph")
        paragraph_merge.add_predecessor([improve_claim_from_rebuttal_1,evidence])
        operations_graph.add_operation(paragraph_merge)
        
        paragraph_ranking_merge.add_predecessor(paragraph_merge)
        
        
        
        refine_majorclaim.add_predecessor(improve_claim_from_rebuttal_1)
        conclusion_merge.add_predecessor(improve_claim_from_rebuttal_1)
        
        # final_essay_merge.add_predecessor(paragraph_merge)
    
    
    operations_graph.add_operation(paragraph_ranking_merge)
    
    paragraph_ranked_merge.add_predecessor(paragraph_ranking_merge)    
    operations_graph.add_operation(paragraph_ranked_merge)
    
    final_essay_merge.add_predecessor(paragraph_ranked_merge)
        
    operations_graph.add_operation(refine_majorclaim)
    
    intro_merge.add_predecessor(refine_majorclaim)
    operations_graph.add_operation(intro_merge)
    
    conclusion_merge.add_predecessor(refine_majorclaim)
    operations_graph.add_operation(conclusion_merge)
        
    final_essay_merge.add_predecessor(intro_merge)
    final_essay_merge.add_predecessor(conclusion_merge)
    operations_graph.add_operation(final_essay_merge)
        
    return operations_graph


def gotDPE_wo_overriding_rebuttal(self_rebuttal_round=1,init_claim_num=3,final_claim_num = 3) -> operations.GraphOfOperations:
    """
    Generates the Graph of Operations for the gotDPE method.

    :return: Graph of Operations
    :rtype: GraphOfOperations
    """
    
    
    # self_rebuttal_round = 2
    # init_claim_num = 3
    # final_claim_num = 3
    self_rebuttal_round = 0
    operations_graph = operations.GraphOfOperations()
    evidence_num = 1

    major_claim = operations.HeterGenerate(1, 1, target_type="majorclaim")
    operations_graph.append_operation(major_claim)  # HeterGenerate the sublists
    claims = operations.HeterGenerate(init_claim_num, 1, target_type="claim")
    # at least selection
    claims.add_predecessor(major_claim)
    operations_graph.add_operation(claims)
    refine_majorclaim = operations.Refine(target_type="majorclaim")
    
    
    conclusion_merge = operations.HeterAggregate(1,target_type = "conclusion")
    intro_merge = operations.HeterAggregate(1,target_type = "introduction")
    
    paragraph_ranked_merge = operations.FilterN(final_claim_num)# KeepBestN
    paragraph_ranking_merge = operations.FilterN(3) # Score
    
    final_essay_merge = operations.Combine(1,target_type = "essay") # simple combine
    for i in range(1, init_claim_num+1):
        claim_id = f"claim {i}"
        claim_list = operations.Selector(
            lambda thoughts, claim_id=claim_id: [
                thought for thought in thoughts if thought.state["part"] == claim_id
            ]
        )
        claim_list.add_predecessor(claims)
        operations_graph.add_operation(claim_list)
        improve_claim_from_rebuttal_1 = claim_list
        for i in range(self_rebuttal_round):
            rebuttal_1 = operations.HeterGenerate(2,1,target_type="rebuttal")
            rebuttal_1.add_predecessor(claim_list)
            operations_graph.add_operation(rebuttal_1)
            # select one or not
            
            keep_best_rebuttal = operations.FilterN(1)
            keep_best_rebuttal.add_predecessor(rebuttal_1)
            operations_graph.add_operation(keep_best_rebuttal)

            
            improve_claim_from_rebuttal_1 = operations.Refine(target_type="claim")
            improve_claim_from_rebuttal_1.add_predecessor([keep_best_rebuttal,claim_list])
            operations_graph.add_operation(improve_claim_from_rebuttal_1)
            claim_list = improve_claim_from_rebuttal_1
            
        # value claim
            
        rebuttal_2  = operations.HeterGenerate(1,1,target_type="rebuttal")
        rebuttal_2.add_predecessor(improve_claim_from_rebuttal_1)
        operations_graph.add_operation(rebuttal_2)
        
        
        keep_best_rebuttal = operations.FilterN(1)
        keep_best_rebuttal.add_predecessor(rebuttal_2)
        operations_graph.add_operation(keep_best_rebuttal)
        
        counter_rebuttal = operations.HeterAggregate(2,target_type='counter_rebuttal')
        counter_rebuttal.add_predecessor([keep_best_rebuttal,improve_claim_from_rebuttal_1])
        operations_graph.add_operation(counter_rebuttal)
        
        keep_best_counter_rebuttal = operations.FilterN(1)
        keep_best_counter_rebuttal.add_predecessor(counter_rebuttal)
        operations_graph.add_operation(keep_best_counter_rebuttal)
        
        evidence = operations.HeterGenerate(evidence_num,1,target_type = 'evidence')
        evidence.add_predecessor(improve_claim_from_rebuttal_1)
        operations_graph.add_operation(evidence)
        
        evidence_keep = operations.FilterN(evidence_num)
        evidence_keep.add_predecessor(evidence)
        operations_graph.add_operation(evidence_keep)
        evidence = evidence_keep
        
        paragraph_merge = operations.HeterAggregate(1,target_type = "paragraph")
        paragraph_merge.add_predecessor([improve_claim_from_rebuttal_1,evidence,keep_best_rebuttal,keep_best_counter_rebuttal])
        operations_graph.add_operation(paragraph_merge)
        
        paragraph_ranking_merge.add_predecessor(paragraph_merge)
        
        
        
        refine_majorclaim.add_predecessor(improve_claim_from_rebuttal_1)
        conclusion_merge.add_predecessor(improve_claim_from_rebuttal_1)
        
        # final_essay_merge.add_predecessor(paragraph_merge)
    
    
    operations_graph.add_operation(paragraph_ranking_merge)
    
    paragraph_ranked_merge.add_predecessor(paragraph_ranking_merge)    
    operations_graph.add_operation(paragraph_ranked_merge)
    
    final_essay_merge.add_predecessor(paragraph_ranked_merge)
        
    operations_graph.add_operation(refine_majorclaim)
    
    intro_merge.add_predecessor(refine_majorclaim)
    operations_graph.add_operation(intro_merge)
    
    conclusion_merge.add_predecessor(refine_majorclaim)
    operations_graph.add_operation(conclusion_merge)
        
    final_essay_merge.add_predecessor(intro_merge)
    final_essay_merge.add_predecessor(conclusion_merge)
    operations_graph.add_operation(final_essay_merge)
        
    return operations_graph




if __name__ == "__main__":
    """
    Input (x)   : an unordered list of 32 numbers between 0 and 9 (inclusive)
    Output (y)  : a sorted list of 32 numbers between 0 and 9 (inclusive)
    Correct     : y == sorted(x)
    Input Example:
        [0, 1, 9, 4, 2, 2, 0, 5, 1...]
    Output Example:
        [0, 0, 0, 0, 1, 1, 1, 1, 2...]
    """
    budget = 30
    samples = [item for item in range(0, 100)]
    approaches = [
        # io, cot, tot, tot2, 
        gotDPE]


    # logging.info(f"Spent {spent} out of {budget} budget.")
