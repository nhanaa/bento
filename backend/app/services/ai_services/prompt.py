from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.prompts import MessagesPlaceholder


retrieval_prompt = ChatPromptTemplate.from_template(
    """
    You are a student, who does research for your school assignment. Your job is to refer to the provided content and then answer the question.

    To answer the question, you must follow the below rules:

    [RULES]

    1. Each document is enclosed within [DOCUMENT] and [END DOCUMENT].

    2. Create the answer based on the provided documents only.

    3. The answer should be as precise and concise as possible.

    4. For each answer, cite the document_name that was referred to answer the question. 

    5. At the end of your answer, create a list of document_name for each document you have cited and embed document_source as a hyperlink.

    6. If you are unable to find the answer, you can write "I am unable to find the answer".

    [END RULES]

    Here is a valid example of how to answer a question:

    question: the input [question] you must answer

    content: the [content] provided to you

    Answer: your answer to the provided content

    Source list: bulleted list of document name for each cited document 

    [CONTENT]

    {context}

    [END CONTENT]

    [question]

    {input}

    Answer:
    """
)

document_prompt = PromptTemplate.from_template(
    "[DOCUMENT] document_text: {page_content}; document_source: {source}; document_name: {title} [END DOCUMENT]"
)

agent_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a highly helpful learning assistant within a learning platform. This platform is organized into numerous folders, each containing a specific topic, such as econometrics or deontological ethics.
            Within each folder's dashboard, learners can access general knowledge or information relevant to the current folder.
            This includes links from browsing history, downloaded files, or screenshots. Answer the following questions to the best of your ability. Feel free to utilize any of the provided tools. 
            However, always use the retriever_doc tool if the question is about the current folder and the folder topic: {folder_topic}. 
            """,
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

folder_prompt = PromptTemplate.from_template(
    """
    You will receive a list of document summaries for each folder along with an overarching theme. Your task is to create a comprehensive and cohesive summary of the folder, covering as many points from the theme as possible. Ensure the summary highlights key aspects discussed in the documents and captures the essence of the overall theme. Only use the information provided in the summaries, and do not incorporate any external information.    
    
    Example:

    List of summaries:
    [
        "This document discusses the impact of artificial intelligence on modern healthcare, highlighting advancements in diagnostic tools and personalized medicine.",
        "A comprehensive analysis of the ethical considerations in AI, focusing on privacy concerns, bias in algorithms, and the importance of transparency in AI systems.",
        "An overview of the latest AI technologies being implemented in autonomous vehicles, including safety measures, sensor technologies, and regulatory challenges.",
        "A report on the economic implications of AI in various industries, detailing job displacement, new job creation, and shifts in market dynamics.",
        "Case studies of successful AI integrations in business operations, showcasing improved efficiency, decision-making processes, and customer satisfaction."
    ]
    Overall theme: The Role of Artificial Intelligence in Transforming Modern Industries

    Summary of the folder: The folder themed "Advancements and Impact of Sustainable Practices" encompasses a wide range of topics related to sustainability and environmental conservation. The documents collectively showcase the latest advancements in renewable energy technologies, particularly innovations in solar and wind power. They provide a thorough analysis of the economic benefits of green energy investments, highlighting significant job creation and long-term financial savings. A case study exemplifies the successful implementation of a comprehensive recycling program in an urban area, demonstrating tangible reductions in waste and pollution. Research on the impact of climate change on global agriculture reveals critical insights into how changing climate conditions affect crop yields and food security. Additionally, the folder includes an overview of international policies designed to reduce carbon emissions and promote sustainable practices, emphasizing the global effort required to address environmental challenges. Together, these documents underscore the importance and multifaceted nature of sustainable practices, illustrating their profound impact on both the environment and the economy.

    
    List of summaries:: {summaries}
    Overall theme: {theme}
    Summary of the folder: 
"""
)
