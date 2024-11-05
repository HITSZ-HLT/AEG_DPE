depth_ind_dict_en = {
    # 1:"The author ambiguously states their opinions with little real argumentation.",
    1:"The authors state their opinions with some reasons",
    2:"The authors state their major claims and demonstrate from different aspects. However, the authors only give some short personal narratives to poorly support the claims.",
    3:"The authors state their major claims and demonstrate from different aspects. The authors write in a flat reasoning structure where each claim is supported by a few independent backings. The reasoning is generalized or shallow.",
    4:"The authors state their major claims and demonstrate from different aspects. The authors write in a hierarchical reasoning structure. However, the authors can make improvements and discuss more deeply.",
    5:"The authors state their major claims and demonstrate from different aspects. The authors carefully build up a complex but traceable tree-like reasoning structure in favor of the claims. Overall, the essay discusses deeply into a controversial issue.",
}

depth_ind_dict_zh = {
    # 1:"The author ambiguously states their opinions with little real argumentation.",
    1:"作者陈述了他们的观点，并给出了一些理由",
    2:"作者陈述了他们的主要观点，并从不同的角度进行了论证。然而，作者只给出了一些简短的个人叙述来支持这些说法。",
    3:"作者陈述了他们的主要观点，并从不同的角度进行了论证。作者以一种扁平的推理结构写作，其中每个论点由几个独立的论据来支持。推理过于笼统或肤浅。",
    4:"作者陈述了他们的主要观点，并从不同的角度进行了论证。作者以分层推理结构写作。但是，作者可以进行改进和更深入的讨论。",
    5:"作者陈述了他们的主要观点，并从不同的角度进行了论证。作者仔细地建立了一个复杂但可追溯的树状推理结构，以支持这些论点。总之，本文深入探讨了一个有争议的问题。",
}

reasonableness_ind_dict_en = {
    1: "The authors do not conclude by analysis. The authors do not contribute to the resolution of the issue and do not address counterarguments.",
    2: "The authors provide little information to support the claims and thus neither contribute to the resolution nor draw a valid conclusion. Counterarguments are not addressed.",
    3: "The authors analyze and present some information to support the claims.  The authors mention counterarguments but barely rebut them.",
    4: "The readers may not accept the conclusion because it makes broad generalizations or lacks enough supportive information. The authors address counterarguments but may not adequately rebut them.",
    5: "The readers would accept the conclusion and consider it in the larger discussion. The authors rebut and adequately address counterarguments.",
}

reasonableness_ind_dict_zh = {
    1: "作者没有通过分析得出结论。作者没有对问题的解决做出贡献，也没有提出反对意见。。",
    2: "作者仅仅提供了很少的资料来支持他们的论点，因此既没有对解决方法作出贡献，也没有得出有效的结论。反对意见没有得到解决。",
    3: "作者分析并提出了一些支持这些说法的信息。作者提到了反对意见，但没有反驳。",
    4: "读者可能不接受结论，因为它过于笼统或缺乏足够的支持性信息。作者提出了反对意见，但可能没有充分反驳。",
    5: "读者会接受这个结论，并在更大的讨论中考虑它。作者充分反驳并解决了反对意见。",
}


richness_ind_dict_en = {
    1:"The essay includes major claims, claims but no evidence.",
    2:"The essay presents major claims. In some paragraphs, the claims are supported by a few evidence.",
    3:"The essay presents major claims. In each paragraph, the claims are supported by evidence.  However, the evidence can be more specific.",
    4:"The essay presents major claims, claims, and corresponding abundant evidence in each paragraph.  The evidence provides some basic reasons or examples.",
    5:"The essay includes major claims, claims, and corresponding abundant evidence in each paragraph.  The evidence provides effective facts or statistics.  The authors also provide further discussions such as calls for action, suggestions, etc."
}

