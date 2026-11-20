import httpx
import asyncio

API_URL = "http://127.0.0.1:8000"

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
    },
    {
        "title": "Reinforcement Learning",
        "content": "Reinforcement Learning is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Supervised Learning",
        "content": "Supervised Learning is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Unsupervised Learning",
        "content": "Unsupervised Learning is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Transfer Learning",
        "content": "Transfer Learning is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Federated Learning",
        "content": "Federated Learning is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Meta-Learning",
        "content": "Meta-Learning is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Generative Adversarial Networks",
        "content": "Generative Adversarial Networks is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Diffusion Models",
        "content": "Diffusion Models is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Transformer Architecture",
        "content": "Transformer Architecture is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "BERT Model",
        "content": "BERT Model is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "GPT Models",
        "content": "GPT Models is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Large Language Models",
        "content": "Large Language Models is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Foundation Models",
        "content": "Foundation Models is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Graph Neural Networks",
        "content": "Graph Neural Networks is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Convolutional Neural Networks",
        "content": "Convolutional Neural Networks is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Recurrent Neural Networks",
        "content": "Recurrent Neural Networks is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "LSTM Networks",
        "content": "LSTM Networks is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Attention Mechanisms",
        "content": "Attention Mechanisms is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Multi-Modal Learning",
        "content": "Multi-Modal Learning is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Self-Supervised Learning",
        "content": "Self-Supervised Learning is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Few-Shot Learning",
        "content": "Few-Shot Learning is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Zero-Shot Learning",
        "content": "Zero-Shot Learning is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Neural Architecture Search",
        "content": "Neural Architecture Search is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "AutoML",
        "content": "AutoML is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Model Compression",
        "content": "Model Compression is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Knowledge Distillation",
        "content": "Knowledge Distillation is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Ensemble Methods",
        "content": "Ensemble Methods is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Random Forests",
        "content": "Random Forests is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Gradient Boosting",
        "content": "Gradient Boosting is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Bagging Methods",
        "content": "Bagging Methods is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Support Vector Machines",
        "content": "Support Vector Machines is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "K-Nearest Neighbors",
        "content": "K-Nearest Neighbors is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Naive Bayes Classification",
        "content": "Naive Bayes Classification is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Decision Tree Learning",
        "content": "Decision Tree Learning is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Cross-Validation Techniques",
        "content": "Cross-Validation Techniques is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Feature Engineering",
        "content": "Feature Engineering is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Principal Component Analysis",
        "content": "Principal Component Analysis is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "t-SNE Visualization",
        "content": "t-SNE Visualization is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Clustering Algorithms",
        "content": "Clustering Algorithms is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Anomaly Detection",
        "content": "Anomaly Detection is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Natural Language Generation",
        "content": "Natural Language Generation is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Machine Translation",
        "content": "Machine Translation is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Object Detection",
        "content": "Object Detection is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Image Segmentation",
        "content": "Image Segmentation is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Speech Recognition",
        "content": "Speech Recognition is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Recommender Systems",
        "content": "Recommender Systems is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "React Framework",
        "content": "React Framework is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Vue.js Framework",
        "content": "Vue.js Framework is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Angular Platform",
        "content": "Angular Platform is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Svelte Framework",
        "content": "Svelte Framework is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Next.js Framework",
        "content": "Next.js Framework is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Nuxt.js Framework",
        "content": "Nuxt.js Framework is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Django Framework",
        "content": "Django Framework is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Flask Framework",
        "content": "Flask Framework is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "FastAPI Framework",
        "content": "FastAPI Framework is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Express.js",
        "content": "Express.js is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Tailwind CSS",
        "content": "Tailwind CSS is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Bootstrap CSS",
        "content": "Bootstrap CSS is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Responsive Web Design",
        "content": "Responsive Web Design is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Progressive Web Apps",
        "content": "Progressive Web Apps is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "GraphQL",
        "content": "GraphQL is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "RESTful APIs",
        "content": "RESTful APIs is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "WebSockets",
        "content": "WebSockets is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Server-Side Rendering",
        "content": "Server-Side Rendering is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Static Site Generation",
        "content": "Static Site Generation is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "WebAssembly",
        "content": "WebAssembly is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Three.js Graphics",
        "content": "Three.js Graphics is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "D3.js Visualization",
        "content": "D3.js Visualization is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "OAuth 2.0",
        "content": "OAuth 2.0 is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "JWT Authentication",
        "content": "JWT Authentication is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "CORS Policy",
        "content": "CORS Policy is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "WebRTC",
        "content": "WebRTC is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "CSS Grid Layout",
        "content": "CSS Grid Layout is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "CSS Flexbox",
        "content": "CSS Flexbox is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "CSS Animations",
        "content": "CSS Animations is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "TypeScript Language",
        "content": "TypeScript Language is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Node.js Runtime",
        "content": "Node.js Runtime is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Python Web Development",
        "content": "Python Web Development is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Java Spring Boot",
        "content": "Java Spring Boot is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Go Web Framework",
        "content": "Go Web Framework is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Ruby on Rails",
        "content": "Ruby on Rails is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Docker Containers",
        "content": "Docker Containers is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Kubernetes Orchestration",
        "content": "Kubernetes Orchestration is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "CI/CD Systems",
        "content": "CI/CD Systems is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Microservices Architecture",
        "content": "Microservices Architecture is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Serverless Computing",
        "content": "Serverless Computing is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "API Gateway",
        "content": "API Gateway is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Message Queues",
        "content": "Message Queues is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Apache Kafka Streaming",
        "content": "Apache Kafka Streaming is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Redis Caching",
        "content": "Redis Caching is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "PostgreSQL",
        "content": "PostgreSQL is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "MongoDB Database",
        "content": "MongoDB Database is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Elasticsearch Search",
        "content": "Elasticsearch Search is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "GitOps Workflow",
        "content": "GitOps Workflow is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Terraform",
        "content": "Terraform is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Ansible Automation",
        "content": "Ansible Automation is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Data Mining",
        "content": "Data Mining is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Data Warehouse Systems",
        "content": "Data Warehouse Systems is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "ETL Pipelines",
        "content": "ETL Pipelines is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Data Lake Architecture",
        "content": "Data Lake Architecture is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Business Intelligence",
        "content": "Business Intelligence is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Statistical Analysis",
        "content": "Statistical Analysis is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "A/B Testing",
        "content": "A/B Testing is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Regression Analysis",
        "content": "Regression Analysis is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Time Series Forecasting",
        "content": "Time Series Forecasting is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Collaborative Filtering",
        "content": "Collaborative Filtering is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Content-Based Systems",
        "content": "Content-Based Systems is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Text Mining",
        "content": "Text Mining is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Sentiment Analysis",
        "content": "Sentiment Analysis is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Named Entity Recognition",
        "content": "Named Entity Recognition is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Word Embeddings",
        "content": "Word Embeddings is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "TF-IDF",
        "content": "TF-IDF is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Information Retrieval",
        "content": "Information Retrieval is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Search Engines",
        "content": "Search Engines is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Web Scraping",
        "content": "Web Scraping is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Data Governance",
        "content": "Data Governance is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Data Quality Management",
        "content": "Data Quality Management is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Data Mesh",
        "content": "Data Mesh is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Data Lineage Tracking",
        "content": "Data Lineage Tracking is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Real-Time Analytics",
        "content": "Real-Time Analytics is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Stream Processing",
        "content": "Stream Processing is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Batch Processing",
        "content": "Batch Processing is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Apache Spark",
        "content": "Apache Spark is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Hadoop Ecosystem",
        "content": "Hadoop Ecosystem is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Feature Store",
        "content": "Feature Store is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Model Monitoring",
        "content": "Model Monitoring is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Data Drift Detection",
        "content": "Data Drift Detection is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Predictive Analytics",
        "content": "Predictive Analytics is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Exploratory Data Analysis",
        "content": "Exploratory Data Analysis is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Load Balancing",
        "content": "Load Balancing is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Network Security",
        "content": "Network Security is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Cloud Computing",
        "content": "Cloud Computing is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Edge Computing",
        "content": "Edge Computing is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "5G Networks",
        "content": "5G Networks is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "VPN Technology",
        "content": "VPN Technology is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "DNS Infrastructure",
        "content": "DNS Infrastructure is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "CDN Networks",
        "content": "CDN Networks is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Infrastructure as Code",
        "content": "Infrastructure as Code is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Continuous Integration",
        "content": "Continuous Integration is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Continuous Deployment",
        "content": "Continuous Deployment is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Observability",
        "content": "Observability is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Distributed Tracing",
        "content": "Distributed Tracing is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Log Aggregation",
        "content": "Log Aggregation is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Incident Response",
        "content": "Incident Response is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Robot Operating System",
        "content": "Robot Operating System is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Autonomous Vehicles",
        "content": "Autonomous Vehicles is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Computer Graphics",
        "content": "Computer Graphics is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Game Development",
        "content": "Game Development is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Computer Networks",
        "content": "Computer Networks is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
    {
        "title": "Compiler Design",
        "content": "Compiler Design is an important area of study and practice. It involves fundamental concepts, practical methodologies, and real-world applications that are essential in modern technology and research."
    },
]


async def seed():
    print("Seeding database with sample documents...")
    async with httpx.AsyncClient() as client:
        # Check if server is running
        try:
            health = await client.get(f"{API_URL}/health")
            if health.status_code != 200:
                print("Server is not healthy. Please run 'python run.py' first.")
                return
        except Exception as e:
            print(f"Could not connect to server at {API_URL}. Please run 'python run.py' first.")
            return

        for doc in SAMPLE_DOCS:
            try:
                print(f"Adding: {doc['title']}")
                response = await client.post(f"{API_URL}/documents", json=doc)
                if response.status_code == 200:
                    print(f"  Success: ID {response.json()['id']}")
                else:
                    print(f"  Failed: {response.text}")
            except Exception as e:
                print(f"  Error: {e}")
                
        print("\nSeeding complete!")

if __name__ == "__main__":
    asyncio.run(seed())
