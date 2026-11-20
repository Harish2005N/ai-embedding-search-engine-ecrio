#!/usr/bin/env python
"""
Startup script for Render deployment.
Checks if FAISS index exists, if not, seeds with sample documents.
"""
import os
import sys
import asyncio
import logging

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sample documents from seed_data.py
SAMPLE_DOCS = [
    {
        "title": "Artificial Intelligence",
        "content": "Artificial intelligence (AI) is the simulation of human intelligence processes by machines, especially computer systems. These processes include learning, reasoning, and self-correction."
    },
    {
        "title": "Machine Learning",
        "content": "Machine learning is a subset of AI that provides systems the ability to automatically learn and improve from experience without being explicitly programmed. It focuses on the development of computer programs that can access data and use it to learn for themselves."
    },
    {
        "title": "Deep Learning",
        "content": "Deep learning is part of a broader family of machine learning methods based on artificial neural networks with representation learning. It relies on multiple layers to progressively extract higher-level features from the raw input."
    },
    {
        "title": "Natural Language Processing",
        "content": "Natural language processing (NLP) is a subfield of linguistics, computer science, and artificial intelligence concerned with the interactions between computers and human language, in particular how to program computers to process and analyze large amounts of natural language data."
    },
    {
        "title": "Computer Vision",
        "content": "Computer vision is an interdisciplinary scientific field that deals with how computers can gain high-level understanding from digital images or videos. It seeks to understand and automate tasks that the human visual system can do."
    },
    {
        "title": "Data Science",
        "content": "Data science is an interdisciplinary field that uses scientific methods, processes, algorithms and systems to extract knowledge and insights from noisy, structured and unstructured data, and apply knowledge and actionable insights from data across a broad range of application domains."
    },
    {
        "title": "Cloud Computing",
        "content": "Cloud computing is the on-demand availability of computer system resources, especially data storage and computing power, without direct active management by the user. Large clouds often have functions distributed over multiple locations, each location being a data center."
    },
    {
        "title": "Cybersecurity",
        "content": "Computer security, cybersecurity or information technology security is the protection of computer systems and networks from information disclosure, theft of or damage to their hardware, software, or electronic data, as well as from the disruption or misdirection of the services they provide."
    },
    {
        "title": "Databases",
        "content": "A database is an organized collection of data, generally stored and accessed electronically from a computer system. Where databases are more complex they are often developed using formal design and modeling techniques."
    },
    {
        "title": "Python Programming",
        "content": "Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation. Python is dynamically-typed and garbage-collected."
    },
    {
        "title": "Quantum Computing",
        "content": "Quantum computing is a rapidly-emerging technology that harnesses the laws of quantum mechanics to solve problems too complex for classical computers. It relies on quantum bits or qubits."
    },
    {
        "title": "Space Exploration",
        "content": "Space exploration is the use of astronomy and space technology to explore outer space. While the exploration of space is carried out mainly by astronomers with telescopes, its physical exploration is conducted both by uncrewed robotic space probes and human spaceflight."
    },
    {
        "title": "Internet of Things (IoT)",
        "content": "The Internet of Things describes the network of physical objects embedded with sensors, software, and other technologies for the purpose of connecting and exchanging data with other devices and systems over the internet."
    },
    {
        "title": "Renewable Energy",
        "content": "Renewable energy is energy derived from natural sources that are replenished at a higher rate than they are consumed. Sunlight and wind, for example, are such sources that are constantly being replenished."
    },
    {
        "title": "Robotics",
        "content": "Robotics is an interdisciplinary branch of computer science and engineering. Robotics involves design, construction, operation, and use of robots. The goal of robotics is to design machines that can help and assist humans."
    },
    {
        "title": "Ancient Egypt",
        "content": "Ancient Egypt was a civilization of ancient North Africa, concentrated along the lower reaches of the Nile River. It is famous for its majestic pyramids, pharaohs, and hieroglyphic writing system."
    },
    {
        "title": "Human Anatomy",
        "content": "Human anatomy is the scientific study of the body's structures. Some of these structures are very small and can only be observed and analyzed with the assistance of a microscope, while others are large enough to easily see."
    },
    {
        "title": "Oceanography",
        "content": "Oceanography is the scientific study of the ocean. It is an important Earth science, which covers a wide range of topics, including ecosystem dynamics, ocean currents, waves, and geophysical fluid dynamics."
    },
    {
        "title": "Climate Change",
        "content": "Climate change refers to long-term shifts in temperatures and weather patterns. These shifts may be natural, but since the 1800s, human activities have been the main driver of climate change, primarily due to the burning of fossil fuels."
    },
    {
        "title": "The Renaissance",
        "content": "The Renaissance was a fervent period of European cultural, artistic, political and economic 'rebirth' following the Middle Ages. Generally described as taking place from the 14th century to the 17th century, the Renaissance promoted the rediscovery of classical philosophy, literature, and art."
    },
    {
        "title": "Black Holes",
        "content": "A black hole is a region of spacetime where gravity is so strong that nothing, not even light or other electromagnetic waves, has enough energy to escape it. The theory of general relativity predicts that a sufficiently compact mass can deform spacetime to form a black hole."
    },
    {
        "title": "Microbiology",
        "content": "Microbiology is the study of all living organisms that are too small to be visible with the naked eye. This includes bacteria, archaea, viruses, fungi, prions, protozoa and algae, collectively known as 'microbes'."
    }
]

async def seed_data():
    """Seed the database with sample documents."""
    from app.services.document_service import document_service
    from app.services.embedding_service import generate_embeddings
    from app.services.faiss_service import faiss_service
    
    logger.info("Seeding database with sample documents...")
    
    # Add documents to document store
    doc_ids = []
    texts = []
    
    for doc in SAMPLE_DOCS:
        doc_id = document_service.add_document(doc["title"], doc["content"])
        doc_ids.append(doc_id)
        texts.append(f"{doc['title']}: {doc['content']}")
    
    # Generate embeddings
    logger.info(f"Generating embeddings for {len(texts)} documents...")
    embeddings = generate_embeddings(texts)
    
    # Add to FAISS index
    faiss_service.add_embeddings(doc_ids, embeddings)
    
    logger.info(f"Seeded {len(doc_ids)} documents successfully!")

def main():
    """Check if index exists, seed if not."""
    data_dir = "data"
    index_file = os.path.join(data_dir, "faiss.index")
    
    os.makedirs(data_dir, exist_ok=True)
    
    if os.path.exists(index_file):
        logger.info("FAISS index already exists, skipping seed")
        return
    
    logger.info("No FAISS index found, seeding data...")
    asyncio.run(seed_data())

if __name__ == "__main__":
    main()