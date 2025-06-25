from langchain_core.prompts import ChatPromptTemplate 
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough,RunnableParallel
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st

# The class inherits StrOutputParser class and on top of that add more filters 
# This way we will only get the code 
class CleanSQLParser(StrOutputParser):
    def parse(self, text: str) -> str:
        # Remove Markdown code fences like ```mysql ... ```
        if text.startswith("```mysql"):
            text = text.removeprefix("```mysql").strip()
        # If the LLM output ends with "```" it will remove it
        if text.endswith("```"):
            text = text.removesuffix("```").strip()
        # To clean any remaining white-spaces
        return text.strip()

#Main class that will contain all the required helping methods
class SQL_Model():
    def __init__(self):
        # Initializing the API key, LLM-Model, establishing connection with my database.
        self.YOUR_API_KEY = "YOUR_API_KEY"
        self.llm =  ChatGoogleGenerativeAI(
            # Using one of the GEMINI free models
            model="gemini-2.0-flash",
            google_api_key=self.YOUR_API_KEY,
            # Specifying the creativeness of the response
            # Keeping the temperature minimum to get simple and repeated response, with minimum experimentation
            temperature = 1
        )
        # writing a connection establishing string
        # Provide the password,host,domain and database name
        self.db_uri = "mysql+mysqlconnector://root:password!!!@localhost:3306/chinook"
        # Establishing Database Connection
        self.db = SQLDatabase.from_uri(self.db_uri)

    # Basic function to get the schema of the database
    # Please note that we have given a dummy argument (_) the reason will be clarified in main_aql_chain
    def get_schema(self,_):
        return self.db.get_table_info()

    # Basic function to run the received SQL response code
    def run_query(self,query):
        try:
            return self.db.run(query)
        except Exception as e:
            st.write("SQL Error:" ,str(e))
    
# Contructing class instance
SM = SQL_Model()

# Introductory prompt design that specifies the LLM model , about what we want from it.
# This is just a template design string
template = """
Base on the table schema below, write a MYSQL 5.7 query that would answer the user's question, avoid using reserved keywords:
{schema}

Question: {question}
SQL Query:
"""

# To build a proper prompt we need to invoke the template
# Now it can be fed to a LLM model
prompt = ChatPromptTemplate.from_template(template)

# It is a sequential chain that runs one function after another
# The output of one function is automatically fed to the next function/method
sql_chain = (
    # 1. It takes a input in our case {"question": user_question} and returns the dictionary as {"question": user_question, "schema" = database_schema}
    RunnablePassthrough.assign(schema = SM.get_schema)
    # 2. Now the dictionary from previous function is fed to prompt as arguments
    | prompt
    # 3. Now the prompt with it's arguments are fed to the LLM model
    | SM.llm
    # 4. The response given by the LLM-model is not in our usabe format so we pass the response string to get filtered
    | CleanSQLParser()
)  

# Now we create the main template design string
main_template = """
Based on the sql schema, question, sql query, and sql response, run the query and return the response in tabular form:
{schema}

Question: {question}
SQL Query: {query}
SQL Response: {response}

Answer
SQL Query:
Response:

"""
# Main prompt is created
main_prompt = ChatPromptTemplate.from_template(main_template)

# The main final chain is created
# While invoking, the main chain will only get the user_question as {"question": user_question}
main_sql_chain = (
    # 2. The output dict from previous runnable will be fed to all the functions in next runnable(both to SM.get_schema and lambda x)
    RunnablePassthrough.assign(schema = SM.get_schema, ### The reason for dummy argument is that the runnable will pass the dict even if we don't need it to
            response = lambda x:SM.run_query(x["query"]) # The function will find the SQL Code and run it and feed it to response
    )
    # 3. The output of the runnable consist of a dictionary with keys as (question->query->schema->response) and will be fed to prompt
    | main_prompt
    # 4. The prompt along with it's parameters are send to LLM-model
    | SM.llm
    # 5. The LLM response is formatted 
    | StrOutputParser()
)


mermaid_template = """
Based on the SQL Code given below , write a Mermaid code to form a grapg explaining the working to the code.
The syntax does not accept brackets of any kind in the label.
SQL Query: {query}

Answer
Mermaid(10.2.4) Code:

"""
mermaid_prompt = ChatPromptTemplate.from_template(mermaid_template)
 
mermaid_chain = (
    mermaid_prompt
    |SM.llm
    |StrOutputParser()
    
)

main_chain = (
    # 1. RunnablePassThrough will take {"question" : user_question} and return {"question" : user_question, "query" : sql_code}
    RunnablePassthrough.assign(query=sql_chain)
    |RunnableParallel(
        mermaid = mermaid_chain,
        response = main_sql_chain
    )
)
# We are using Streamlit to create an UI
st.title("SQL_LLM")
st.write("A database schema has been uploaded to the LLM")
st.write("Write any question in natural language")
question = st.text_input("Ask any question regarding database:")
if question:
    with st.spinner("Generating response..."):
        response = main_chain.invoke({"question": question})
        st.write(response["response"])
        st.sidebar.write(response["mermaid"])
    
