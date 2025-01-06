diversify_prompt = '''You are provided with a <constraint> in an instruction. As a prompt engineer, your task is to rephrase the provided <constraint> to make it more diverse. You ought to provide five more variants of the <constraint>. Make sure your revision does not change the meaning of the original <constraint>.
---INPUT---
<constraint>:
Your response should contain at least 3 sentences.
---OUTPUT---
variants:
1. Respond with at least three sentences
2. Use at least 3 sentences in your reply
3. Your entire response should include at least three sentences
4. Organize your entire response in at least 3 sentences
5. Please make sure the response at least 3 sentences long
---INPUT---
<constraint>:
{}
---OUTPUT---
variants:
'''


keyword_prompt = '''You are provided with an <instruction>. Your object is to come up some keywords that may be used to answer the <instruction>. They are usually related to the task described in the <instruction>. you should output your thinking process and the keywords you come up with.
---INPUT---
<instruction>:
Explain Generative Adversarial Networks (GANs) to me using bullet points. Do not contain any commas in your response. 
---OUTPUT---
thinking process:
the <instruction> as to explain GANs, hence, 'architecture','training' and 'generator' may be appropriate keywords to use in the answer.
keywords:
['architecture', 'training', 'generator']
---INPUT---
<instruction>:
{}
---OUTPUT---
'''