richness_ind_dict_zh = {
    1:"这篇文章包括主要论点，分论点但没有论据。",
    2:"这篇文章提出了主要论点。在一些段落中，这些论点得到了一些论据的支持。",
    3:"这篇文章提出了主要论点。在每一段中，这些论点都有论据支持。然而，论据可以更具体。",
    4:"这篇文章在每个段落中都提出了主要论点、论点和相应的充分论据。论据提供了一些基本的原因或例子。",
    5:"这篇文章在每一段都包含了主要论点、论点和相应的充分论据。论据提供了有效的事实或统计数据。作者还提供了进一步的讨论，如呼吁采取行动，建议等。"
}


cogency_ind_dict_en = {
     1:"The authors provide no evidence for their claims.",
     2:"The evidence for the author's claim may not be believable. The authors do not provide support to draw a conclusion.",
     3:"The authors provide some relevant and acceptable evidence (the evidence can be more specific) for their claims but not enough to draw a conclusion.",
     4:"The essay includes acceptable and relevant evidence (basic reasons or examples) that may or may not provide enough support to draw a conclusion.",
     5:"The essay contains acceptable and believable evidence for the author's claims. The evidence (effective facts or statistics) is relevant to the author's point and is sufficient for drawing a conclusion. "
}

cogency_ind_dict_zh = {
    1:"作者没有为他们的说法提供证据。",
    2:"作者论点的论据可能不可信。作者没有提供支持来得出结论。",
    3:"作者为他们的论点提供了一些相关和可接受的理由，证据可以更具体，但不足以得出结论。",
    4:"文章包括可接受的和相关的论据（基本原因或例子），可能或可能未提供足够的支持来得出结论。",
    5:"这篇文章为作者的论点提供了可接受和可信服的论据（有效事实或统计数据）。证据与作者的观点相关，足以得出结论。"
}

persuasiveness_ind_dict_en = {
    1:"The way the essay is written and organized is hard to follow. The content is not presented in a sensical order.",
    2:"The authors evoke emotions that make the readers less likely to agree. The authors do not use clear language or organization.",
    3:"Although the argumentative essay is appropriate, the authors do not evoke an emotional response. The organization of the argument could be improved.",
    4:"The authors use clear and appropriate language and structure their argument in a way that makes sense. The essay is lacking in emotional appeal.",
    5:"The authors present their argument using clear organization and language. The authors demonstrate their opinion with supporting points, which is an effective organizational structure. The author evokes emotions that make the argument more agreeable."
}

persuasiveness_ind_dict_zh = {
    1:"这篇文章的写作和组织方式很难理解。内容没有按合理的顺序呈现。",
    2:"作者唤起了读者不太可能同意的情绪。作者没有使用清晰的语言或组织。",
    3:"虽然议论文是合适的，但作者并没有引起情感上的反应。辩论的组织可以改进。",
    4:"作者使用清晰和适当的语言，并以一种有意义的方式组织他们的论点。这篇文章缺乏情感感染力。",
    5:"作者用清晰的组织和语言提出了他们的论点。作者用论点论证自己的观点，这是一种有效的组织结构。作者唤起了人们的情感，使他的论点更令人愉快。"
}


depth_ind_en =f"""
文章深度(Argument Depth):
1-{depth_ind_dict_en[1]}
2-{depth_ind_dict_en[2]}
3-{depth_ind_dict_en[3]}
4-{depth_ind_dict_en[4]}
5-{depth_ind_dict_en[5]}
"""

depth_ind_zh =f"""
Description of Argument Depth:
1-{depth_ind_dict_zh[1]}
2-{depth_ind_dict_zh[2]}
3-{depth_ind_dict_zh[3]}
4-{depth_ind_dict_zh[4]}
5-{depth_ind_dict_zh[5]}
"""

depth_ind_en_option =f"""
Description of Argument Depth, choose a best option that best describes the essay:
A-{depth_ind_dict_en[2]}
B-{depth_ind_dict_en[4]}
C-{depth_ind_dict_en[5]}
D-{depth_ind_dict_en[1]}
E-{depth_ind_dict_en[3]}
"""


