import chromadb
from chromadb.utils import embedding_functions
import requests
from bs4 import BeautifulSoup
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

class Knowledge:
    def __init__(self):
        """Initialize ChromaDB, scrape & store scriptures, and load Llama-2"""
        # Setup ChromaDB
        self.chroma_client = chromadb.PersistentClient(path="./tejas_ai_knowledge_db")
        self.scripture_collection = self.chroma_client.get_or_create_collection(
            name="hindu_knowledge",
            embedding_function=embedding_functions.DefaultEmbeddingFunction()
        )

        # Load Llama-2
        MODEL_NAME = "meta-llama/Llama-2-7b-chat-hf"
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float16, device_map="auto")
        self.llama_pipeline = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer, max_length=1024)

        # Scrape and store data
        self.resources = {
    # Aryan Invasion Theory
    "Debunking the Aryan Invasion Myth": "https://www.indictoday.com/aryan-invasion-myth-debunked/",
    "Max Muller’s Distortion of Vedic History": "https://www.sanskritimagazine.com/history/max-muller-fabrication-vedic-history/",

    # Temple Destruction Whitewashing
    "Islamic Invasions Whitewashed in Indian Textbooks": "https://www.opindia.com/2020/06/history-whitewashing-islamic-invasions/",
    "How Left Historians Hid Temple Destruction": "https://www.firstpost.com/long-reads/leftist-historians-denial-hindu-temple-destruction/",
    
    # British & Western Manipulation
    "How British Created the Caste System": "https://www.indictoday.com/history/how-the-british-created-the-caste-system/",
    "Macaulay’s Education System & Destruction of Gurukuls": "https://www.sanskritimagazine.com/history/macaulay-education-destroyed-indian-culture/",
    
    # Communist & Secular Attacks
    "Leftist Control Over Indian Academia": "https://www.opindia.com/2021/03/left-academic-mafia-india/",
    "Hinduphobia in Western Media": "https://www.indiafacts.org/hinduphobia-western-media/",
    
    # Propaganda in Bollywood
    "How Bollywood Defames Hindus": "https://www.opindia.com/2022/01/bollywood-anti-hindu-movies-list/",
    "Why Hindu Kings Are Villains in Bollywood": "https://www.sanskritimagazine.com/history/how-bollywood-distorts-history/",

    # Islamic Invasions & Temple Destruction
    "Hindu Temples: What Happened to Them": "https://www.sanskritimagazine.com/history/hindu-temples-what-happened-to-them/",
    "Destruction of Somnath Temple": "https://www.sanskritimagazine.com/history/destruction-of-somnath-temple/",
    "Kashi Vishwanath Destruction": "https://www.sanskritimagazine.com/history/kashi-vishwanath-temple-history/",
    "Martyrdom of Raja Dahir": "https://www.sanskritimagazine.com/history/raja-dahir-last-hindu-king-sindh/",
    
    # British & Portuguese Colonization
    "British Colonial Destruction of Indian Education": "https://www.sanskritimagazine.com/history/british-colonial-destruction-indian-education/",
    "Goa Inquisition by Portuguese": "https://www.sanskritimagazine.com/history/goa-inquisition-horrors-portuguese-rule/",
    "Destruction of Nalanda": "https://www.sanskritimagazine.com/history/destruction-of-nalanda-university/",

    # Rajput & Maratha Warriors
    "Prithviraj Chauhan": "https://www.rajputcommunity.in/history/prithviraj-chauhan",
    "Maharana Pratap": "https://www.rajputcommunity.in/history/maharana-pratap",
    "Chhatrapati Shivaji Maharaj": "https://www.historyfiles.co.uk/KingListFarEast/IndiaShivaji.htm",
    "Baji Rao Peshwa": "https://www.historyfiles.co.uk/KingListFarEast/IndiaBajiRao.htm",

    # Battles & Resistance
    "Battle of Tarain": "https://www.historyfiles.co.uk/KingListFarEast/IndiaBattleTarain.htm",
    "Battle of Haldighati": "https://www.historyfiles.co.uk/KingListFarEast/IndiaBattleHaldighati.htm",
    "Battle of Sinhagad": "https://www.historyfiles.co.uk/KingListFarEast/IndiaBattleSinhagad.htm",
    "Battle of Panipat": "https://www.historyfiles.co.uk/KingListFarEast/IndiaBattlePanipat.htm",

    # 🏥 Ayurveda (Medicine)
    "Charaka Samhita": "https://www.wisdomlib.org/hinduism/book/charaka-samhita",
    "Sushruta Samhita": "https://www.wisdomlib.org/hinduism/book/sushruta-samhita",
    "Ashtanga Hridayam": "https://www.wisdomlib.org/hinduism/book/ashtanga-hridaya",

    # 🔭 Astronomy & Jyotish Shastra
    "Surya Siddhanta": "https://www.wisdomlib.org/astronomy/book/surya-siddhanta",
    "Brihat Samhita": "https://www.wisdomlib.org/hinduism/book/brihat-samhita",
    "Laghu Parashari": "https://www.wisdomlib.org/astrology/book/laghu-parashari",
    "Vedanga Jyotisha": "https://www.sacred-texts.com/hin/jyotisha.htm",

    # ⚗️ Rasashastra (Alchemy & Metallurgy)
    "Rasaratna Samuchchaya": "https://www.wisdomlib.org/hinduism/book/rasaratna-samuchchaya",
    "Rasendrasarasangraha": "https://www.wisdomlib.org/hinduism/book/rasendrasarasangraha",
    "Nagarjuna’s Rasashastra": "https://www.wisdomlib.org/hinduism/book/nagarjuna-rasashastra",
    
    # ➗ Mathematics
    "Baudhayana Sulba Sutra": "https://www.wisdomlib.org/hinduism/book/baudhayana-sulba-sutra",
    "Aryabhatiya (Aryabhatta)": "https://www.wisdomlib.org/hinduism/book/aryabhatiya",
    "Brahmasphutasiddhanta (Brahmagupta)": "https://www.wisdomlib.org/hinduism/book/brahmasphutasiddhanta",
    "Leelavati (Bhaskara)": "https://www.wisdomlib.org/hinduism/book/leelavati",

    # 🚀 Vimanas & Aviation
    "Vaimanika Shastra": "https://www.wisdomlib.org/hinduism/book/vaimanika-shastra",
    "Yantra Sarvasva (Bharadwaja)": "https://www.wisdomlib.org/hinduism/book/yantra-sarvasva",
    "Shakuna Vimana (Ancient Aircraft)": "https://www.wisdomlib.org/hinduism/book/shakuna-vimana",
    
    # 🌍 Cosmology & Time Cycles
    "Vishnu Purana - Cosmic Cycles": "https://www.wisdomlib.org/hinduism/book/vishnu-purana",
    "Bhagavata Purana - Time Theory": "https://www.wisdomlib.org/hinduism/book/bhagavata-purana",
    "Brahmanda Purana - Universe Creation": "https://www.wisdomlib.org/hinduism/book/brahmanda-purana",

    # 🏛 Vedas
    "Rigveda": "https://vedicheritage.com/rigveda/",
    "Yajurveda": "https://vedicheritage.com/yajurveda/",
    "Samaveda": "https://vedicheritage.com/samaveda/",
    "Atharvaveda": "https://vedicheritage.com/atharvaveda/",

    # 📜 Brahmanas (Commentaries on Vedas)
    "Aitareya Brahmana": "https://www.sacred-texts.com/hin/aitbr/index.htm",
    "Shatapatha Brahmana": "https://www.sacred-texts.com/hin/sbr/index.htm",

    # 📖 Aranyakas (Forest Treatises)
    "Aitareya Aranyaka": "https://www.sacred-texts.com/hin/aiar/index.htm",
    "Brihadaranyaka Upanishad": "https://www.sacred-texts.com/hin/brih/index.htm",

    # 🔹 Upanishads (Expanded)
    "Isha Upanishad": "https://www.upanishads.org/isha-upanishad",
    "Kena Upanishad": "https://www.upanishads.org/kena-upanishad",
    "Katha Upanishad": "https://www.upanishads.org/katha-upanishad",
    "Mundaka Upanishad": "https://www.upanishads.org/mundaka-upanishad",
    "Mandukya Upanishad": "https://www.upanishads.org/mandukya-upanishad",
    "Taittiriya Upanishad": "https://www.upanishads.org/taittiriya-upanishad",
    "Chandogya Upanishad": "https://www.upanishads.org/chandogya-upanishad",
    "Prashna Upanishad": "https://www.upanishads.org/prashna-upanishad",
    
    # 📜 Vedangas (Ancillary Texts)
    "Shiksha (Phonetics)": "https://www.sanskritdocuments.org/vedanga/shiksha/",
    "Chandas (Meter)": "https://www.sanskritdocuments.org/vedanga/chandas/",
    "Vyakarana (Grammar - Panini)": "https://www.sanskritdocuments.org/vedanga/astadhyayi/",
    "Nirukta (Etymology)": "https://www.sanskritdocuments.org/vedanga/nirukta/",
    "Jyotisha (Astronomy)": "https://www.sacred-texts.com/hin/suryasiddhanta.htm",
    "Kalpa (Rituals)": "https://www.sanskritdocuments.org/vedanga/kalpasutra/",

    # 📜 Smritis & Dharmashastras (Expanded)
    "Manusmriti": "https://www.sacred-texts.com/hin/manu.htm",
    "Yajnavalkya Smriti": "https://www.sacred-texts.com/hin/yajnavalkya-smriti.htm",
    "Parashara Smriti": "https://www.sacred-texts.com/hin/parashara-smriti.htm",
    "Gautama Smriti": "https://www.sacred-texts.com/hin/gautama.htm",
    "Baudhayana Smriti": "https://www.sacred-texts.com/hin/baudh.htm",
    "Apastamba Smriti": "https://www.sacred-texts.com/hin/apastamba.htm",

    # 🔹 Hindu Philosophies
    "Advaita Vedanta (Shankaracharya)": "https://www.sacred-texts.com/hin/vedanta/index.htm",
    "Dvaita Vedanta (Madhvacharya)": "https://www.sacred-texts.com/hin/dvaita.htm",
    "Vishishtadvaita (Ramanujacharya)": "https://www.sacred-texts.com/hin/ramanuja.htm",
    "Nyaya (Logic)": "https://www.sacred-texts.com/hin/nyaya.htm",
    "Vaisheshika (Atomic Theory)": "https://www.sacred-texts.com/hin/vaisheshika.htm",
    "Samkhya (Dualism)": "https://www.sacred-texts.com/hin/samkhya.htm",
    "Mimamsa (Ritual Interpretation)": "https://www.sacred-texts.com/hin/mimamsa.htm",

    # 📜 Itihasas (Epics)
    "Ramayana": "https://www.valmikiramayan.net/",
    "Mahabharata": "https://www.sacred-texts.com/hin/maha/index.htm",
    "Bhagavad Gita": "https://www.bhagavad-gita.org/",

    # 📚 Puranas (Expanded)
    "Vishnu Purana": "https://www.sacred-texts.com/hin/vp/index.htm",
    "Shiva Purana": "https://www.sacred-texts.com/hin/sp/index.htm",
    "Bhagavata Purana": "https://www.sacred-texts.com/hin/srimad/index.htm",
    "Devi Bhagavata Purana": "https://www.sacred-texts.com/hin/db/index.htm",
    "Agni Purana": "https://www.sacred-texts.com/hin/agni/index.htm",
    "Brahmanda Purana": "https://www.sacred-texts.com/hin/brahmanda/index.htm",

    # 📖 Other Hindu Texts
    "Arthashastra (Chanakya)": "https://www.sacred-texts.com/hin/kautil/index.htm",
    "Yoga Sutras of Patanjali": "https://www.sacred-texts.com/hin/yogasutras.htm",
    "Narada Bhakti Sutra": "https://www.sacred-texts.com/hin/nbhakti.htm",
    "Brahma Sutras": "https://www.sacred-texts.com/hin/brahma.htm"
}
        self.scrape_and_store_resources()

    def scrape_and_store_resources(self):
        """Scrape scripture texts from resources and store in ChromaDB"""
        for category, url in self.resources.items():
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            texts = soup.find_all("p")  # Extract paragraph texts

            for i, text in enumerate(texts):
                self.scripture_collection.add(
                    ids=[f"{category}_{i+1}"],
                    metadatas=[{"category": category}],
                    documents=[text.text.strip()]
                )
        print("✅ Hindu scriptures and history stored successfully!")

    def query_chromadb(self, question):
        """Fetch relevant scripture texts from ChromaDB"""
        results = self.scripture_collection.query(query_texts=[question], n_results=5)
        retrieved_texts = results["documents"]
        return " ".join(retrieved_texts) if retrieved_texts else "No relevant scriptures found."

    def generate_llama_response(self, question, context_text):
        """Generate AI response using Llama-2"""
        prompt = f"""
        You are Tejas AI, an expert in Hindu scriptures, history, and philosophy.
        Below is a question followed by relevant texts. Generate a concise response.

        Question: {question}

        Relevant Texts:
        {context_text}

        Provide a **clear and insightful** answer.
        """
        response = self.llama_pipeline(prompt)[0]["generated_text"]
        return response

    def combine_responses(self, chroma_response, llama_response):
        """Merge ChromaDB response and Llama-2 response into one meaningful answer"""
        prompt = f"""
        Given the following two responses, generate a **coherent and meaningful** answer:

        📖 **Response from Scriptures (ChromaDB):**  
        {chroma_response}

        🧠 **Response from AI (Llama-2):**  
        {llama_response}

        Create a **single, well-structured, and insightful** answer.
        """
        final_response = self.llama_pipeline(prompt)[0]["generated_text"]
        return final_response

    def query(self, question):
        """Main function to get a combined response from ChromaDB and Llama-2"""
        chroma_response = self.query_chromadb(question)
        llama_response = self.generate_llama_response(question, chroma_response)
        final_response = self.combine_responses(chroma_response, llama_response)
        return final_response