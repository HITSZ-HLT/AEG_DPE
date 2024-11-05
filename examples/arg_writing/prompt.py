from planning_of_thoughts import controller, operations, prompter, parser
from typing import Dict, List, Callable, Union



class ArgWritingPrompter_en(prompter.Prompter):


    slot_plan_update_prompt="""
    Here is the input claim: <claim> {claim} </claim>
    Here is the input evidence: <evidence> {evidence} </evidence>
    Here is the input rebuttal: <rebuttal> {rebuttal} </rebuttal>
    Here is the input counter-rebuttal: <counter_rebuttal> {counter_rebuttal} </counter_rebuttal>
    <Instruction>
    Approaches:
    1. Evidence should be reasons or examples to defend the claim. Revise the evidence sentences bentween tags <evidence> and </evidence> .
    2. Rebuttal directly addresses the opposing view and refutes the claim convincingly. Revise the rebuttal sentences articulated logically and clearly between tags <rebuttal> and </rebuttal>. 
    3. Counter-rebuttal should further defend your claim considering the rebuttal. Revise the counter-rebuttal sentences articulated logically and clearly between tags <counter_rebuttal> and </counter_rebuttal> .
    4. Review the claim and rebuttal sentences. Please comprehend why the claim is being argued. Revise the claim sentences between tags <claim> and </claim> .
    
    Please carefully follow the approaches and input sentences. Only output the revised sentences with their corresponding tags respectively.
    </Instruction>
    """
        
    # 1
    init_majorclaim_prompt = """
    Writing prompt: {input}
    <Instruction> Write a concise, contentious, and coherent Thesis Statement (major claim) given the writing prompt. </Instruction>
    """
    
    # 2 
    # input=major claim
    claim_prompt="""
    Major Claim: {input}
    <Instruction> To support the major claim, please further derive {num_branches} effective claims in one sentence. Think about the claims from different perspectives. Please Note that each claim must end with token <sep>. </Instruction>
    """

    # 3 
    # input = claim
    rebuttal_prompt = """
    Claim: {input}
    <Instruction> Evaluate the claim and refute it. Only output {num_branches} pieces of rebuttal. Please Note that each rebuttal must end with speical token <sep>. </Instruction>
    """
    
    # 4 
    improve_claim_from_rebuttal_prompt = """
    Claim: {claim}
    Rebuttal: {rebuttal}
    <Instruction> Improve the above claim considering the weakness that the rebuttal points out. Directly output an improved claim in one sentence without any supporting evidence or acknowledging the weakness again. </Instruction>
    """   
    
    
    # 5
    counter_rebuttal_prompt = """
    Claim: {claim}
    Rebuttal: {rebuttal}    
    <Instruction> Carefully review the claim and rebuttal. Please write a brief and persuasive counter-rebuttal to defend your claim or give solutions. Only output the counter-rebuttal . </Instruction>
    """
    
    # 6
    # input=claim
    evidence_prompt = """
    Claim: {input}    
    <Instruction> To support the claim, please think of {num_branches} evidence of real-life examples, fact, statistics, etc. Please Note that each evidence must end with speical token <sep>. </Instruction>
    """
    
    # 7
    # input = evidence
    more_evidence_prompt="""
    Evidence: {input}    
    <Instruction> Please provide more sub-evidence to support the given evidence. Only output sub-evidence between <sub-evidence> and </sub-evidence>. If no more sub-evidence can sufficiently support the evidence output <NONE> between. </Instruction>
    """

    # 8
    improve_final_majorclaim_prompt="""
    Writing prompt: {input}
    Claims: {claim}    
    <Instruction> Write a concise, contentious, and coherent Thesis Statement (major claim) given the writing prompt. The thesis statement should cover the main points of the listed claims. Only output the statement. </Instruction>
    """
    
    # 1
    body_para_prompt="""
    Claim: {claim}\n
    <Hints>
    Evidence: {evidence}\n
    Rebuttal: {rebuttal}\n
    Counter_rebuttal: {counter_rebuttal}\n
    </Hints>
    <Instruction> {argument_relation_prompt} Consider and summarize the main points of the Hints. Write a coherent and persuasive body paragraph in favor of the claim. Only output the paragraph. </Instruction> 
    """
    
    body_para_prompt_wo_dia_planning="""
    Claim: {claim}\n

    <Instruction>  Write a coherent and persuasive body paragraph in favor of the claim. Only output the paragraph. </Instruction> 
    """
    
    body_para_prompt_wo_undercutting_rebuttal="""
    Claim: {claim}\n
    <Hints>
    Evidence: {evidence}
    </Hints>
    <Instruction> You are provided with the above hints. Write a coherent and persuasive body paragraph in favor of the claim. Only output the paragraph. </Instruction> 
    """
    

    argument_relation_prompt = {
        "Simple":"You are provided with the above hints.",
        "sLink":"Evidence is important to support Claim. Rebuttal and Counter_rebuttal are optional.",
        "Component":"The primary incorporation of claim and evidence coupled with the complementary integration of rebuttal and counter-rebuttal determine the quality of the argument.",
        # "Hard_Relation":"Component Relation: Evidence supports Claim; Rebuttal attacks Claim; Counter_rebuttal attacks Rebuttal but supports Claim.",
        "Relation":"Evidence is important to support Claim. You should adequately rebut and address the rebuttal according to Counter_rebuttal to further support the claim.",
        "CR":"The primary incorporation of claim and evidence coupled with the complementary integration of rebuttal and counter-rebuttal determine the quality of the argument. Evidence is important to support Claim. You should adequately rebut and address the rebuttal according to Counter_rebuttal to further support the claim.",
    }
    
    # 2
    intro_para_prompt = """
    Writing prompt: {input}
    Major claim: {majorclaim}    
    <Instruction> Write an introduction of an argumentative essay given a writing prompt. The introduction should clearly state the major claim. Only output a concise introduction. </Instruction>
    """
    
    # 3
    conclusion_para_prompt = """
    Claims: {claim}    
    <Instruction> Write a conclusion of an argumentative essay referring to the claims above. Only output a concise conclusion . </Instruction>
    """
    
    essay_fianl_prompt = """
    Writing prompt: {input}\n
    Introduction: {introduction} \n
    Paragraphs: {paragraph} \n
    Conclusion: {conclusion} \n
    <Instruction> Read the above essay planning for the writing prompt. You should combine introduction, paragraphs and conclusion, and then organize your language. Output a coherent and persuasive argumentative essay. </Instruction>
    """
    
    io_prompt = """
    Prompt: {input}
    <Instruction> Write an argumentative essay according to above prompt. Only output an essay between the tags <essay> and </essay> </Instruction>
    """

    score_paragraph_prompt="""
    Here is an argumentative body paragraph: {paragraph}
    

    A score of 100 for evidence abundance implies that the provided evidence sufficiently supports the claim, while a score of 0 implies that there is no valid evidence. The final score for evidence abundance should be between <Evidence> and </Evidence>
    A score of 100 for insight implies that the essay is thoughtful with valuable insight, while a score of 0 implies that the essay is too naive or one-sided. The final score for insight of essay should be between <Insight> and </Insight>.
    A score of 100 for persuasiveness implies that the paragraph is convincing with coherent logical flow, while a score of 0 implies that the paragraph is illogical and self-contradictory. The final score for persuasiveness should be between <Persuade> and </Persuade>. 
    <Instruction> Provide reasoning for your scoring and place the score numbers between corresponding tags without any additional text. </Instruction>
    """
    
    score_claim_prompt="""
    Writing prompt: {input}
    Claim: {claim}
    
    Analyze the quality of the claim. Score it from 0 to 10, where score 10 means the claim is in-depth, critical, and highly related to the prompt. Output Your integer score without any additional text between the tags <score> and </score>.
    """
    #     <reasoning>Your reasons here<reasoning>
    # <score>Your integer score here without any additional text<score>
    cot_prompt="""
    Here is the writing prompt: {input}
    
    Write an argumentative essay following the writing prompt.
    
    Make a brief plan then write. Your output should be in the following format:
    
    <plan>Your plan here</plan>
    
    <essay>Your essay here</essay>
    """
    
    tot_plan_prompt="""
    Writing prompt: {input}
    Original wiriting plan :{plan}
    
    Make or improve the original plan for writing an argumentative essay. Your output should be in the following format:
    
    <plan>Your plan here</plan>
    """
    
    tot_essay_prompt="""
    Writing prompt: {input}
    Writing plan: {plan}
    
    Write a choerent and persuasive argumentative essay following the writing prompt. You should produce the essay based on the plan.
    Your output should be in the following format:
    
    <essay>Your essay here</essay>
    """
    
    tot_score_prompt="""
    Here is the writing plan: {plan}
    
    Analyze the quality of the writing plan for argumentative essay. Score it from 0 to 10, where socre 10 means the plan is coherent and logical. 
    Provide reasoning for your scoring and place the score numbers between tags <score> and </score>
    """

    generate_prompt_selector = {
        "majorclaim":init_majorclaim_prompt,
        "claim":claim_prompt,
        "rebuttal":rebuttal_prompt,
        "evidence":evidence_prompt,
        
        # "cot_prompt":cot_prompt,
        # "tot_plan_prompt":tot_plan_prompt,
        # "tot_essay_prompt":tot_essay_prompt
        # "io_prompt": io_prompt 
    }
    
    aggregate_prompt_selector = {
        "counter_rebuttal":counter_rebuttal_prompt,
        "conclusion":conclusion_para_prompt,
        "introduction":intro_para_prompt,
        "paragraph":body_para_prompt,
        "essay":essay_fianl_prompt,
        "slot":slot_plan_update_prompt
    }
    
    refine_prompt_selector = {
        "claim":improve_claim_from_rebuttal_prompt,
        "majorclaim":improve_final_majorclaim_prompt,
    }
    
    integ_prompt_selector = {
        "slot":slot_plan_update_prompt
    }
    
    score_prompt_selector = {
        "paragraph":score_paragraph_prompt,
        "claim":score_claim_prompt,
    }
    
    def __init__(self, argument_relation_prompt="",ablation_method = "") -> None:
        self.body_para_prompt = self.body_para_prompt.format(claim="{claim}",evidence="{evidence}",rebuttal="{rebuttal}",counter_rebuttal="{counter_rebuttal}",argument_relation_prompt=self.argument_relation_prompt[argument_relation_prompt])
        if ablation_method == "gotDPE_wo_dia_planning":
            self.body_para_prompt = self.body_para_prompt_wo_dia_planning
        elif ablation_method == "gotDPE_wo_undercutting_rebuttal":
            self.body_para_prompt = self.body_para_prompt_wo_undercutting_rebuttal
        self.aggregate_prompt_selector["paragraph"]=self.body_para_prompt
        super().__init__()
        

    def aggregation_prompt(self, state_dicts: List[Dict], target_type:str, **kwargs) -> str:
        """
        Generate an aggregation prompt for the language model.

        :param state_dicts: The thought states that should be aggregated.
        :type state_dicts: List[Dict]
        :param kwargs: Additional keyword arguments.
        :return: The aggregation prompt.
        :rtype: str
        :raise AssertionError: If not exactly two thought states are provided.
        """
        # pack state_dicts
        merge_dict = {
            "input":[],
            "claim":[],
            "evidence":[],
            "rebuttal":[],
            "counter_rebuttal":[],
            "majorclaim":[],
            "introduction":[],
            "conclusion":[],
            "paragraph":[],
            }
        merge_dict['input']=[state_dicts[0]['original']]
        for state in state_dicts:
            type_ = state['type']
            if type_ not in merge_dict:
                raise TypeError("please predefine a key {} in the template".format(type_))
            else:
                merge_dict[type_].append(state['current'])
        for key,value in merge_dict.items():
            
            value_ = ["{}".format(v) for v in value]
            if key == "paragraph":
                merge_dict[key]='\n'.join(value_)
            else:
                merge_dict[key]='<sep>'.join(value_)
            
        prompt =  self.aggregate_prompt_selector[target_type].format(**merge_dict)
        return prompt

    
    def generate_prompt(self, num_branches: int, original: str, current: str, method: str, target_type:str=None, **kwargs) -> str:
        """
        Generate a generate prompt for the language model.

        :param num_branches: The number of responses the prompt should ask the LM to generate.
        :type num_branches: int
        :param original: Input list of numbers.
        :type original: str
        :param current: Intermediate solution.
        :type current: str
        :param method: Method for which the generate prompt is generated.
        :type method: str
        :param kwargs: Additional keyword arguments.
        :return: The generate prompt.
        :rtype: str
        :raise AssertionError: If the requested number of branches is not one.
        """
        # pack state_dicts
        kwargs["num_branches"]=num_branches
        if current is None or current == "":
            kwargs['input']=original
        else:
            kwargs['input']=current
        if method.startswith("io"):
            return self.io_prompt.format(**kwargs)
        elif method.startswith("cot"):
            prompt = self.cot_prompt.format(**kwargs)
            return prompt
        elif method.startswith("tot"):
            # parm: plan w_prompt
            if target_type == "plan":
                kwargs['plan']=None
                prompt = self.tot_plan_prompt.format(**kwargs)
            elif target_type == "essay":
                kwargs['input']=original
                kwargs['plan']=current
                prompt = self.tot_essay_prompt.format(**kwargs)
            return prompt
        elif method.startswith("gotDPE"):
            prompt = self.generate_prompt_selector[target_type].format(**kwargs)
            return prompt
        return 
    
    def improve_prompt(self, state_dicts: List[Dict], target_type:str, **kwargs) -> str:
        """
        Generate an improve prompt for the language model.

        :param kwargs: Additional keyword arguments.
        :return: The improve prompt.
        :rtype: str
        """
        # pack state_dicts
        merge_dict = {
            "input":[],
            "claim":[],
            "rebuttal":[],
        }
        for state in state_dicts:
            type_ = state['type']
            if type_ not in merge_dict:
                merge_dict[type_] = [state['current']]
            else:
                merge_dict[type_].append(state['current'])
        for key,value in merge_dict.items():
            value_ = ["<{}>{}</{}>".format(key,v,key) for v in value]
            merge_dict[key]=' '.join(value_)
        if target_type == "majorclaim":
            merge_dict['input']=state['original']
        prompt =  self.refine_prompt_selector[target_type].format(**merge_dict)
        return prompt
    
    def integ_prompt(self, state_dicts: List[Dict], target_type:str, **kwargs) -> str:
            # pack state_dicts
        merge_dict = {"claim":[],"evidence":[],"rebuttal":[],"counter_rebuttal":[]}
        for state in state_dicts:
            type_ = state['type']
            if type_ not in merge_dict:
                merge_dict[type_] = [state['current']]
            else:
                merge_dict[type_].append(state['current'])
        for key,value in merge_dict.items():
            value_ = ["{}".format(v) for v in value]
            merge_dict[key]=' '.join(value_)

        prompt =  self.integ_prompt_selector[target_type].format(**merge_dict)
        return prompt

    def validation_prompt(self, **kwargs) -> str:
        """
        Generate a validation prompt for the language model.

        :param kwargs: Additional keyword arguments.
        :return: The validation prompt.
        :rtype: str
        """
        pass

    def score_prompt(self, state_dicts: List[Dict], **kwargs) -> str:
        """
        Generate a score prompt for the language model.

        :param state_dicts: The thought states that should be scored,
                            if more than one, they should be scored together.
        :type state_dicts: List[Dict]
        :param kwargs: Additional keyword arguments.
        :return: The score prompt.
        :rtype: str
        """
        # pack state_dicts
        merge_dict = {
            "paragraph":[],
            "plan":[],
            "claim":[],
            "input":[]
            }
        type_consist_ensure = []
        for state in state_dicts:
            merge_dict['input'] = [state["original"]]
            method = state['method']
            type_ = state['type']
            type_consist_ensure.append(type_)
            if type_ not in merge_dict:
                raise TypeError("please predefine a key {} in the template".format(type_))
            else:
                merge_dict[type_].append(state['current'])
        for key,value in merge_dict.items():
            value_ = ["{}".format(v) for v in value]
            merge_dict[key]=' '.join(value_)
        assert len(set(type_consist_ensure)) == 1
        target_type = type_consist_ensure[0]
        merge_dict['method']=method
        if merge_dict['method'].startswith("gotDPE"):
            prompt =  self.score_prompt_selector[target_type].format(**merge_dict)
        elif merge_dict['method'].startswith("tot"):
            prompt =  self.tot_score_prompt.format(**merge_dict)
        return prompt