depth_ind = f"""
Description of Argument Depth:
1-{depth_ind_dict_en[1]} {depth_ind_dict_zh[1]}
2-{depth_ind_dict_en[2]} {depth_ind_dict_zh[2]}
3-{depth_ind_dict_en[3]} {depth_ind_dict_zh[3]}
4-{depth_ind_dict_en[4]} {depth_ind_dict_zh[4]}
5-{depth_ind_dict_en[5]} {depth_ind_dict_zh[5]}
"""



reasonableness_ind_en=f"""
Description of Reasonableness:
1-{reasonableness_ind_dict_en[1]}
2-{reasonableness_ind_dict_en[2]}
3-{reasonableness_ind_dict_en[3]}
4-{reasonableness_ind_dict_en[4]}
5-{reasonableness_ind_dict_en[5]}
"""

reasonableness_ind_zh = f"""
文章辩证性(Reasonableness):
1-{reasonableness_ind_dict_zh[1]}
2-{reasonableness_ind_dict_zh[2]}
3-{reasonableness_ind_dict_zh[3]}
4-{reasonableness_ind_dict_zh[4]}
5-{reasonableness_ind_dict_zh[5]}
"""

reasonableness_ind_en_option=f"""
Description of Reasonableness, choose a best option that best describes the essay:
A-{reasonableness_ind_dict_en[5]}
B-{reasonableness_ind_dict_en[3]}
C-{reasonableness_ind_dict_en[1]}
D-{reasonableness_ind_dict_en[2]}
E-{reasonableness_ind_dict_en[4]}
"""

reasonableness_ind = f"""
Description of Reasonableness:
1-{reasonableness_ind_dict_en[1]} {reasonableness_ind_dict_zh[1]}
2-{reasonableness_ind_dict_en[2]} {reasonableness_ind_dict_zh[2]}
3-{reasonableness_ind_dict_en[3]} {reasonableness_ind_dict_zh[3]}
4-{reasonableness_ind_dict_en[4]} {reasonableness_ind_dict_zh[4]}
5-{reasonableness_ind_dict_en[5]} {reasonableness_ind_dict_zh[5]}
"""



richness_ind_en =f"""
Description of Content Richness:
1-{richness_ind_dict_en[1]}
2-{richness_ind_dict_en[2]}
3-{richness_ind_dict_en[3]}
4-{richness_ind_dict_en[4]}
5-{richness_ind_dict_en[5]} 
"""

richness_ind_zh =f"""
Description of Content Richness:
1-{richness_ind_dict_zh[1]}
2-{richness_ind_dict_zh[2]}
3-{richness_ind_dict_zh[3]}
4-{richness_ind_dict_zh[4]}
5-{richness_ind_dict_zh[5]} 
"""

richness_ind_en_option =f"""
Description of Content Richness, choose a best option that best describes the essay:
A-{richness_ind_dict_en[3]}
B-{richness_ind_dict_en[1]}
C-{richness_ind_dict_en[2]}
D-{richness_ind_dict_en[5]}
E-{richness_ind_dict_en[4]} 
"""

richness_ind =f"""
Description of Content Richness:
1-{richness_ind_dict_en[1]} {richness_ind_dict_zh[1]}
2-{richness_ind_dict_en[2]} {richness_ind_dict_zh[2]}
3-{richness_ind_dict_en[3]} {richness_ind_dict_zh[3]}
4-{richness_ind_dict_en[4]} {richness_ind_dict_zh[4]}
5-{richness_ind_dict_en[5]} {richness_ind_dict_zh[5]}
"""
 


cogency_ind_en = f"""
Description of Cogency:
1-{cogency_ind_dict_en[1]}
2-{cogency_ind_dict_en[2]}
3-{cogency_ind_dict_en[3]}
4-{cogency_ind_dict_en[4]}
5-{cogency_ind_dict_en[5]}
"""

cogency_ind_zh = f"""
文章逻辑性(Cogency):
1-{cogency_ind_dict_zh[1]}
2-{cogency_ind_dict_zh[2]}
3-{cogency_ind_dict_zh[3]}
4-{cogency_ind_dict_zh[4]}
5-{cogency_ind_dict_zh[5]}
"""

