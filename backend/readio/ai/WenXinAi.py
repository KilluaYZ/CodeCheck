import erniebot
erniebot.api_type = 'qianfan'
erniebot.ak = '61LSVpKQkIAxRGoxGq1Ez6lT'
erniebot.sk = '4uFsoZ3O9GxPzEGlTieNjYpkcWqFVMij'
stream = False

def chat(chat_history: list):
    response = erniebot.ChatCompletion.create(
        model='ernie-bot',
        messages=chat_history,
        top_p=0.9,
        stream=stream,
        system="你是一个IT领域的专家，熟练掌握诸如C，C++，Java，Python等常用的各种编程语言，"
               "此外你还是一个信息安全领域的专家，对各种类型的漏洞都有了解，并能给出专业的建议。"
               "现在你被中国人民大学信息学院信息安全实验室雇佣，成为该实验室中的小助手，你将协助"
               "该实验室的工作人员进行模糊测试，漏洞挖掘等方面的研究，提供你的见解和建议，你很擅长"
               "阅读代码，所以也会为他们解读代码。有一点十分值得注意！欺骗和模糊的信息在这里是绝对"
               "绝被禁止的！你在任何时候，任何情况下，无论对方问什么，你都只能给出确切的，真实的答案"
               "对于一个你不知道怎么回答的问题你可以让他重新表述得更清晰或直接回答不知道，但绝对不允许"
               "欺骗他！"
    )
    result = ''
    if stream:
        for resp in response:
            resp_result = resp.get_result()
            result += resp_result
    else:
        result = response.get_result()

    chat_history.append({
        "role": "assistant",
        "content": result
    })

    return chat_history, result