class ArgWritingPrompter_zh(prompter.Prompter):

    
    slot_plan_update_prompt="""
    Claim: <claim> {claim} </claim>
    Evidence: <evidence> {evidence} </evidence>
    Rebuttal: <rebuttal> {rebuttal} </rebuttal>
    Counter-rebuttal: <counter_rebuttal> {counter_rebuttal} </counter_rebuttal>
    <Instruction>
    Approaches:
    1. Evidence should be reasons or examples to defend the claim. Revise the evidence sentences bentween tags <evidence> and </evidence> .
    2. Rebuttal directly addresses the opposing view and refutes the claim convincingly. Revise the rebuttal sentences articulated logically and clearly between tags <rebuttal> and </rebuttal>. 
    3. Counter-rebuttal should further defend your claim considering the rebuttal. Revise the counter-rebuttal sentences articulated logically and clearly between tags <counter_rebuttal> and </counter_rebuttal> .
    4. Review the claim and rebuttal sentences. Please comprehend why the claim is being argued. Revise the claim sentences between tags <claim> and </claim> .
    
    Please carefully follow the approaches and input sentences. Only output the revised sentences with their corresponding tags respectively.
    </Instruction>
    """
        
    # 1
    init_majorclaim_prompt = """
    写作要求：{input}
    【要求】：根据写作要求，写一句议论性的、连贯的论文主旨（中心论点）。
    """
    
    # 2 
    # input=major claim
    claim_prompt="""
    中心论点：{input}
    【要求】：为了支持中心论点，请进一步推导出{num_branches}句简明有效的子论点句子。从不同的角度思考子论点。请注意每个子论点的结尾必须是符号“<sep>”。 
    """

    # 3 
    # input = claim
    rebuttal_prompt = """
    论点：{input}
    【要求】：阅读论点并反驳它。输出{num_branches}句反对论点，请注意每句反对论点的结尾必须是符号“<sep>”。
    """
    
    # 4 ????新的claim 总是承认，能不能直接限定呢
    improve_claim_from_rebuttal_prompt = """
    论点：{claim}
    反对论点：{rebuttal}
    【要求】：考虑到反对论点所指出的弱点，改进上述论点。写出一则直接、简洁、深刻的论点，不需要有任何论据支持，也不要再次承认自己的弱点。 
    """   
    
    
    # 5
    counter_rebuttal_prompt = """
    论点：{claim}
    反对论点：{rebuttal}    
    【要求】：仔细审查给出的论点和反对论点。请写一则简短而有说服力的反驳来为你的论点辩护或者给出解决方案。 
    """
    
    # 6
    # input=claim
    evidence_prompt = """
    论点：{input}    
    【要求】：为了支持这一论点，请考虑现实生活中的事件、数据等，写出{num_branches}句论据捍卫给出的论点。请注意每条论据必须的结尾必须是符号“<sep>”。 
    """
    

    # 8
    improve_final_majorclaim_prompt="""
    写作要求：{input}
    论点：{claim}    
    【要求】：根据写作要求，写一段简洁的、议论性的、连贯的论文主旨（中心论点）。论文主旨应涵盖所列的论点。
    """
    
    # 1
    body_para_prompt="""
    中心论点：{claim}\n

    【提示】
    论据：{evidence}\n
    反对论点：{rebuttal}\n
    反驳：{counter_rebuttal}\n
    【要求】
    {argument_relation_prompt} 为了支持中心论点，请用流畅性、逻辑性的语言写一个段落。请注意要用中文。
    """
    
    
    body_para_prompt_wo_dia_planning="""
    Claim: {claim}\n

    <Instruction>  请用中文写一段连贯且有说服力的段落来支持这一论点。为了避免冗余，请做出合适的删减。</Instruction> 
    """
    
    body_para_prompt_wo_undercutting_rebuttal="""
    Claim: {claim}\n

    Evidence: {evidence}

    <Instruction> 提供以上信息，请用中文写一段连贯且有说服力的段落来支持这一论点。为了避免冗余，请做出合适的删减。 </Instruction> 
    """
    
    
    # 论元结构
    # 考虑不写的那么规整，更清晰的instruct
    argument_relation_prompt = {
        "Simple":"你会得到上述提示。",
        "sLink":"论据对支持论点很重要。反对论点和反驳是可选的。",
        "Component":"论点和论据的主要结合，加上反对论点和反驳的互补整合，决定了论证过程的质量。",
        # "Hard_Relation":"Component Relation: Evidence supports Claim; Rebuttal attacks Claim; Counter_rebuttal attacks Rebuttal but supports Claim.",
        "Relation":"论据对支持论点很重要。你需要根据反驳充分驳斥和解决反对论点的内容，以进一步支持该论点。",
        "CR":"论点需要论据支持。如果反对论点削弱了中心论点，建议你根据反驳充分解决反对论点，这样可以有力支持中心论点。",
    }
    
    # 2
    intro_para_prompt = """
    写作要求：{input}
    中心论点：{majorclaim}
    【要求】：根据写作要求，用中文写一段议论文的引言介绍。引言介绍应该清楚地说明中心论点。
    """
    
    # 3
    conclusion_para_prompt = """
    论点：{claim}
    【要求】：根据上述论点用中文写一段简短清晰的议论文结论。
    """
    
    essay_fianl_prompt = """
    引入：{introduction}  主体：{paragraph} \n 结尾：{conclusion} \n
    【要求】：请从流畅性、逻辑性修改上述文字，用中文输出修改后的议论文。
    """
    
    io_prompt = """
    写作要求：{input}
    根据上面的写作要求，写一篇议论文。你的输出应该是以下格式：
    
    <essay> 此处为议论文 </essay> 
    """

    score_paragraph_prompt="""
    Here is an argumentative body paragraph：{paragraph}
    

    A score of 100 for evidence abundance implies that the provided evidence sufficiently supports the claim, while a score of 0 implies that there is no valid evidence. The final score for evidence abundance should be between <Evidence> and </Evidence>
    A score of 100 for insight implies that the essay is thoughtful with valuable insight, while a score of 0 implies that the essay is too naive or one-sided. The final score for insight of essay should be between <Insight> and </Insight>.
    A score of 100 for persuasiveness implies that the paragraph is convincing with coherent logical flow, while a score of 0 implies that the paragraph is illogical and self-contradictory. The final score for persuasiveness should be between <Persuade> and </Persuade>. 
    <Instruction> Provide reasoning for your scoring and place the score numbers between corresponding tags without any additional text. </Instruction>
    """
    
    score_claim_prompt="""
    写作要求：{input}
    论点: {claim}
    
    分析论点的质量，从0到10分打分，10分表示该观点是有深度的，批判性的，并且与要求高度相关。，在<score>和</score>之间输出你的整数评分，其中没有任何额外的文本。
    """
    
    cot_prompt="""
    写作要求：{input}
    
    根据写作提示写一篇议论文。
    
    制定一个简短的计划，然后写下来。你的输出应该是以下格式:
    
    <plan>此处为计划</plan>
    
    <essay>此处为议论文</essay>
    """
    
    tot_plan_prompt="""
    写作要求：{input}
    原本的写作计划：{plan}
    
    制定或改进写议论文的原计划。 你的输出应该是以下格式：
    
    <plan>此处为计划</plan>
    """
    
    tot_essay_prompt="""
    写作要求：{input}
    写作计划：{plan}
    
    根据写作提示写一篇议论文。你可以按照写作计划写。
    你的输出应该是以下格式:
    
    <essay>此处为议论文</essay>
    """
    
    tot_score_prompt="""
    写作计划：{plan}
    
    分析议论文写作计划的质量。从0到10分打分，10分意味着这个计划是连贯的、合乎逻辑的。
    给出你的评分理由，并将得分数字放在<score>和</score>标签之间。
    """

    generate_prompt_selector = {
        "majorclaim":init_majorclaim_prompt,
        "claim":claim_prompt,
        "rebuttal":rebuttal_prompt,
        "evidence":evidence_prompt,
        
        # "cot_prompt":cot_prompt,
        # "tot_plan_prompt":tot_plan_prompt,
        # "tot_essay_prompt":tot_essay_prompt
        # "io_prompt": io_prompt 
    }
    
    aggregate_prompt_selector = {
        "counter_rebuttal":counter_rebuttal_prompt,
        "conclusion":conclusion_para_prompt,
        "introduction":intro_para_prompt,
        "paragraph":body_para_prompt,
        "essay":essay_fianl_prompt,
        "slot":slot_plan_update_prompt
    }
    
    refine_prompt_selector = {
        "claim":improve_claim_from_rebuttal_prompt,
        "majorclaim":improve_final_majorclaim_prompt,
    }
    
    integ_prompt_selector = {
        "slot":slot_plan_update_prompt
    }
    
    score_prompt_selector = {
        "paragraph":score_paragraph_prompt,
        "claim":score_claim_prompt,
    }

    def __init__(self, argument_relation_prompt="",ablation_method="") -> None:
        self.body_para_prompt = self.body_para_prompt.format(claim="{claim}",evidence="{evidence}",rebuttal="{rebuttal}",counter_rebuttal="{counter_rebuttal}",argument_relation_prompt=self.argument_relation_prompt[argument_relation_prompt])
        if ablation_method == "gotDPE_wo_dia_planning":
            self.body_para_prompt = self.body_para_prompt_wo_dia_planning
        elif ablation_method == "gotDPE_wo_undercutting_rebuttal":
            self.body_para_prompt = self.body_para_prompt_wo_undercutting_rebuttal
        self.aggregate_prompt_selector["paragraph"]=self.body_para_prompt
        super().__init__()

    def aggregation_prompt(self, state_dicts: List[Dict], target_type:str, **kwargs) -> str:
        """
        Generate an aggregation prompt for the language model.

        :param state_dicts: The thought states that should be aggregated.
        :type state_dicts: List[Dict]
        :param kwargs: Additional keyword arguments.
        :return: The aggregation prompt.
        :rtype: str
        :raise AssertionError: If not exactly two thought states are provided.
        """
        # pack state_dicts
        merge_dict = {
            "input":[],
            "claim":[],
            "evidence":[],
            "rebuttal":[],
            "counter_rebuttal":[],
            "majorclaim":[],
            "introduction":[],
            "conclusion":[],
            "paragraph":[],
            }
        merge_dict['input']=[state_dicts[0]['original']]
        for state in state_dicts:
            type_ = state['type']
            if type_ not in merge_dict:
                raise TypeError("please predefine a key {} in the template".format(type_))
            else:
                merge_dict[type_].append(state['current'])
        for key,value in merge_dict.items():
            
            value_ = ["{}".format(v.strip()) for v in value]
            if key == "paragraph":
                merge_dict[key]='\n'.join(value_)
            else:
                merge_dict[key]='<sep>'.join(value_)

        prompt =  self.aggregate_prompt_selector[target_type].format(**merge_dict)
        return prompt

    
    def generate_prompt(self, num_branches: int, original: str, current: str, method: str, target_type:str=None, **kwargs) -> str:
        """
        Generate a generate prompt for the language model.

        :param num_branches: The number of responses the prompt should ask the LM to generate.
        :type num_branches: int
        :param original: Input list of numbers.
        :type original: str
        :param current: Intermediate solution.
        :type current: str
        :param method: Method for which the generate prompt is generated.
        :type method: str
        :param kwargs: Additional keyword arguments.
        :return: The generate prompt.
        :rtype: str
        :raise AssertionError: If the requested number of branches is not one.
        """
        # pack state_dicts
        kwargs["num_branches"]=num_branches
        if current is None or current == "":
            kwargs['input']=original
        else:
            kwargs['input']=current
        if method.startswith("io"):
            return self.io_prompt.format(**kwargs)
        elif method.startswith("cot"):
            prompt = self.cot_prompt.format(**kwargs)
            return prompt
        elif method.startswith("tot"):
            # parm: plan w_prompt
            if target_type == "plan":
                kwargs['plan']=None
                prompt = self.tot_plan_prompt.format(**kwargs)
            elif target_type == "essay":
                kwargs['input']=original
                kwargs['plan']=current
                prompt = self.tot_essay_prompt.format(**kwargs)
            return prompt
        elif method.startswith("gotDPE"):
            prompt = self.generate_prompt_selector[target_type].format(**kwargs)
            return prompt
        return 
    
    def improve_prompt(self, state_dicts: List[Dict], target_type:str, **kwargs) -> str:
        """
        Generate an improve prompt for the language model.

        :param kwargs: Additional keyword arguments.
        :return: The improve prompt.
        :rtype: str
        """
        # pack state_dicts
        merge_dict = {
            "input":[],
            "claim":[],
            "rebuttal":[],
        }
        for state in state_dicts:
            type_ = state['type']
            if type_ not in merge_dict:
                merge_dict[type_] = [state['current']]
            else:
                merge_dict[type_].append(state['current'])
        for key,value in merge_dict.items():
            value_ = ["{}".format(v) for v in value]
            merge_dict[key]=' '.join(value_)
        if target_type == "majorclaim":
            merge_dict['input']=state['original']
        prompt =  self.refine_prompt_selector[target_type].format(**merge_dict)
        return prompt
    
    def integ_prompt(self, state_dicts: List[Dict], target_type:str, **kwargs) -> str:
            # pack state_dicts
        merge_dict = {"claim":[],"evidence":[],"rebuttal":[],"counter_rebuttal":[]}
        for state in state_dicts:
            type_ = state['type']
            if type_ not in merge_dict:
                merge_dict[type_] = [state['current']]
            else:
                merge_dict[type_].append(state['current'])
        for key,value in merge_dict.items():
            value_ = ["{}".format(v) for v in value]
            merge_dict[key]=' '.join(value_)

        prompt =  self.integ_prompt_selector[target_type].format(**merge_dict)
        return prompt

    def validation_prompt(self, **kwargs) -> str:
        """
        Generate a validation prompt for the language model.

        :param kwargs: Additional keyword arguments.
        :return: The validation prompt.
        :rtype: str
        """
        pass

    def score_prompt(self, state_dicts: List[Dict], **kwargs) -> str:
        """
        Generate a score prompt for the language model.

        :param state_dicts: The thought states that should be scored,
                            if more than one, they should be scored together.
        :type state_dicts: List[Dict]
        :param kwargs: Additional keyword arguments.
        :return: The score prompt.
        :rtype: str
        """
        # pack state_dicts
        merge_dict = {
            "paragraph":[],
            "plan":[],
            "claim":[],
            "input":[]
            }
        type_consist_ensure = []
        for state in state_dicts:
            merge_dict['input'] = [state["original"]]
            method = state['method']
            type_ = state['type']
            type_consist_ensure.append(type_)
            if type_ not in merge_dict:
                raise TypeError("please predefine a key {} in the template".format(type_))
            else:
                merge_dict[type_].append(state['current'])
        for key,value in merge_dict.items():
            value_ = ["{}".format(v) for v in value]
            merge_dict[key]=' '.join(value_)
        assert len(set(type_consist_ensure)) == 1
        target_type = type_consist_ensure[0]
        merge_dict['method']=method
        if merge_dict['method'].startswith("gotDPE"):
            prompt =  self.score_prompt_selector[target_type].format(**merge_dict)
        elif merge_dict['method'].startswith("tot"):
            prompt =  self.tot_score_prompt.format(**merge_dict)
        return prompt