cogency_ind_en_option = f"""
Description of Cogency, choose a best option that best describes the essay:
A-{cogency_ind_dict_en[5]}
B-{cogency_ind_dict_en[2]}
C-{cogency_ind_dict_en[1]}
D-{cogency_ind_dict_en[3]}
E-{cogency_ind_dict_en[4]}
"""

cogency_ind = f"""
Description of Cogency:
1-{cogency_ind_dict_en[1]} {cogency_ind_dict_zh[1]}
2-{cogency_ind_dict_en[2]} {cogency_ind_dict_zh[2]}
3-{cogency_ind_dict_en[3]} {cogency_ind_dict_zh[3]}
4-{cogency_ind_dict_en[4]} {cogency_ind_dict_zh[4]}
5-{cogency_ind_dict_en[5]} {cogency_ind_dict_zh[5]}
"""



persuasiveness_ind_en = f"""
Description of Persuasiveness:
1-{persuasiveness_ind_dict_en[1]}
2-{persuasiveness_ind_dict_en[2]}
3-{persuasiveness_ind_dict_en[3]}
4-{persuasiveness_ind_dict_en[4]}
5-{persuasiveness_ind_dict_en[5]}
"""

persuasiveness_ind_zh = f"""
文章说服力(Persuasiveness):
1-{persuasiveness_ind_dict_zh[1]}
2-{persuasiveness_ind_dict_zh[2]}
3-{persuasiveness_ind_dict_zh[3]}
4-{persuasiveness_ind_dict_zh[4]}
5-{persuasiveness_ind_dict_zh[5]}
"""

persuasiveness_ind_en_option = f"""
Description of Persuasiveness, choose a best option that best describes the essay:
A-{persuasiveness_ind_dict_en[3]}
B-{persuasiveness_ind_dict_en[1]}
C-{persuasiveness_ind_dict_en[5]}
D-{persuasiveness_ind_dict_en[4]}
E-{persuasiveness_ind_dict_en[2]}
"""


persuasiveness_ind = f"""
Description of Persuasiveness:
1-{persuasiveness_ind_dict_en[1]} {persuasiveness_ind_dict_zh[1]}
2-{persuasiveness_ind_dict_en[2]} {persuasiveness_ind_dict_zh[2]}
3-{persuasiveness_ind_dict_en[3]} {persuasiveness_ind_dict_zh[3]}
4-{persuasiveness_ind_dict_en[4]} {persuasiveness_ind_dict_zh[4]}
5-{persuasiveness_ind_dict_en[5]} {persuasiveness_ind_dict_zh[5]}
"""




instruct_prompt = """
You are provided with an argumentative essay and some descriptions about Reasonableness, Cogency, and Persuasiveness. Please select the most appropriate description of the essay ranging from 1 to 5.  You need to output your options in JSON format. An example is as follows:
{{"Reasonableness": 3, "Cogency":3 ,"Persuasiveness":3}}    
"""

instruct_prompt_feedback = """
You are provided with an argumentative essay and some descriptions about Reasonableness, Cogency, and Persuasiveness. You should first provide a brief feedback of the essay's quality. Then, please select the most appropriate description of the essay ranging from 1 to 5.  You need to output your options in JSON format. An example is as follows:
{{"Feedback": "Feedback should cover pros, cons, suggestions, etc." , "Reasonableness": 3,"Cogency":3 ,"Persuasiveness":3}}    
"""

instruct_prompt_feedback_zh = """
你需要对一篇议论文关于辩证性、逻辑性和说服力的描述进行选择。首先，你应该对文章的质量给出一个简短的反馈。然后，请从1到5中选择最合适的描述。您需要以JSON格式输出选项。示例如下:
{{"Feedback": "反馈包括优点、缺点和建议等" , "Reasonableness": 3,"Cogency":3 ,"Persuasiveness":3}}    
"""

instruct_prompt_option = """
You are provided with an argumentative essay and some descriptions about Reasonableness, Cogency, and Persuasiveness. Please select the most appropriate description of the essay ranging from 1 to 5. You need to output your options in JSON format. An example is as follows:
{{"Argument Depth": "A", "Reasonableness": "B", "Content Richness":"C" ,"Cogency":"D" ,"Persuasiveness":"E"}}    
"""


