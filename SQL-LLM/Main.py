from langchain_core.prompts import ChatPromptTemplate 
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
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
            temperature = 0.1
        )
        # writing a connection establishing string
        # Provide the password,host,domain and database name
        self.db_uri = "mysql+mysqlconnector://root:PASSWORD@HOST:DOMAIN/DATABASE"
        # Establishing Database Connection
        self.db = SQLDatabase.from_uri(self.db_uri)

    # Basic function to get the schema of the database
    def get_schema(self,_):
        return self.db.get_table_info()

    # Basic function to run the received SQL response code
    def run_query(self,query):
        try:
            return self.db.run(query)
        except Exception as e:
            st.write("SQL Error:" ,str(e)
    

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

main_prompt = ChatPromptTemplate.from_template(main_template)

main_sql_chain = (
    RunnablePassthrough.assign(query=sql_chain)
    | RunnablePassthrough.assign(schema = SM.get_schema,
            response = lambda x:SM.run_query(x["query"])
    )
    | main_prompt
    | SM.llm
    | StrOutputParser()
)

st.title("SQL_LLM")
st.write("A database schema has been uploaded to the LLM")
st.write("Write any question in natural language")
question = st.text_input("Ask any question regarding database:")
if question:
    with st.spinner("Generating response..."):
        response = main_sql_chain.invoke({"question": question})

    st.write(response)
    
