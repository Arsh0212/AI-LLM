from stocks import Database_Management 
from langchain.text_splitter import CharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chains.question_answering.chain import load_qa_chain
from langchain_community.vectorstores import FAISS

class Para_Processing:

    def __init__(self):
        self.YOUR_API_KEY = "YOUR_API_KEY"
        self.dm = Database_Management()
        self.chunks=""
        self.embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=self.YOUR_API_KEY)
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=self.YOUR_API_KEY
        )

    def splitter_embedding(self):
        text_splitter = CharacterTextSplitter(
            separator = " ",
            chunk_size = 600,
            chunk_overlap = 50,
            length_function = len
        )
        print("Text_splitter Created")

        Query = input("Write any keyword you want to search about:")
        result = self.dm.select_data(Query)
        info = " ".join(res[0].strip(" ") for res in result)
        print("DataBase Searched")

        self.chunks = text_splitter.split_text(info)
        print("Text Splitted")

        # embeddings = OpenAIEmbeddings()
        # self.knowledge_base = FAISS.from_texts(chunks,embeddings)


    def interaction(self):
        
        knowledge_base = FAISS.from_texts(self.chunks, self.embedding)
        user_question = input("Type your question:")
        # user_question = "What is Vingroup and how does it operate?"
        docs = knowledge_base.similarity_search(user_question)
        chain = load_qa_chain(self.llm,chain_type="stuff")
        response = chain.invoke({
            "input_documents": docs,
            "question": user_question
        })

        print(response["output_text"])

print("Going into Class")
Para = Para_Processing()
print("Created Instance")
print("Splitting Data")
Para.splitter_embedding()
print("Performing AI")
Para.interaction()