input_prompt_template = """
Argumentative Essay:
{essay}


Scores:
{reasonableness_ind_en}{cogency_ind_en}{persuasiveness_ind_en}

Instructions:
{instruct_prompt}
"""

sample_input="""
In today's interconnected world, the importance of learning English in school cannot be overstated. English has established itself as the lingua franca of international communication, business, and academia. In my opinion, it is important for everyone to learn English, but we should also make concerted efforts to ensure the survival of local languages. 





Firstly, learning English is crucial for individuals on a global scale. English serves as a bridge between nations, allowing individuals from different countries to communicate effectively. It is the language of international trade, enabling businesses to expand beyond their domestic markets and connect with partners worldwide.

However, while English is undoubtedly important, we must not forget the vital role that local languages play in our cultural diversity. Local languages are not merely means of communication; they hold immense cultural and historical significance. They are repositories of traditional knowledge, storytelling, and expressions of identity. 

Therefore, it is crucial to strike a balance between learning English and preserving local languages. One way to achieve this is by incorporating local languages into school curricula alongside English. This not only preserves local languages but also helps students develop cognitive skills, enhance cultural awareness, and foster appreciation for linguistic diversity. 

In conclusion, while learning English is undeniably important for global communication and opportunities, it is equally crucial to ensure the survival of local languages. By striking a balance between the two objectives, we can equip students with English language skills while preserving the cultural significance and diversity that local languages bring. 
"""

sample_score="""
{"Argument Depth": 3, "Reasonableness": 3, "Content Richness":3 ,"Cogency":4 ,"Persuasiveness":3} 
"""

sample_input_h = """
Nowadays, people travel to other countries for holidays for various reasons. This phenomenon has both positive and negative implications for the countries being visited. On one hand, it benefits the local tourism industry and promotes cultural exchange. However, it can also lead to problems such as overcrowding and environmental degradation. Thus, it can be argued that this trend has both positive and negative aspects for the countries they travel to.

Traveling to other countries for holidays can indeed support the local tourism industry through increased spending on accommodation, food, and tourism activities. The World Travel & Tourism Council highlights the massive economic impact of international tourism, generating $1.7 trillion in revenue for destinations worldwide. Additionally, popular tourist destinations like Bali have experienced an influx of international visitors, resulting in an estimated $10 billion in tourism revenue.  Although some money may go to international chains, it is important to recognize that local businesses such as boutique hotels, family-owned restaurants, and small tour operators also benefit from tourist spending. Therefore, it is clear that traveling to other countries for holidays plays a vital role in supporting the local tourism industry.

Interacting with a diverse range of people from different cultures and communities during holiday travel has the potential to significantly contribute to improved global relations. The increasing number of international tourist arrivals means that more people are engaging in cross-cultural interactions during their holidays. This exposure to different cultures allows individuals to develop a broader perspective and empathy towards others, ultimately fostering a greater understanding and appreciation of cultural diversity. While improved global relations require a more comprehensive and systematic approach, holiday interactions can play a crucial role in breaking down stereotypes and prejudices, creating personal connections that can be translated into broader diplomatic efforts. By promoting empathy and cultural understanding, these interactions lay the foundation for more meaningful and productive dialogue, ultimately leading to improved global relations.

However, tourist destinations may face challenges due to the influx of visitors during holiday seasons. Overcrowding, pollution, and cultural commodification are some of the issues that arise. Venice, for example, struggles with overcrowding in popular spots like St. Mark's Square, with around 30 million tourists annually. This strain on the city's infrastructure leads to traffic congestion, long queues, and difficulty accessing public services. Similarly, Bali faces significant pollution problems during peak tourist periods. The island's limited waste management facilities struggle to cope with the increased garbage generated by tourists, and the high demand for water resources leads to over-extraction, diminishing freshwater supplies and harming the local ecosystem. While tourism can have positive impacts on the local economy, such as job creation and support for local businesses, we cannot ignore the long-term consequences of unchecked tourism. The strain on infrastructure and the negative effects on the environment and cultural heritage call for a balanced approach that protects and preserves the destination for future generations.

In conclusion, holiday travel can support the local tourism industry and foster improved global relations, but it also comes with potential drawbacks such as overcrowding, pollution, and cultural commodification. To ensure the sustainability and authenticity of tourist destinations, it is crucial for both travelers and the tourism industry to prioritize responsible and respectful travel practices. By doing so, we can ensure that the benefits of holiday travel outweigh the negative impacts, creating a positive and mutually beneficial experience for both the travelers and the countries they visit.
"""

sample_score_h="""
{"Argument Depth": 5, "Reasonableness": 4, "Content Richness":5 ,"Cogency":5 ,"Persuasiveness":5} 
"""



input_prompt = input_prompt_template.format(essay="{essay}",reasonableness_ind_en=reasonableness_ind_en,cogency_ind_en=cogency_ind_en,persuasiveness_ind_en=persuasiveness_ind_en,instruct_prompt=instruct_prompt_feedback)

input_prompt = input_prompt_template.format(essay="{essay}",reasonableness_ind_en=reasonableness_ind_en,cogency_ind_en=cogency_ind_en,persuasiveness_ind_en=persuasiveness_ind_en,instruct_prompt=instruct_prompt_feedback)


input_prompt_template_zh = """
论文:
{essay}


评分细则:
{reasonableness_ind_zh}{cogency_ind_zh}{persuasiveness_ind_zh}

要求:
{instruct_prompt}
"""

sample_input="""
In today's interconnected world, the importance of learning English in school cannot be overstated. English has established itself as the lingua franca of international communication, business, and academia. In my opinion, it is important for everyone to learn English, but we should also make concerted efforts to ensure the survival of local languages. 

Firstly, learning English is crucial for individuals on a global scale. English serves as a bridge between nations, allowing individuals from different countries to communicate effectively. It is the language of international trade, enabling businesses to expand beyond their domestic markets and connect with partners worldwide.

However, while English is undoubtedly important, we must not forget the vital role that local languages play in our cultural diversity. Local languages are not merely means of communication; they hold immense cultural and historical significance. They are repositories of traditional knowledge, storytelling, and expressions of identity. 

Therefore, it is crucial to strike a balance between learning English and preserving local languages. One way to achieve this is by incorporating local languages into school curricula alongside English. This not only preserves local languages but also helps students develop cognitive skills, enhance cultural awareness, and foster appreciation for linguistic diversity. 

In conclusion, while learning English is undeniably important for global communication and opportunities, it is equally crucial to ensure the survival of local languages. By striking a balance between the two objectives, we can equip students with English language skills while preserving the cultural significance and diversity that local languages bring. 
"""


input_prompt = input_prompt_template.format(essay="{essay}",depth_ind_en=depth_ind_en,reasonableness_ind_en=reasonableness_ind_en,richness_ind_en=richness_ind_en,cogency_ind_en=cogency_ind_en,persuasiveness_ind_en=persuasiveness_ind_en,instruct_prompt=instruct_prompt_feedback)
input_prompt_zh = input_prompt_template_zh.format(essay="{essay}",depth_ind_zh=depth_ind_zh,reasonableness_ind_zh=reasonableness_ind_zh,richness_ind_zh=richness_ind_zh,cogency_ind_zh=cogency_ind_zh,persuasiveness_ind_zh=persuasiveness_ind_zh,instruct_prompt=instruct_prompt_feedback_zh)
# input_prompt = input_prompt_template.format(essay="{essay}",depth_ind_en=depth_ind_en_option,reasonableness_ind_en=reasonableness_ind_en_option,richness_ind_en=richness_ind_en_option,cogency_ind_en=cogency_ind_en_option,persuasiveness_ind_en=persuasiveness_ind_en_option,instruct_prompt=instruct_prompt_option)

if __name__ == "__main__":

    print(input_prompt_zh.format(essay="hi"))