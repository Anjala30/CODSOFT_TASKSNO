import streamlit as st
import re



# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Student Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* Main application background */
    .stApp {
        background: linear-gradient(135deg, #f5f7ff 0%, #eef2ff 100%);
    }

    /* Main content width */
    .block-container {
        max-width: 950px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Header */
    .main-header {
        text-align: center;
        padding: 25px 20px;
        border-radius: 22px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.25);
        margin-bottom: 25px;
    }

    .main-header h1 {
        color: white;
        font-size: 2.4rem;
        margin-bottom: 8px;
        font-weight: 700;
    }

    .main-header p {
        color: #f1f3ff;
        font-size: 1rem;
        margin: 0;
    }

    /* Section heading */
    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #343a70;
        margin-top: 20px;
        margin-bottom: 12px;
    }

    /* Quick question buttons */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: 1px solid #d8dcff;
        background-color: white;
        color: #4b4f8a;
        font-weight: 600;
        padding: 10px;
        transition: 0.2s;
    }

    .stButton > button:hover {
        border-color: #667eea;
        color: #667eea;
        background-color: #f5f6ff;
    }

    /* Chat input */
    .stChatInput {
        border-radius: 15px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #171a3a 0%, #242858 100%);
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Clear Chat button text visibility */
    section[data-testid="stSidebar"] .stButton > button,
    section[data-testid="stSidebar"] .stButton > button * {
        color: #4b4f8a !important;
        background-color: white !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover,
    section[data-testid="stSidebar"] .stButton > button:hover * {
        color: #667eea !important;
        background-color: #f5f6ff !important;
    }

    .sidebar-title {
        font-size: 1.35rem;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .sidebar-subtitle {
        font-size: 0.9rem;
        opacity: 0.8;
        margin-bottom: 25px;
    }

    .feature-card {
        background: rgba(255, 255, 255, 0.08);
        padding: 13px;
        border-radius: 12px;
        margin-bottom: 10px;
        border: 1px solid rgba(255, 255, 255, 0.12);
    }

    /* Status card */
    .status-card {
        background: rgba(46, 204, 113, 0.15);
        border: 1px solid rgba(46, 204, 113, 0.35);
        padding: 12px;
        border-radius: 12px;
        margin-top: 20px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #777;
        font-size: 0.85rem;
        margin-top: 30px;
        padding: 15px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">🤖 AI Student Assistant</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">Your smart study companion</div>',
        unsafe_allow_html=True
    )

    st.markdown("### ✨ Features")

    st.markdown("""
    <div class="feature-card">🧠 Rule-Based NLP</div>
    <div class="feature-card">💬 Interactive Chat</div>
    <div class="feature-card">⚡ Quick Questions</div>
    <div class="feature-card">📚 Student Assistance</div>
    <div class="feature-card">🌐 Pattern Matching & NLP</div>
    """, unsafe_allow_html=True)

    st.markdown("### 📌 Topics")

    st.write("🐍 Python")
    st.write("📊 Data Science")
    st.write("🤖 Machine Learning")
    st.write("💼 Internships")
    st.write("🧑‍💻 Projects")
    st.write("📚 Study Tips")
    st.write("🎓 Courses")

    st.markdown("""
    <div class="status-card">
        🟢 <b>System Status</b><br>
        Chatbot is ready!
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    if st.button("🧹 Clear Chat", use_container_width=True):

        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hello! 👋 I'm your AI Student Assistant. How can I help you today?"
            }
        ]

        st.rerun()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="main-header">
        <h1>🤖 AI Student Assistant</h1>
        <p>Your intelligent companion for learning, projects, internships and technology.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# INITIALIZE CHAT HISTORY
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! 👋 I'm your AI Student Assistant.\n\n"
                "I can answer common student questions using NLP and pattern matching. "
                "Ask me about Python, Data Science, Machine Learning, SQL, projects or study tips. 😊"
            )
        }
    ]


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):
    """Normalize user input for rule-based NLP matching."""
    text = text.lower()

    # Keep +, -, *, /, %, (, ) so simple arithmetic can be detected.
    text = re.sub(r"[^a-zA-Z0-9\s+\-*/().%]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


def contains_phrase(text, phrases):
    """Match complete words/phrases instead of unsafe substring matching."""
    for phrase in phrases:
        phrase = normalize_text(phrase)
        if re.search(r"\b" + re.escape(phrase) + r"\b", text):
            return True
    return False


def is_greeting(text):
    """Detect greetings without confusing words inside other words."""
    greeting_patterns = [
        r"^(hi|hello|hey|heyy|heyyy)$",
        r"^(good morning|good afternoon|good evening)$",
        r"^(hi|hello|hey|heyy)[, ]+(there|assistant|bot)$"
    ]
    return any(re.search(pattern, text) for pattern in greeting_patterns)


# ============================================================
# CHATBOT RESPONSE ENGINE
# ============================================================

def get_response(user_input):
    """Rule-based NLP response engine for CodSoft Task 1.

    Flow:
    Text Processing -> NLP / Pattern Matching -> Rule Engine -> Response
    """

    text = normalize_text(user_input)

    # ------------------------------------------------------------
    # SIMPLE CALCULATION
    # ------------------------------------------------------------
    # Supports both direct expressions and natural-language questions:
    #   2 + 5
    #   What is 2 + 5?
    #   Calculate 10 * 5
    #   100 / 4

    arithmetic_pattern = (
        r"(?<![a-zA-Z0-9])"
        r"(?:\d+(?:\.\d+)?\s*[+\-*/%]\s*)+"
        r"\d+(?:\.\d+)?"
        r"(?![a-zA-Z0-9])"
    )

    arithmetic_match = re.search(arithmetic_pattern, text)

    if arithmetic_match:
        expression = arithmetic_match.group(0).strip()

        try:
            result = eval(expression, {"__builtins__": {}}, {})
            return f"The answer is **{result}**. 🧮"
        except Exception:
            pass

    # ------------------------------------------------------------
    # RESPONSE STYLE
    # ------------------------------------------------------------
    is_brief = contains_phrase(text, [
        "in brief", "briefly", "short answer", "shortly",
        "keep it short", "very short", "one line", "one sentence"
    ])

    is_easy = contains_phrase(text, [
        "easy words", "simple words", "easy language",
        "explain simply", "simple explanation",
        "explain in simple words", "beginner friendly",
        "explain like a beginner"
    ])

    is_detailed = contains_phrase(text, [
        "in detail", "detailed", "deeply", "explain fully",
        "elaborate", "thoroughly", "full explanation"
    ])

    def format_answer(short, normal, easy=None, detailed=None):
        if is_brief:
            return short
        if is_detailed and detailed:
            return detailed
        if is_easy and easy:
            return easy
        return normal

    # ------------------------------------------------------------
    # GREETINGS / BASIC CONVERSATION
    # ------------------------------------------------------------
    if contains_phrase(text, ["how are you", "how r you", "how are u"]):
        return "I'm doing great and ready to help! 😊 What would you like to learn or work on?"

    if is_greeting(text):
        return "Hello! 👋 I'm your AI Student Assistant. How can I help you today?"

    if contains_phrase(text, ["thank you", "thanks", "thank u"]):
        return "You're welcome! 😊 I'm happy to help."

    if text in ["bye", "goodbye", "see you", "see ya"]:
        return "Goodbye! 👋 All the best with your studies and projects! 🚀"

    # ------------------------------------------------------------
    # HELP / CAPABILITIES
    # ------------------------------------------------------------
    # Keep this BEFORE the general "help me" pattern. Only trigger
    # when the user is actually asking about chatbot capabilities.
    if contains_phrase(text, [
        "what can you do",
        "how can you help",
        "your features",
        "what do you help with"
    ]) and not contains_phrase(text, [
        "python", "data science", "machine learning", "sql",
        "project", "internship", "recursion"
    ]):
        return (
            "I can help with Python, Data Science, Machine Learning, SQL, "
            "projects, internships, study tips, coding basics and common "
            "student questions. 😊"
        )

    # ------------------------------------------------------------
    # PYTHON
    # ------------------------------------------------------------
    if contains_phrase(text, [
        "python", "py programming", "python language",
        "pandas", "numpy", "matplotlib",
        "scikit learn", "scikit-learn", "sklearn"
    ]):

        # Python specifically in Machine Learning
        if contains_phrase(text, [
        "machine learning", "ml",
        "training data", "training dataset", "train data",
        "testing data", "testing dataset", "test data",
        "target variable", "target in machine learning", "target value"
    ]):
            return format_answer(
                "Python is widely used in Machine Learning because of its simple syntax and useful libraries.",
                "Python is widely used in Machine Learning for data preparation, model training, evaluation and visualization. Libraries such as Pandas, NumPy and Scikit-learn make these tasks easier.",
                "Python helps in Machine Learning by providing simple tools and libraries to prepare data, train models and make predictions.",
                "Python is commonly used throughout the Machine Learning workflow. Pandas and NumPy help prepare and process data, Scikit-learn provides Machine Learning algorithms, and visualization libraries help understand results. Python's readable syntax also makes experimentation and development easier."
            )

        # Python libraries
        if contains_phrase(text, [
            "python library", "python libraries",
            "libraries in python", "library in python",
            "python package", "python packages"
        ]):
            return format_answer(
                "Popular Python libraries include NumPy, Pandas and Scikit-learn.",
                "Popular Python libraries include NumPy for numerical work, Pandas for data analysis, Matplotlib for visualization and Scikit-learn for Machine Learning.",
                "Python libraries are ready-made collections of code. Pandas helps work with data, NumPy handles numerical operations, Matplotlib creates graphs, and Scikit-learn is used for Machine Learning.",
                "Some commonly used Python libraries are NumPy for numerical computing, Pandas for data manipulation and analysis, Matplotlib and Seaborn for visualization, Scikit-learn for Machine Learning, and TensorFlow/PyTorch for deep learning."
            )

        # Pandas
        if contains_phrase(text, [
            "pandas", "what is pandas", "pandas library",
            "python pandas", "use of pandas"
        ]):
            return format_answer(
                "Pandas is a Python library used for data analysis and data manipulation.",
                "Pandas is a popular Python library used for data analysis and manipulation. It provides useful structures such as Series and DataFrame for working with structured data.",
                "Pandas is a Python library that helps us work with and analyze data. It is commonly used to read, clean, filter and organize datasets.",
                "Pandas is a Python library designed for data manipulation and analysis. Its main data structures are Series and DataFrame. It is commonly used for reading datasets, cleaning missing values, filtering records, transforming data and performing exploratory data analysis."
            )

        # NumPy
        if contains_phrase(text, [
            "numpy", "what is numpy", "numpy library",
            "python numpy", "use of numpy"
        ]):
            return format_answer(
                "NumPy is a Python library used for numerical and mathematical operations.",
                "NumPy is a Python library used for numerical computing. It provides efficient arrays and functions for mathematical, statistical and scientific operations.",
                "NumPy helps Python programs work with numbers, arrays and mathematical calculations efficiently.",
                "NumPy is a fundamental Python library for numerical computing. It provides multidimensional arrays and a wide range of mathematical functions. It is widely used in Data Science, Machine Learning and scientific computing."
            )

        # Matplotlib
        if contains_phrase(text, [
            "matplotlib", "what is matplotlib",
            "matplotlib library", "python matplotlib",
            "use of matplotlib"
        ]):
            return format_answer(
                "Matplotlib is a Python library used for creating graphs and visualizations.",
                "Matplotlib is a Python visualization library used to create graphs, charts and plots from data.",
                "Matplotlib helps us create graphs and charts so we can understand data visually.",
                "Matplotlib is a widely used Python library for data visualization. It can create line charts, bar charts, histograms, scatter plots and many other types of graphs. It is commonly used during data analysis and exploratory data analysis."
            )

        # Scikit-learn
        if contains_phrase(text, [
            "scikit learn", "scikit-learn",
            "sklearn", "what is scikit learn",
            "what is scikit-learn", "scikit learn library",
            "python scikit learn"
        ]):
            return format_answer(
                "Scikit-learn is a Python library used for Machine Learning.",
                "Scikit-learn is a popular Python library that provides tools for Machine Learning, including classification, regression, clustering and model evaluation.",
                "Scikit-learn is a Python library that helps us build and test Machine Learning models.",
                "Scikit-learn is a widely used Python Machine Learning library. It provides algorithms and tools for classification, regression, clustering, preprocessing, model selection and evaluation."
            )

        # Python Data Types
        if contains_phrase(text, [
            "python data types",
            "data types in python",
            "types of data in python",
            "different data types in python",
            "different python data types",
            "what are python data types",
            "what are the data types in python",
            "what are the different data types in python"
        ]):
            return format_answer(
                "Common Python data types include int, float, str, bool, list, tuple, set and dict.",
                "Common Python data types include:\n\n• int – whole numbers\n• float – decimal numbers\n• str – text\n• bool – True or False\n• list – ordered, changeable collection\n• tuple – ordered, unchangeable collection\n• set – unordered collection of unique items\n• dict – key-value pairs",
                "Python has common data types such as int for whole numbers, float for decimals, str for text, bool for True or False, list, tuple, set and dict.",
                "Python provides built-in data types for storing different kinds of values. Common examples are int for whole numbers, float for decimal numbers, str for text, bool for True or False, list for ordered changeable collections, tuple for ordered unchangeable collections, set for unique items and dict for key-value pairs."
            )

        # Python list
        if contains_phrase(text, [
            "list in python", "python list",
            "what is a list"
        ]):
            return format_answer(
                "A list in Python is an ordered and changeable collection of items.",
                "A list in Python is an ordered, mutable collection that can store multiple values. Lists are created using square brackets, for example: [10, 20, 30].",
                "A Python list stores multiple items in one variable. For example: [10, 20, 30]. Lists can be changed after they are created.",
                "A list is a built-in Python data structure used to store an ordered collection of items. Lists can contain different data types and can be modified after creation. They are created using square brackets, such as [10, 20, 30]."
            )

        # Python dictionary
        if contains_phrase(text, [
            "dictionary in python", "python dictionary",
            "what is a dictionary"
        ]):
            return format_answer(
                "A dictionary in Python stores data as key-value pairs.",
                "A dictionary in Python is a mutable collection that stores data in key-value pairs. It is created using curly brackets, for example: {'name': 'Anjala'}.",
                "A Python dictionary stores information using a key and its value. For example, {'name': 'Anjala'} stores the value Anjala with the key name.",
                "A dictionary is a built-in Python data structure that stores data as key-value pairs. Each key is used to access its corresponding value. Dictionaries are written using curly brackets and are useful when data needs to be accessed using meaningful keys."
            )

        # Python function
        if contains_phrase(text, [
            "function in python", "python function",
            "what is a function", "functions in python",
            "define function"
        ]):
            return format_answer(
                "A function in Python is a reusable block of code that performs a specific task.",
                "A function in Python is a reusable block of code designed to perform a specific task. Functions are defined using the 'def' keyword.",
                "A function is a block of code that we can reuse whenever we need to perform a particular task.",
                "A function in Python is a reusable block of code that performs a specific task. It is defined using the 'def' keyword and can accept parameters and return a result. Functions help make programs organized, reusable and easier to maintain."
            )

        # Why Python is popular
        if contains_phrase(text, [
            "why python", "why is python popular",
            "why python popular", "why use python",
            "advantages of python", "benefits of python",
            "python advantages", "python benefits"
        ]):
            return format_answer(
                "Python is popular because it is simple, flexible and has many useful libraries.",
                "Python is popular because it has simple and readable syntax, a large community, many useful libraries, and applications in Data Science, AI, Machine Learning, automation and web development.",
                "Python is easy to learn, easy to read and has many ready-made libraries. It can be used for many different types of work.",
                "Python is popular because of its readable syntax, extensive library ecosystem, large developer community and versatility. It is widely used in areas such as Data Science, Artificial Intelligence, Machine Learning, automation, scripting and web development."
            )

        # General Python
        return format_answer(
            "Python is a simple, high-level programming language used for many types of software development.",
            "Python is a high-level programming language known for its simple and readable syntax. It is widely used in Data Science, AI, Machine Learning, automation and web development.",
            "Python is a programming language that is relatively easy to learn. It is used for coding, data analysis, AI, automation and many other tasks.",
            "Python is a high-level, general-purpose programming language designed to be readable and relatively easy to learn. It supports procedural, object-oriented and functional programming styles. Python is widely used in Data Science, Artificial Intelligence, Machine Learning, automation, web development and scripting."
        )

    # ------------------------------------------------------------
    # DATA SCIENCE
    # ------------------------------------------------------------
    # Direct missing-value rules are placed before the broader Data Science
    # trigger so these common questions always get the correct DS answer.
    if contains_phrase(text, [
        "how do you handle missing values",
        "how do i handle missing values",
        "how to handle missing values",
        "how can missing values be handled",
        "how to deal with missing values",
        "ways to handle missing values",
        "methods to handle missing values",
        "how should missing values be handled",
        "how to treat missing values",
        "what to do with missing values",
        "handle missing values",
        "handling missing values"
    ]):
        return format_answer(
            "Missing values can be handled by removing unsuitable data or filling missing entries with appropriate values.",
            "Common ways to handle missing values include removing rows or columns when appropriate, or filling missing values using methods such as mean, median or mode when suitable.",
            "We can remove missing data or fill it with a suitable value, such as the mean, median or mode, depending on the data.",
            "Handling missing values depends on the type of data and why values are missing. Common methods include removing rows or columns when appropriate, imputing numerical values with the mean or median, using the mode for suitable categorical data, or applying more advanced imputation methods."
        )

    if contains_phrase(text, [
        "what are missing values",
        "what is a missing value",
        "define missing values",
        "missing values meaning",
        "what does missing value mean",
        "missing values",
        "missing data",
        "missing value"
    ]):
        return format_answer(
            "Missing values are data entries that are absent or unavailable in a dataset.",
            "Missing values are observations for which information is absent or unavailable in a dataset. They should be identified and handled appropriately before analysis.",
            "Missing values mean that some information is not present in the dataset.",
            "Missing values occur when a dataset does not contain a value for an observation or variable. They may occur because information was not collected, was unavailable, or was recorded incorrectly. Missing values should be examined before analysis because they can affect results."
        )

    if contains_phrase(text, [
        "data science", "data scientist", "data analysis", "data analytics",
        "exploratory data analysis", "what is eda", "eda",
        "data cleaning", "data visualization", "data preprocessing",
        "data wrangling", "data manipulation", "data collection",
        "data mining", "statistics in data science", "data science project",
        "covariance", "correlation", "mean", "median", "mode",
        "variance", "standard deviation", "outlier", "outliers",
        "feature engineering", "time series", "time-series data",
        "normalization", "standardization", "sampling",
        "descriptive statistics", "inferential statistics",
        "hypothesis testing", "null hypothesis", "p-value",
        "data transformation", "structured data", "unstructured data",
        "qualitative data", "quantitative data", "missing value", "missing values",
        "missing", "handle missing", "handling missing",
        "data visualization tools", "visualization tools"
    ]):

        # Difference between Data Science and Data Analytics
        if (
            contains_phrase(text, ["difference", "different", "distinguish", "vs", "versus"])
            and contains_phrase(text, ["data science"])
            and contains_phrase(text, ["data analytics", "data analysis"])
        ):
            return format_answer(
                "Data Science is broader and can include Machine Learning, while Data Analytics mainly focuses on analyzing data to find insights.",
                "Data Science is a broader field that includes programming, statistics, data analysis and Machine Learning. Data Analytics mainly focuses on examining data, finding patterns and generating insights to support decisions.",
                "Data Science is about working with data using programming, statistics and sometimes Machine Learning. Data Analytics mainly focuses on studying data to understand what happened and find useful insights.",
                "Data Science covers a wider workflow including data collection, cleaning, analysis, visualization, statistics and Machine Learning when required. Data Analytics mainly focuses on examining existing data, identifying trends and patterns, creating reports or dashboards, and communicating insights."
            )

        # What is Data Science
        if contains_phrase(text, [
            "what is data science", "define data science",
            "data science meaning", "explain data science"
        ]):
            return format_answer(
                "Data Science is the field of using data, statistics and programming to find useful insights.",
                "Data Science is a field that combines programming, statistics, data analysis and domain knowledge to extract useful insights from data and solve practical problems.",
                "Data Science means using data and programming to understand information, find patterns and solve problems.",
                "Data Science combines programming, statistics, mathematics, data analysis and domain knowledge. A typical workflow includes collecting data, cleaning it, exploring and visualizing it, applying statistical or Machine Learning techniques when required, and communicating useful findings."
            )

        # Data Analytics
        if contains_phrase(text, [
            "what is data analytics", "define data analytics",
            "data analytics meaning", "explain data analytics"
        ]):
            return format_answer(
                "Data Analytics is the process of examining data to find useful patterns, trends and insights.",
                "Data Analytics is the process of collecting, cleaning and examining data to identify patterns, trends and useful insights for decision-making.",
                "Data Analytics means studying data to understand what happened, find patterns and get useful information for decisions.",
                "Data Analytics involves collecting, cleaning, transforming and examining data to identify trends, patterns and relationships. The results are often presented through reports, dashboards and visualizations to support better decisions."
            )

        # Data Scientist
        if contains_phrase(text, [
            "what is a data scientist", "who is a data scientist",
            "define data scientist", "data scientist role"
        ]):
            return format_answer(
                "A Data Scientist uses data, statistics and programming to solve problems and generate insights.",
                "A Data Scientist collects, cleans, analyzes and interprets data and may build Machine Learning models to solve practical problems.",
                "A Data Scientist works with data to find patterns, answer questions and create useful solutions using programming and statistics.",
                "A Data Scientist typically works across data collection, cleaning, EDA, visualization, statistical analysis and model building when required. They also communicate findings and help turn data into useful business or project insights."
            )

        # Data Science vs Machine Learning
        if (
            contains_phrase(text, ["difference", "different", "distinguish", "vs", "versus"])
            and contains_phrase(text, ["data science"])
            and contains_phrase(text, ["machine learning", "ml"])
        ):
            return format_answer(
                "Data Science is broader, while Machine Learning focuses on algorithms that learn patterns from data.",
                "Data Science covers the complete process of working with data, while Machine Learning is a part of Data Science that focuses on learning patterns from data to make predictions or decisions.",
                "Data Science works with the whole data process. Machine Learning is one technique used to make models learn from data.",
                "Data Science can include data collection, cleaning, EDA, visualization, statistics, communication and Machine Learning. Machine Learning specifically focuses on algorithms that learn from data and produce predictions, classifications or other outputs."
            )

        # EDA
        if contains_phrase(text, [
            "what is eda", "eda", "exploratory data analysis",
            "what is exploratory data analysis"
        ]):
            return format_answer(
                "EDA stands for Exploratory Data Analysis. It is used to understand a dataset before deeper analysis or modeling.",
                "Exploratory Data Analysis (EDA) is the process of examining data using statistics and visualizations to understand distributions, patterns, relationships and unusual values.",
                "EDA means exploring a dataset to understand its columns, values, patterns, missing data and possible outliers before building a model.",
                "EDA is an important Data Science step that involves inspecting data types, checking missing values and duplicates, studying distributions, identifying outliers, analyzing relationships between variables and creating visualizations."
            )

        # Data Collection
        if contains_phrase(text, [
            "what is data collection", "data collection", "collecting data",
            "methods of data collection", "data sources"
        ]):
            return format_answer(
                "Data collection is the process of gathering relevant data from suitable sources.",
                "Data collection is the process of gathering data required for analysis or a Data Science project. Sources can include databases, files, APIs, surveys, sensors and websites where permitted.",
                "Data collection means gathering the information needed for a project from useful sources.",
                "Data collection is an early Data Science step in which relevant and reliable information is gathered. Common sources include databases, CSV or Excel files, APIs, surveys, application logs and sensors. The collected data should be relevant to the problem being solved."
            )

        # Data Cleaning
        if contains_phrase(text, [
            "what is data cleaning", "data cleaning", "define data cleaning",
            "explain data cleaning", "cleaning data"
        ]):
            return format_answer(
                "Data cleaning is the process of finding and fixing incorrect, missing, duplicate or inconsistent data.",
                "Data cleaning prepares data for analysis by handling missing values, duplicates, incorrect formats, inconsistent values and other data quality problems.",
                "Data cleaning means making a dataset more accurate and consistent before using it for analysis.",
                "Common data cleaning tasks include handling missing values, removing duplicates, correcting inconsistent formats, treating invalid values, standardizing data and checking data quality before analysis."
            )

        # Data Wrangling
        if contains_phrase(text, [
            "what is data wrangling", "data wrangling", "data munging",
            "data manipulation", "wrangling in data science"
        ]):
            return format_answer(
                "Data wrangling is the process of transforming raw data into a useful format for analysis.",
                "Data wrangling involves collecting, cleaning, transforming, combining and organizing raw data so it can be analyzed effectively.",
                "Data wrangling means changing messy raw data into a clean and useful form for analysis.",
                "Data wrangling prepares raw data for analysis by handling missing values, changing formats, filtering records, creating useful columns, combining datasets and organizing information into a suitable structure."
            )

        # Data Visualization Tools
        # Keep this BEFORE the general Data Visualization rule so that
        # tool-related questions do not get the general visualization answer.
        if contains_phrase(text, [
            "data visualization tools", "tools for data visualization",
            "visualization tools", "visualization tool",
            "tools used for data visualization",
            "what are data visualization tools",
            "what is data visualization tool", "data visualization software"
        ]):
            return (
                "Common Data Visualization tools include:\n\n"
                "• Matplotlib – Python library for creating charts and plots\n"
                "• Seaborn – Python library for statistical visualizations\n"
                "• Plotly – Interactive charts and dashboards\n"
                "• Power BI – Business intelligence and interactive dashboards\n"
                "• Tableau – Data visualization and business intelligence\n"
                "• Excel – Basic charts, graphs and data visualization 📊"
            )

        # Data Visualization
        if contains_phrase(text, [
            "what is data visualization", "data visualization", "define data visualization",
            "explain data visualization", "visualize data"
        ]):
            return format_answer(
                "Data Visualization is the use of charts, graphs and other visuals to understand and communicate data.",
                "Data Visualization represents data using charts, graphs and plots so that trends, patterns and relationships can be understood more easily.",
                "Data Visualization means showing data visually using graphs and charts instead of only looking at tables of numbers.",
                "Data Visualization helps communicate complex information clearly. Common visualizations include bar charts, line charts, scatter plots, histograms, box plots and pie charts, depending on the data and purpose of analysis."
            )

        # Structured Data
        if contains_phrase(text, [
            "what is structured data", "define structured data",
            "structured data meaning", "structured data in data science"
        ]):
            return format_answer(
                "Structured data is organized in a defined format, usually rows and columns.",
                "Structured data is organized according to a predefined schema, commonly in rows and columns such as a database table or spreadsheet.",
                "Structured data is neatly organized, like information stored in rows and columns.",
                "Structured data follows a predefined structure or schema. Examples include database tables, spreadsheets and records with fixed fields such as name, age and salary. It is generally easy to store, query and analyze."
            )

        # Unstructured Data
        if contains_phrase(text, [
            "what is unstructured data", "define unstructured data",
            "unstructured data meaning", "unstructured data in data science"
        ]):
            return format_answer(
                "Unstructured data does not follow a fixed tabular structure, such as images, videos or free text.",
                "Unstructured data is information without a predefined tabular schema. Examples include text documents, images, audio and video.",
                "Unstructured data is less organized, like photos, videos or free text.",
                "Unstructured data does not follow a fixed tabular structure. It can include documents, emails, images, audio and video, and may require additional processing before analysis."
            )

        # Structured vs Unstructured Data
        if (
            contains_phrase(text, ["difference", "different", "distinguish", "vs", "versus"])
            and contains_phrase(text, ["structured data", "unstructured data"])
        ):
            return format_answer(
                "Structured data follows a defined format, while unstructured data does not follow a fixed tabular structure.",
                "Structured data is organized into a predefined format such as rows and columns. Unstructured data can include text, images, audio or video without a fixed tabular structure.",
                "Structured data is neatly organized, like a table. Unstructured data is less organized, like images, videos or free text.",
                "Structured data usually follows a predefined schema and is easy to store and query in relational tables. Unstructured data does not follow a fixed tabular schema and may require additional processing techniques before analysis."
            )

        # Qualitative Data
        if contains_phrase(text, [
            "what is qualitative data", "define qualitative data",
            "qualitative data meaning", "qualitative data in data science",
            "qualitative data definition", "explain qualitative data"
        ]):
            return format_answer(
                "Qualitative data describes qualities, characteristics or categories rather than numerical measurements.",
                "Qualitative data is non-numerical, descriptive information used to represent qualities, opinions, categories or characteristics. Examples include customer feedback, color, product type and opinions.",
                "Qualitative data describes what something is like instead of giving a measurable number. For example, 'red', 'excellent' or 'online'.",
                "Qualitative data represents non-numerical characteristics, categories, opinions or descriptions. It is commonly used to understand attributes or experiences. Examples include customer feedback, color, product type, interview responses and satisfaction comments."
            )

        # Quantitative Data
        if contains_phrase(text, [
            "what is quantitative data", "define quantitative data",
            "quantitative data meaning", "quantitative data in data science",
            "quantitative data definition", "explain quantitative data"
        ]):
            return format_answer(
                "Quantitative data represents numerical values that can be measured or counted.",
                "Quantitative data is numerical information that can be measured or counted. Examples include age, salary, height, temperature, marks and number of customers.",
                "Quantitative data gives numbers that can be measured or counted, such as 25 years, ₹50,000 or 180 cm.",
                "Quantitative data represents measurable numerical values. It can be analyzed using mathematical and statistical methods. Examples include income, temperature, marks, sales amount, height and number of customers."
            )

        # Qualitative vs Quantitative Data
        if (
            contains_phrase(text, ["difference", "different", "distinguish", "compare", "comparison", "vs", "versus"])
            and contains_phrase(text, ["qualitative", "quantitative"])
        ):
            return format_answer(
                "Qualitative data describes qualities or categories, while quantitative data represents numerical values.",
                "Qualitative data is non-numerical and describes characteristics, opinions or categories, such as color or customer feedback. Quantitative data is numerical and can be measured or counted, such as age, salary or height.",
                "Qualitative data describes qualities or categories. Quantitative data gives numbers that can be measured or counted.",
                "For example, customer feedback such as 'excellent' is qualitative, while a customer rating of 5 is quantitative. Qualitative data helps describe characteristics or experiences; quantitative data supports numerical measurement and statistical analysis."
            )

        # Data Types
        if contains_phrase(text, [
            "types of data", "data types in data science", "types of data in data science",
            "different types of data"
        ]):
            return format_answer(
                "Common data types include numerical, categorical, ordinal, time-series and text data.",
                "In Data Science, common data types include numerical data, categorical data, ordinal data, time-series data and text or other unstructured data.",
                "Data can contain numbers, categories, ordered categories, dates and text. Each type may need different analysis methods.",
                "Data can be classified in several ways. Numerical data represents quantities, categorical data represents groups, ordinal data has meaningful order, time-series data is recorded over time, and unstructured data can include text, images, audio or video."
            )

        # Handling Missing Values
        # Keep this BEFORE the general Missing Values rule so questions
        # asking how to handle them receive a practical answer.
        if contains_phrase(text, [
            "handle missing values", "handling missing values",
            "how to handle missing values", "how do you handle missing values",
            "how can missing values be handled", "how to deal with missing values",
            "ways to handle missing values", "methods to handle missing values",
            "how do i handle missing values", "how should missing values be handled",
            "how to treat missing values", "what to do with missing values"
        ]):
            return format_answer(
                "Missing values can be handled by removing suitable data or filling the values with appropriate replacements.",
                "Common ways to handle missing values include removing suitable rows or columns, or filling values using methods such as mean, median or mode when appropriate.",
                "We can remove missing data or fill it with a suitable value, such as the mean, median or mode, depending on the situation.",
                "Handling missing values depends on the dataset and why the values are missing. Common approaches include removing rows or columns when appropriate, imputing numerical values with mean or median, using mode for suitable categorical data, or applying more advanced imputation methods."
            )

        # Missing Values
        if contains_phrase(text, [
            "missing values", "what are missing values", "missing data",
            "missing value", "what is a missing value",
            "define missing values", "missing values meaning",
            "what does missing value mean"
        ]):
            return format_answer(
                "Missing values are data entries that are absent or unavailable in a dataset.",
                "Missing values are observations for which information is absent or unavailable in a dataset. They should be identified and handled appropriately before analysis.",
                "Missing values mean some information is not present in the dataset.",
                "Missing values occur when a dataset does not contain a value for an observation or variable. They can arise because information was not collected, was unavailable or was recorded incorrectly. Missing values should be examined before analysis because they can affect results."
            )

        # Duplicates
        if contains_phrase(text, [
            "duplicate data", "duplicate values", "duplicate records",
            "remove duplicates", "handling duplicates"
        ]):
            return format_answer(
                "Duplicate records are repeated entries that may affect the quality of analysis.",
                "Duplicate data occurs when the same record or observation appears more than once. Duplicates should be identified and removed or handled when they do not represent valid repeated observations.",
                "Duplicate data means the same information appears more than once. Unwanted duplicates can be removed during data cleaning.",
                "Duplicate records can distort counts, summaries and model results. Data cleaning often includes identifying exact or logically duplicated records and deciding whether they should be removed based on the meaning of the dataset."
            )

        # Outliers
        if contains_phrase(text, [
            "what is an outlier", "what are outliers", "outlier", "outliers",
            "detect outliers", "handling outliers"
        ]):
            return format_answer(
                "An outlier is a data value that is unusually far from the other observations.",
                "An outlier is an observation that differs substantially from the general pattern of the data. Outliers can be investigated using methods such as the IQR rule, box plots or statistical techniques.",
                "An outlier is a value that looks unusually high or low compared with most other values.",
                "Outliers may represent valid rare observations, measurement errors or unusual events. They should be investigated rather than automatically removed. Common detection approaches include box plots, the IQR rule and standardized scores."
            )

        # Correlation
        if contains_phrase(text, [
            "what is correlation", "correlation in data science",
            "correlation analysis", "correlation coefficient"
        ]):
            return format_answer(
                "Correlation measures the strength and direction of the relationship between two variables.",
                "Correlation describes how two variables move in relation to each other. A positive relationship means they tend to increase together, while a negative relationship means one tends to increase as the other decreases.",
                "Correlation tells us whether two variables are related and how strongly they move together.",
                "Correlation is a statistical measure of association between variables. The commonly used Pearson correlation coefficient ranges from -1 to +1, where the sign indicates direction and the magnitude indicates strength of linear association. Correlation does not by itself prove causation."
            )

        # Covariance
        if contains_phrase(text, [
            "what is covariance", "covariance in data science", "covariance"
        ]):
            return format_answer(
                "Covariance indicates the direction in which two variables vary together.",
                "Covariance measures whether two variables tend to increase or decrease together. Its magnitude depends on the scale of the variables, so it is less directly comparable than correlation.",
                "Covariance tells us whether two variables generally move in the same or opposite directions.",
                "A positive covariance indicates that variables tend to move in the same direction, while a negative covariance indicates opposite movement. Unlike correlation, covariance is affected by the units and scale of the variables."
            )

        # Mean, Median, Mode
        if (
            contains_phrase(text, ["mean", "average"])
            and contains_phrase(text, ["median", "mode"])
        ):
            return format_answer(
                "Mean is the average, Median is the middle value, and Mode is the most frequent value.",
                "Mean is calculated by dividing the sum of values by the number of values. Median is the middle value after sorting the data, and Mode is the value that occurs most frequently.",
                "Mean is the average, median is the middle value, and mode is the most common value.",
                "Mean, median and mode are measures of central tendency. Mean uses all numerical values and can be affected by extreme values. Median is based on the middle position and is often more robust to outliers. Mode identifies the most frequently occurring value."
            )

        # Mean
        if contains_phrase(text, ["what is mean", "mean in data science", "arithmetic mean", "average in data"]):
            return format_answer(
                "Mean is the average of a set of numerical values.",
                "The mean is calculated by adding all numerical values and dividing the total by the number of values.",
                "Mean means average. Add all the values and divide by how many values there are.",
                "The arithmetic mean is a measure of central tendency calculated as the sum of all observations divided by the number of observations. It is useful for summarizing numerical data but can be influenced by extreme values."
            )

        # Median
        if contains_phrase(text, ["what is median", "median in data science"]):
            return format_answer(
                "Median is the middle value of an ordered dataset.",
                "The median is the middle value after the data is arranged in order. If there is an even number of observations, it is commonly calculated as the average of the two middle values.",
                "Median is the middle value when the data is arranged from smallest to largest.",
                "Median is a measure of central tendency based on the position of observations after sorting. It is less affected by extreme values than the mean and is therefore useful for skewed data."
            )

        # Mode
        if contains_phrase(text, ["what is mode", "mode in data science", "mode of data"]):
            return format_answer(
                "Mode is the value that occurs most frequently in a dataset.",
                "The mode is the most frequently occurring value in a dataset. A dataset can have one mode, more than one mode, or no unique mode.",
                "Mode is simply the value that appears most often.",
                "Mode is a measure of central tendency that identifies the most frequent observation. It can be useful for categorical data as well as numerical data and does not require arithmetic operations."
            )

        # Variance
        if contains_phrase(text, ["what is variance", "variance in data science", "variance"]):
            return format_answer(
                "Variance measures how much data values spread around the mean.",
                "Variance measures the average squared deviation of observations from the mean. A larger variance indicates greater spread in the data.",
                "Variance tells us how spread out the values are from their average.",
                "Variance quantifies dispersion by averaging squared deviations from the mean, using the appropriate population or sample formula. Because deviations are squared, variance is expressed in squared units."
            )

        # Standard Deviation
        if contains_phrase(text, [
            "what is standard deviation", "standard deviation", "std deviation"
        ]):
            return format_answer(
                "Standard deviation measures the typical spread of values around the mean.",
                "Standard deviation is the square root of variance and indicates how much observations typically vary around the mean.",
                "Standard deviation tells us how far values usually spread from the average.",
                "Standard deviation is a measure of dispersion calculated as the square root of variance. A smaller standard deviation generally indicates values are closer to the mean, while a larger value indicates greater spread."
            )

        # Population vs Sample
        if (
            contains_phrase(text, ["difference", "different", "distinguish", "vs", "versus"])
            and contains_phrase(text, ["population", "sample"])
        ):
            return format_answer(
                "A population includes the full group of interest, while a sample is a subset of that group.",
                "A population is the complete set of observations being studied, while a sample is a smaller subset selected from the population for analysis.",
                "Population means the whole group. Sample means a smaller part taken from that group.",
                "In statistics, the population represents the entire group of interest, while a sample represents selected observations from that population. Sampling is used when studying the entire population is impractical or unnecessary."
            )

        # Descriptive Statistics
        if contains_phrase(text, [
            "what is descriptive statistics", "descriptive statistics",
            "define descriptive statistics"
        ]):
            return format_answer(
                "Descriptive statistics summarize the main characteristics of data.",
                "Descriptive statistics use measures such as mean, median, mode, variance, standard deviation and frequency summaries to describe a dataset.",
                "Descriptive statistics help us summarize and understand the main features of a dataset.",
                "Descriptive statistics organize and summarize observed data without necessarily making predictions beyond it. Common measures include central tendency, dispersion, frequencies, percentages and summary tables or visualizations."
            )

        # Inferential Statistics
        if contains_phrase(text, [
            "what is inferential statistics", "inferential statistics",
            "define inferential statistics"
        ]):
            return format_answer(
                "Inferential statistics use sample data to draw conclusions about a wider population.",
                "Inferential statistics use information from a sample to estimate, test or make conclusions about a population.",
                "Inferential statistics help us use a sample to learn about a larger population.",
                "Inferential statistics include methods such as confidence intervals and hypothesis tests that use sample information to draw conclusions about a population while accounting for uncertainty."
            )

        # Hypothesis Testing
        if contains_phrase(text, [
            "what is hypothesis testing", "hypothesis testing",
            "hypothesis test", "hypothesis"
        ]):
            return format_answer(
                "Hypothesis testing is a statistical method used to evaluate a claim using sample data.",
                "Hypothesis testing compares evidence from sample data with a stated null hypothesis to determine whether the evidence is sufficient to reject it under a chosen significance level.",
                "Hypothesis testing checks whether the data gives enough evidence against a starting assumption.",
                "Hypothesis testing generally involves stating a null and alternative hypothesis, selecting a significance level, calculating an appropriate test statistic or p-value, and making a decision based on the statistical evidence."
            )

        # Null Hypothesis
        if contains_phrase(text, [
            "what is null hypothesis", "null hypothesis", "h0 hypothesis"
        ]):
            return format_answer(
                "The null hypothesis is the starting assumption that there is no effect or difference of interest.",
                "The null hypothesis, often written as H₀, represents a stated assumption such as no difference, no association or no effect. Statistical tests evaluate evidence against it.",
                "The null hypothesis is the starting assumption that nothing important has changed or that there is no effect.",
                "In hypothesis testing, the null hypothesis is a formal statement about a population parameter or relationship. Evidence from the sample is used to assess whether the observed result would be unusual under that assumption."
            )

        # P-value
        if contains_phrase(text, [
            "what is p value", "what is p-value", "p value", "p-value"
        ]):
            return format_answer(
                "A p-value measures how unusual the observed result would be if the null hypothesis were true.",
                "A p-value is the probability, under the null hypothesis, of obtaining a result at least as extreme as the one observed, according to the chosen statistical test.",
                "The p-value helps us judge how much evidence the data gives against the null hypothesis.",
                "A p-value is calculated under the assumption that the null hypothesis is true. A small p-value can provide evidence against that hypothesis, but it is not the probability that the null hypothesis itself is true."
            )

        # Data Preprocessing
        if contains_phrase(text, [
            "what is data preprocessing", "data preprocessing",
            "preprocessing in data science", "preprocess data", "pre processing"
        ]):
            return format_answer(
                "Data preprocessing prepares raw data so it can be analyzed effectively.",
                "Data preprocessing is the process of preparing raw data by cleaning it, transforming variables, handling missing values and converting data into a suitable form for analysis or modeling.",
                "Data preprocessing means cleaning and preparing raw data before analysis or Machine Learning.",
                "Data preprocessing can include data cleaning, handling missing values and outliers, encoding categorical variables, transforming or scaling numerical values, selecting useful variables and splitting data appropriately for modeling."
            )

        # Feature Engineering
        if contains_phrase(text, [
            "what is feature engineering", "feature engineering",
            "feature creation", "feature extraction"
        ]):
            return format_answer(
                "Feature Engineering creates or transforms useful input variables from existing data.",
                "Feature Engineering is the process of creating, transforming or selecting variables so that useful information can be represented effectively for analysis or Machine Learning.",
                "Feature Engineering means making useful input columns from existing data so a model or analysis can work better.",
                "Feature Engineering can include creating new variables, transforming existing variables, extracting information from dates or text, combining fields and selecting informative features. The goal is to represent useful information in a form suitable for the task."
            )

        # Data Transformation
        if contains_phrase(text, [
            "what is data transformation", "data transformation",
            "transforming data", "data transform"
        ]):
            return format_answer(
                "Data transformation changes data into a suitable format for analysis.",
                "Data transformation involves changing the representation, scale, structure or values of data so that it is suitable for analysis or modeling.",
                "Data transformation means changing data into a more useful form before analysis.",
                "Data transformation may include changing data types, encoding categories, scaling numerical values, applying mathematical transformations, reshaping tables or creating derived variables."
            )

        # Normalization vs Standardization
        if (
            contains_phrase(text, ["difference", "different", "distinguish", "vs", "versus"])
            and contains_phrase(text, ["normalization", "standardization"])
        ):
            return format_answer(
                "Normalization commonly scales values to a fixed range, while Standardization centers values around the mean with unit standard deviation.",
                "Normalization often rescales values to a specified range such as 0 to 1. Standardization transforms values using the mean and standard deviation so the resulting variable has mean near 0 and standard deviation near 1.",
                "Normalization usually puts values into a fixed range. Standardization changes values based on their mean and standard deviation.",
                "Normalization and standardization are scaling techniques. Min-max normalization commonly maps values to a selected range, while standardization commonly uses z-scores: (value - mean) / standard deviation. The appropriate method depends on the analysis or model."
            )

        # Normalization
        if contains_phrase(text, [
            "what is normalization", "normalization in data science",
            "data normalization", "min max normalization"
        ]):
            return format_answer(
                "Normalization rescales numerical values to a common range.",
                "Normalization is a scaling technique that commonly transforms numerical values to a fixed range, such as 0 to 1, using the minimum and maximum values.",
                "Normalization changes numbers so they fit into a common range, often 0 to 1.",
                "Min-max normalization commonly uses the formula (x - min) / (max - min) to map values to the 0-to-1 range. Scaling can be useful when variables have very different numeric ranges."
            )

        # Standardization
        if contains_phrase(text, [
            "what is standardization", "standardization in data science",
            "data standardization", "z score", "z-score"
        ]):
            return format_answer(
                "Standardization transforms values based on their mean and standard deviation.",
                "Standardization commonly converts a value to a z-score using (x - mean) / standard deviation, producing a variable centered around 0 with a standard deviation near 1.",
                "Standardization changes values based on how far they are from the average.",
                "Standardization expresses observations relative to the mean and standard deviation. The common z-score transformation is (x - mean) / standard deviation. It is often used when variables have different scales and the chosen method benefits from standardized inputs."
            )

        # Data Sampling
        if contains_phrase(text, [
            "what is sampling", "sampling in data science", "data sampling",
            "sampling methods"
        ]):
            return format_answer(
                "Sampling is the process of selecting a subset of observations from a larger population or dataset.",
                "Sampling selects a subset of observations for analysis. It can reduce cost and processing requirements while aiming to represent the population appropriately.",
                "Sampling means taking a smaller group of data from a larger group for analysis.",
                "Sampling is used when analyzing every observation is impractical or unnecessary. Methods include simple random sampling, stratified sampling, systematic sampling and cluster sampling, with the appropriate choice depending on the study design."
            )

        # Time Series
        if contains_phrase(text, [
            "what is time series", "time series data", "time-series data",
            "time series analysis"
        ]):
            return format_answer(
                "Time-series data consists of observations recorded over time.",
                "Time-series data contains measurements collected in a time order, such as daily sales, monthly revenue or hourly temperature readings.",
                "Time-series data is data collected over time, such as daily sales or monthly temperature.",
                "Time-series analysis studies observations indexed by time. It can involve trends, seasonality, cycles, autocorrelation and forecasting, depending on the problem and data."
            )

        # Data Mining
        if contains_phrase(text, [
            "what is data mining", "data mining", "data mining in data science"
        ]):
            return format_answer(
                "Data Mining is the process of discovering useful patterns and relationships in large datasets.",
                "Data Mining uses computational and statistical techniques to discover patterns, relationships, groups or useful information in large datasets.",
                "Data Mining means finding useful patterns or information hidden inside large amounts of data.",
                "Data Mining involves analyzing large datasets to discover useful patterns, associations, clusters, trends or anomalies. It can use techniques from statistics, databases and Machine Learning."
            )

        # Role of SQL in Data Science
        if contains_phrase(text, [
            "role of sql in data science", "sql in data science",
            "use of sql in data science", "why sql is used in data science"
        ]):
            return format_answer(
                "SQL helps Data Scientists retrieve, filter and analyze data stored in databases.",
                "SQL is used in Data Science to query databases, filter records, join tables, aggregate data and prepare datasets for analysis.",
                "SQL helps a Data Scientist get the required data from databases and organize it before analysis.",
                "SQL is important in Data Science because much real-world data is stored in relational databases. Data Scientists use SQL to select relevant records, join tables, calculate aggregates, filter data and prepare datasets for further analysis in Python or other tools."
            )

        # Python in Data Science
        if contains_phrase(text, [
            "python in data science", "role of python in data science",
            "use of python in data science", "why python is used in data science"
        ]):
            return format_answer(
                "Python is widely used in Data Science for data cleaning, analysis, visualization and Machine Learning.",
                "Python is widely used in Data Science because libraries such as Pandas, NumPy and Matplotlib support data manipulation, numerical analysis and visualization, while other libraries support Machine Learning and statistics.",
                "Python helps Data Scientists clean data, analyze it, create charts and build models using useful libraries.",
                "Python supports many stages of the Data Science workflow. Pandas helps manipulate datasets, NumPy supports numerical computing, visualization libraries help communicate patterns, and Machine Learning libraries provide modeling tools."
            )

        # Pandas in Data Science
        if contains_phrase(text, [
            "pandas in data science", "role of pandas in data science",
            "use of pandas in data science"
        ]):
            return format_answer(
                "Pandas is used to load, clean, transform and analyze structured data.",
                "Pandas is commonly used in Data Science for reading datasets, cleaning data, filtering records, handling missing values, transforming columns and performing exploratory analysis.",
                "Pandas helps us read, clean, organize and analyze datasets in Python.",
                "Pandas provides Series and DataFrame structures that make tabular data manipulation convenient. It supports operations such as reading files, selecting and filtering data, handling missing values, grouping, merging and transforming datasets."
            )

        # NumPy in Data Science
        if contains_phrase(text, [
            "numpy in data science", "role of numpy in data science",
            "use of numpy in data science"
        ]):
            return format_answer(
                "NumPy supports numerical computing and array operations in Data Science.",
                "NumPy provides efficient multidimensional arrays and mathematical functions that are useful for numerical analysis and many Data Science workflows.",
                "NumPy helps Data Scientists work with numbers, arrays and mathematical calculations efficiently.",
                "NumPy is widely used for numerical computing. Its array operations and mathematical functions support data manipulation and provide a foundation used by many scientific and Data Science libraries."
            )

        # Machine Learning in Data Science
        if contains_phrase(text, [
            "machine learning in data science", "what is machine learning in data science",
            "role of machine learning in data science", "machine learning role in data science"
        ]):
            return format_answer(
                "Machine Learning helps Data Science systems learn patterns from data and make predictions or classifications.",
                "Machine Learning is used in Data Science to build models that learn from data and can make predictions, classifications or other data-driven decisions.",
                "In Data Science, Machine Learning is used when we want a computer to learn patterns from data and make predictions on new data.",
                "Machine Learning is one part of the Data Science workflow. After data preparation and analysis, suitable Machine Learning techniques can be used for tasks such as classification, regression, clustering and prediction, followed by model evaluation."
            )

        # Steps in a Data Science Project
        if contains_phrase(text, [
            "steps in a data science project", "steps of a data science project",
            "data science project steps", "workflow of a data science project",
            "data science project workflow", "data science life cycle",
            "data science lifecycle", "data science life cycle steps"
        ]):
            return (
                "Typical steps in a Data Science project are:\n\n"
                "1. Define the problem 🎯\n"
                "2. Collect the data 📥\n"
                "3. Clean and prepare the data 🧹\n"
                "4. Perform EDA and visualization 📊\n"
                "5. Build a model when required 🤖\n"
                "6. Evaluate the results\n"
                "7. Communicate findings or deploy the solution 🚀"
            )

        # Data Science Lifecycle
        if contains_phrase(text, ["data science lifecycle", "data science life cycle"]):
            return (
                "A Data Science lifecycle commonly includes:\n\n"
                "1. Problem definition 🎯\n"
                "2. Data collection 📥\n"
                "3. Data cleaning and preparation 🧹\n"
                "4. Exploratory Data Analysis 📊\n"
                "5. Modeling when required 🤖\n"
                "6. Evaluation\n"
                "7. Communication or deployment 🚀"
            )

        # How to learn / roadmap
        if contains_phrase(text, [
            "roadmap", "learn data science", "learning path",
            "how to become a data scientist", "how do i learn data science",
            "data science roadmap"
        ]):
            return (
                "A simple Data Science roadmap is:\n\n"
                "1. Learn Python and SQL 🐍\n"
                "2. Learn statistics and probability 📊\n"
                "3. Practice Pandas, NumPy and visualization\n"
                "4. Learn Machine Learning basics 🤖\n"
                "5. Build real projects\n"
                "6. Create a portfolio and prepare for interviews 🚀"
            )

        # Skills needed for Data Science
        if contains_phrase(text, ["skills", "skill set", "what skills"]):
            return (
                "Important Data Science skills include:\n\n"
                "• Python and SQL 🐍\n"
                "• Statistics and probability 📊\n"
                "• Data cleaning and EDA\n"
                "• Pandas and NumPy\n"
                "• Data visualization\n"
                "• Machine Learning basics 🤖"
            )

        # Importance of Data Science
        if contains_phrase(text, ["important", "importance", "why data science"]):
            return (
                "Data Science is important because it helps organizations "
                "use data to discover patterns, generate insights, support "
                "decisions and solve practical problems. 📊"
            )

        # Applications of Data Science
        if contains_phrase(text, [
            "applications of data science", "application of data science",
            "uses of data science", "where is data science used",
            "data science applications"
        ]):
            return (
                "Data Science is used in many areas, such as:\n\n"
                "• Healthcare and medical analysis 🏥\n"
                "• Finance and fraud detection 💰\n"
                "• Recommendation systems 🎯\n"
                "• Customer and marketing analysis\n"
                "• Predictive analysis\n"
                "• Business intelligence and decision-making 📊"
            )

        # Tools used in Data Science
        if contains_phrase(text, [
            "tools used in data science", "data science tools",
            "tools for data science", "data science technologies"
        ]):
            return (
                "Common Data Science tools and technologies include:\n\n"
                "• Python and SQL 🐍\n"
                "• Pandas and NumPy\n"
                "• Matplotlib and Seaborn 📊\n"
                "• Jupyter Notebook\n"
                "• Power BI and Tableau\n"
                "• Scikit-learn for Machine Learning 🤖"
            )

        return format_answer(
            "Data Science uses data, statistics and programming to find useful insights and support decisions.",
            "Data Science combines programming, statistics, data analysis and Machine Learning to collect, clean, analyze and interpret data.",
            "Data Science means using data and programming to understand information, find patterns and get useful insights.",
            "Data Science is a field that combines programming, statistics, mathematics and domain knowledge to extract useful information from data. A typical workflow includes collecting data, cleaning it, performing EDA, visualizing patterns, building models when needed, evaluating results and communicating insights."
        )

    # ------------------------------------------------------------
    # MACHINE LEARNING
    # ------------------------------------------------------------
    # Complete Machine Learning question bank
    # ------------------------------------------------------------
    if contains_phrase(text, [
        "machine learning", "ml", "training data", "testing data", "test data",
        "target variable", "target value", "target in machine learning",
        "features in machine learning", "input features", "classification",
        "regression", "clustering", "supervised learning", "unsupervised learning",
        "reinforcement learning", "applications of machine learning",
        "machine learning applications", "machine learning algorithm",
        "machine learning algorithms", "machine learning model", "overfitting",
        "underfitting", "model training", "model evaluation", "accuracy in machine learning",
        "precision", "recall", "f1 score", "f1-score", "confusion matrix",
        "cross validation", "cross-validation", "hyperparameter", "hyperparameters",
        "hyperparameter tuning", "train test split", "train-test split",
        "bias and variance", "feature scaling", "normalization", "standardization",
        "decision tree", "random forest", "knn", "k nearest neighbors", "support vector machine",
        "svm", "logistic regression", "linear regression", "naive bayes", "naive bayes classifier",
        "k means", "k-means", "dbscan", "gradient boosting", "xgboost",
        "model parameter", "model parameters", "parameters in machine learning",
        "validation data", "validation set", "data preprocessing", "preprocessing in machine learning",
        "machine learning workflow", "ml workflow", "machine learning process",
        "generalization", "generalisation", "class imbalance", "imbalanced data",
        "roc curve", "roc", "auc", "area under curve", "specificity", "sensitivity",
        "classification vs regression", "classification and regression",
        "supervised vs unsupervised", "supervised and unsupervised"
    ]):

        # Difference between Artificial Intelligence and Machine Learning
        if (
            contains_phrase(text, ["difference", "different", "distinguish"])
            and contains_phrase(text, ["artificial intelligence", "ai"])
        ):
            return format_answer(
                "AI is the broader concept of making machines perform tasks that require intelligence, while Machine Learning is a part of AI that learns patterns from data.",
                "Artificial Intelligence (AI) is the broader field of creating systems that can perform tasks that normally require human intelligence. Machine Learning (ML) is a subset of AI in which algorithms learn patterns from data to make predictions or decisions.",
                "AI is the bigger field. Machine Learning is one part of AI that teaches computers to learn from data.",
                "Artificial Intelligence is a broad field focused on building systems that can perform intelligent tasks such as reasoning, perception, language understanding or decision-making. Machine Learning is a subset of AI that uses data and algorithms to learn patterns and improve predictions or decisions without requiring every rule to be explicitly programmed."
            )

        # What is a Machine Learning model?
        if contains_phrase(text, [
            "machine learning model", "ml model",
            "what is a model in machine learning",
            "what is machine learning model", "define machine learning model"
        ]):
            return format_answer(
                "A Machine Learning model is a system that learns patterns from data to make predictions or decisions.",
                "A Machine Learning model is a trained computational system that learns patterns from data and uses those patterns to make predictions or decisions on new data.",
                "A Machine Learning model learns from examples in data and then uses what it learned to make predictions.",
                "A Machine Learning model is the result of training a Machine Learning algorithm on data. During training, the model learns relationships or patterns from the available data. After training, it can be evaluated and used to make predictions, classifications or other decisions on new data."
            )

        # Machine Learning workflow / process
        if contains_phrase(text, [
            "machine learning workflow", "ml workflow", "machine learning process",
            "process of machine learning", "steps of machine learning",
            "steps in machine learning", "machine learning steps"
        ]):
            return (
                "A typical Machine Learning workflow is:\n\n"
                "1. Define the problem 🎯\n"
                "2. Collect data 📥\n"
                "3. Clean and preprocess the data 🧹\n"
                "4. Select or engineer features\n"
                "5. Split the data\n"
                "6. Train a model 🤖\n"
                "7. Evaluate the model\n"
                "8. Tune and improve the model\n"
                "9. Deploy or use the model 🚀"
            )

        # Supervised vs Unsupervised Learning
        if (
            contains_phrase(text, ["difference", "different", "distinguish", "vs", "versus"])
            and contains_phrase(text, ["supervised learning", "unsupervised learning"])
        ):
            return format_answer(
                "Supervised Learning uses labelled data, while Unsupervised Learning works with unlabelled data.",
                "Supervised Learning learns from labelled data with known outputs, while Unsupervised Learning works with unlabelled data to discover patterns or groups.",
                "Supervised Learning learns using examples with answers. Unsupervised Learning finds patterns when the answers are not given.",
                "Supervised Learning uses input-output examples to learn a mapping and is commonly used for classification and regression. Unsupervised Learning does not use predefined target labels and is commonly used for tasks such as clustering and dimensionality reduction."
            )

        # Classification vs Regression
        if (
            contains_phrase(text, ["difference", "different", "distinguish", "vs", "versus"])
            and contains_phrase(text, ["classification", "regression"])
        ):
            return format_answer(
                "Classification predicts categories, while Regression predicts numerical values.",
                "Classification is used to predict discrete classes or categories, while Regression is used to predict continuous numerical values.",
                "Classification gives a category, such as spam or not spam. Regression predicts a number, such as a house price.",
                "Classification and Regression are supervised learning tasks. Classification predicts categorical targets such as yes/no or class labels, while Regression predicts continuous numerical targets such as price, temperature or sales."
            )

        # Data Preprocessing
        if contains_phrase(text, [
            "data preprocessing", "preprocessing in machine learning",
            "what is data preprocessing", "preprocess data", "pre processing"
        ]):
            return format_answer(
                "Data preprocessing prepares raw data so it can be used effectively by a Machine Learning model.",
                "Data preprocessing is the process of preparing raw data for Machine Learning by handling missing values, duplicates, inconsistent formats, categorical variables and feature scaling when required.",
                "Data preprocessing means cleaning and preparing data before giving it to a Machine Learning model.",
                "Data preprocessing can include cleaning data, handling missing values and outliers, encoding categorical variables, scaling numerical features, selecting useful features and splitting data appropriately before model training."
            )

        # Validation Data / Validation Set
        if contains_phrase(text, [
            "validation data", "validation set", "what is validation data",
            "what is validation set"
        ]):
            return format_answer(
                "Validation data is used to check and tune a Machine Learning model during development.",
                "A validation set is a portion of data used during model development to compare models, tune hyperparameters and make decisions before final testing.",
                "Validation data helps us choose and improve a model before checking it on the final test data.",
                "Validation data provides an independent dataset for model selection and hyperparameter tuning. Keeping the final test set separate helps provide a more honest estimate of performance on unseen data."
            )

        # Model Parameters
        if contains_phrase(text, [
            "model parameter", "model parameters",
            "parameters in machine learning", "what are parameters in machine learning",
            "parameter in machine learning"
        ]):
            return format_answer(
                "Model parameters are values learned from training data.",
                "Model parameters are internal values learned by a Machine Learning algorithm during training. Examples include coefficients in Linear Regression and weights in many neural networks.",
                "Parameters are values the model learns automatically from the training data.",
                "Model parameters are learned from the training examples during optimization. They are different from hyperparameters, which are settings chosen to control the learning process."
            )

        # Parameters vs Hyperparameters
        if (
            contains_phrase(text, ["difference", "different", "distinguish", "vs", "versus"])
            and contains_phrase(text, ["parameter", "hyperparameter"])
        ):
            return format_answer(
                "Parameters are learned from data, while hyperparameters are settings chosen for the learning process.",
                "Model parameters are learned during training, while hyperparameters are selected before or around training to control how the algorithm works.",
                "Parameters are learned by the model. Hyperparameters are settings we choose.",
                "Parameters are internal values learned from training data, such as regression coefficients or neural-network weights. Hyperparameters are configuration choices such as tree depth, learning rate or the number of neighbors in KNN."
            )

        # Generalization
        if contains_phrase(text, [
            "generalization", "generalisation", "what is generalization",
            "model generalization"
        ]):
            return format_answer(
                "Generalization is the ability of a Machine Learning model to perform well on unseen data.",
                "Generalization describes how well a trained Machine Learning model applies learned patterns to new data that was not used during training.",
                "Generalization means the model works well not only on training data but also on new data.",
                "A model generalizes well when it learns useful underlying patterns rather than memorizing training examples. Good generalization is important because real-world predictions are usually made on unseen observations."
            )

        # Python + Machine Learning
        if contains_phrase(text, ["python"]):
            return format_answer(
                "Python is widely used in Machine Learning because of its simple syntax and useful libraries.",
                "Python is widely used in Machine Learning for data preparation, model training, evaluation and visualization. Libraries such as Pandas, NumPy and Scikit-learn make these tasks easier.",
                "Python helps in Machine Learning by providing simple tools and libraries to prepare data, train models and make predictions.",
                "Python is commonly used throughout the Machine Learning workflow. Pandas and NumPy help prepare and process data, Scikit-learn provides Machine Learning algorithms, and visualization libraries help understand results. Python's readable syntax also makes experimentation and development easier."
            )

        # Supervised Learning
        if contains_phrase(text, ["supervised learning", "what is supervised learning", "supervised"]):
            return format_answer(
                "Supervised Learning learns from labelled data to make predictions.",
                "Supervised Learning is a Machine Learning approach where a model learns from labelled data. The training data contains inputs and known outputs, which the model uses to learn a relationship and make predictions on new data.",
                "Supervised Learning means teaching a computer using examples where the correct answer is already known.",
                "Supervised Learning uses labelled training data, meaning each training example has an input and a known target output. The model learns the relationship between them and then uses that learned pattern to predict outputs for new observations. Classification and regression are common supervised learning tasks."
            )

        # Unsupervised Learning
        if contains_phrase(text, ["unsupervised learning", "what is unsupervised learning", "unsupervised"]):
            return format_answer(
                "Unsupervised Learning finds patterns or groups in data without labelled answers.",
                "Unsupervised Learning is a Machine Learning approach where a model works with unlabelled data to discover patterns, relationships or groups. Clustering is a common example.",
                "Unsupervised Learning means finding useful groups or patterns in data when the correct answers are not already given.",
                "Unsupervised Learning works with data that does not have predefined target labels. Algorithms analyze the structure of the data to discover patterns, relationships or groups. Clustering and dimensionality reduction are common examples."
            )

        # Reinforcement Learning
        if contains_phrase(text, ["reinforcement learning", "what is reinforcement learning", "reinforcement"]):
            return format_answer(
                "Reinforcement Learning learns by receiving rewards or penalties for actions.",
                "Reinforcement Learning is a Machine Learning approach in which an agent learns by interacting with an environment and receiving rewards or penalties for its actions.",
                "Reinforcement Learning means learning by trying actions and receiving rewards or penalties based on the result.",
                "Reinforcement Learning involves an agent interacting with an environment. The agent selects actions and receives feedback in the form of rewards or penalties. Over time, it learns a strategy for choosing actions that can improve its cumulative reward."
            )

        # Classification
        if contains_phrase(text, ["classification", "classify", "classifier"]) and not contains_phrase(text, [
            "decision tree", "random forest", "knn", "k nearest neighbors", "k-nearest neighbors",
            "support vector machine", "svm", "logistic regression", "linear regression"
        ]):
            return format_answer(
                "Classification is a supervised Machine Learning technique used to predict categories or classes.",
                "Classification is a supervised Machine Learning technique where a model learns from labelled data and predicts a category or class for new data. For example, an email can be classified as spam or not spam.",
                "Classification means teaching a computer to put data into categories. For example, it can decide whether an email is spam or not spam.",
                "Classification is a supervised learning problem in which the target variable contains categories or classes. The model learns patterns from labelled training data and uses those patterns to assign a class to new observations. Examples include spam detection, disease classification and sentiment classification."
            )

        # Regression
        if contains_phrase(text, ["regression", "regressor"]) and not contains_phrase(text, [
            "logistic regression", "linear regression"
        ]):
            return format_answer(
                "Regression is a supervised Machine Learning technique used to predict numerical values.",
                "Regression is a supervised Machine Learning technique used to predict continuous numerical values. For example, it can be used to predict house prices based on features such as area, location and number of rooms.",
                "Regression means predicting a number using data. For example, a model can predict the price of a house.",
                "Regression is a supervised learning problem where the target is a continuous numerical value. A regression model learns relationships between input features and the target and uses them to predict values for new observations. Common examples include predicting prices, sales and temperatures."
            )

        # Clustering
        if contains_phrase(text, ["clustering", "cluster", "k means", "k-means"]):
            return format_answer(
                "Clustering is an unsupervised Machine Learning technique that groups similar data points.",
                "Clustering is an unsupervised Machine Learning technique that groups similar data points together without predefined labels. K-Means is a common clustering algorithm.",
                "Clustering means grouping similar data together without already knowing the categories.",
                "Clustering is an unsupervised learning technique used to discover natural groups or patterns in data. The algorithm groups observations based on their similarity without using labelled target values. K-Means is one commonly used clustering algorithm."
            )

        # Training Data
        if contains_phrase(text, ["training data", "what is training data", "training dataset", "train data"]):
            return format_answer(
                "Training data is the data used to teach a Machine Learning model patterns from examples.",
                "Training data is the dataset used to train a Machine Learning model. It contains input examples and, in supervised learning, the corresponding target values that help the model learn relationships in the data.",
                "Training data is the data a model learns from. It gives the model examples so it can learn patterns and make predictions later.",
                "Training data is the portion of a dataset used during model training. The algorithm uses these examples to learn relationships between features and, when applicable, target values. The learned patterns are then evaluated on data that was not used for training."
            )

        # Testing Data
        if contains_phrase(text, ["testing data", "what is testing data", "test data", "testing dataset"]):
            return format_answer(
                "Testing data is used to evaluate how well a trained Machine Learning model performs on unseen data.",
                "Testing data is a separate dataset used after training to measure how well a Machine Learning model generalizes to new, unseen examples.",
                "Testing data checks whether the model can work correctly on data it has not seen during training.",
                "Testing data is kept separate from the training process and is used to evaluate the final model. Metrics such as accuracy, precision, recall, F1-score or mean squared error can be used depending on the type of Machine Learning problem."
            )

        # Features
        if contains_phrase(text, ["features in machine learning", "what are features", "feature in machine learning", "input features"]):
            return format_answer(
                "Features are the input variables used by a Machine Learning model to make predictions.",
                "Features are the measurable input variables given to a Machine Learning model. For example, in house-price prediction, area, location and number of rooms can be features.",
                "Features are the inputs a model uses to learn and make predictions.",
                "Features represent the input attributes used by a Machine Learning algorithm. Good feature selection can help a model learn useful patterns. Examples include age, income, temperature, transaction amount or image pixel values, depending on the problem."
            )

        # Target Variable / Label
        if contains_phrase(text, ["target variable", "target in machine learning", "what is target", "label in machine learning", "target value"]):
            return format_answer(
                "The target is the output a Machine Learning model is trained to predict.",
                "The target variable, also called the label in many supervised learning tasks, is the known output that a model learns to predict from input features.",
                "The target is the answer the model tries to predict. For example, house price can be the target when predicting house prices.",
                "In supervised learning, the target variable is the output associated with each training example. Classification targets are categories, while regression targets are usually continuous numerical values."
            )

        # Applications
        if contains_phrase(text, ["applications", "application", "use cases", "used for", "uses of", "where is machine learning used"]):
            return (
                "Machine Learning is used in many areas, such as:\n\n"
                "• Recommendation systems 🎯\n"
                "• Spam and fraud detection\n"
                "• Image and speech recognition\n"
                "• Predictive analysis\n"
                "• Healthcare and finance\n"
                "• Customer behavior analysis"
            )

        # Types of Machine Learning
        if contains_phrase(text, ["types", "type", "categories"]):
            return (
                "The main types of Machine Learning are:\n\n"
                "• Supervised Learning – learns from labelled data.\n"
                "• Unsupervised Learning – finds patterns in unlabelled data.\n"
                "• Reinforcement Learning – learns through rewards and penalties."
            )

        # Algorithms
        if contains_phrase(text, ["algorithm", "algorithms"]) and not contains_phrase(text, [
            "decision tree", "random forest", "knn", "k nearest neighbors", "k-nearest neighbors",
            "support vector machine", "svm", "logistic regression", "linear regression"
        ]):
            return (
                "Common Machine Learning algorithms include:\n\n"
                "• Linear Regression\n"
                "• Logistic Regression\n"
                "• Decision Tree\n"
                "• Random Forest\n"
                "• K-Nearest Neighbors (KNN)\n"
                "• Support Vector Machine (SVM)\n"
                "• K-Means Clustering"
            )

        # Overfitting
        if contains_phrase(text, ["overfitting", "over fit", "over-fit"]):
            return format_answer(
                "Overfitting occurs when a Machine Learning model learns the training data too closely and performs poorly on new data.",
                "Overfitting occurs when a Machine Learning model learns the training data too closely, including noise and small details. It may perform well on training data but poorly on new data.",
                "Overfitting means the model memorizes the training data instead of learning patterns that work well on new data.",
                "Overfitting happens when a model becomes too closely fitted to the training examples and captures noise or random variation. As a result, training performance can be high while performance on unseen data is lower."
            )

        # Underfitting
        if contains_phrase(text, ["underfitting", "under fit", "under-fit"]):
            return format_answer(
                "Underfitting occurs when a Machine Learning model is too simple to learn important patterns in the data.",
                "Underfitting occurs when a Machine Learning model is too simple to learn the important patterns in the data. It usually performs poorly on both training and new data.",
                "Underfitting means the model has not learned enough from the data, so it performs poorly on both training and new examples.",
                "Underfitting occurs when the model has insufficient complexity or useful information to represent the relationships in the data. It can result from an overly simple model, unsuitable features or insufficient training."
            )

        # Model Training
        if contains_phrase(text, ["model training", "what is model training", "training a model", "train a model"]):
            return format_answer(
                "Model training is the process of teaching a Machine Learning model using training data.",
                "Model training is the process of teaching a Machine Learning algorithm using training data. The model learns patterns and relationships that can be used to make predictions on new data.",
                "Model training means teaching a model using examples so it can learn patterns and make predictions.",
                "Model training involves providing training data to a Machine Learning algorithm so that the resulting model can learn relationships between input features and target values when applicable. The trained model can then be evaluated and used on new data."
            )

        # Model Evaluation
        if contains_phrase(text, ["model evaluation", "what is model evaluation", "evaluate a model"]):
            return format_answer(
                "Model evaluation is the process of measuring how well a Machine Learning model performs.",
                "Model evaluation is the process of measuring how well a Machine Learning model performs using suitable evaluation metrics and unseen data.",
                "Model evaluation means checking how well a model works on data it has not used for training.",
                "Model evaluation helps determine how well a trained model performs on appropriate validation or test data. Different metrics are used depending on the task, such as accuracy, precision, recall, F1-score or mean squared error."
            )

        # Accuracy
        if contains_phrase(text, ["what is accuracy", "accuracy in machine learning", "machine learning accuracy"]):
            return format_answer(
                "Accuracy is the proportion of correct predictions made by a Machine Learning model.",
                "Accuracy is a Machine Learning evaluation metric that shows the proportion of correct predictions out of all predictions made by the model.",
                "Accuracy tells us how many predictions the model got correct out of all its predictions.",
                "Accuracy is calculated as the number of correct predictions divided by the total number of predictions. It is commonly used for classification tasks, although it may not fully describe performance when the classes are highly imbalanced."
            )

        # Precision
        if contains_phrase(text, ["what is precision", "precision in machine learning", "machine learning precision"]):
            return format_answer(
                "Precision measures how many of the predictions made as positive were actually positive.",
                "Precision is a classification metric that measures the proportion of true positive predictions among all predictions classified as positive. It is useful when false positive predictions are important.",
                "Precision tells us how many predicted positives were actually correct.",
                "Precision is calculated as True Positives divided by True Positives plus False Positives. A higher precision means that positive predictions contain fewer false positives."
            )

        # Recall
        if contains_phrase(text, ["what is recall", "recall in machine learning", "machine learning recall"]):
            return format_answer(
                "Recall measures how many of the actual positive cases were correctly identified by the model.",
                "Recall is a classification metric that measures the proportion of actual positive cases correctly identified by a model. It is useful when missing positive cases is important.",
                "Recall tells us how many of the real positive cases the model successfully found.",
                "Recall is calculated as True Positives divided by True Positives plus False Negatives. A higher recall means fewer actual positive cases are missed by the model."
            )

        # F1 Score
        if contains_phrase(text, ["f1 score", "f1-score", "f1score", "what is f1"]):
            return format_answer(
                "F1 Score is a metric that combines Precision and Recall into one value.",
                "F1 Score is the harmonic mean of Precision and Recall. It provides a single measure that balances the two metrics, especially when both false positives and false negatives matter.",
                "F1 Score combines precision and recall into one score so we can consider both together.",
                "F1 Score is calculated as 2 × (Precision × Recall) / (Precision + Recall). It can be useful for classification problems where class imbalance makes accuracy less informative."
            )

        # Confusion Matrix
        if contains_phrase(text, ["confusion matrix", "what is confusion matrix"]):
            return format_answer(
                "A Confusion Matrix is a table used to compare predicted classes with actual classes.",
                "A Confusion Matrix summarizes classification results using True Positives, True Negatives, False Positives and False Negatives.",
                "A Confusion Matrix shows where a classification model predicted correctly and where it made mistakes.",
                "For binary classification, a Confusion Matrix contains four main outcomes: True Positive, True Negative, False Positive and False Negative. These values can be used to calculate metrics such as accuracy, precision, recall and F1 Score."
            )

        # Cross Validation
        if contains_phrase(text, ["cross validation", "cross-validation", "what is cross validation"]):
            return format_answer(
                "Cross-validation is a technique for evaluating a Machine Learning model using multiple train-validation splits.",
                "Cross-validation divides the available data into multiple parts and repeatedly trains and validates the model using different parts. This provides a more reliable estimate of model performance.",
                "Cross-validation checks a model several times using different portions of the data instead of relying on one split.",
                "In k-fold cross-validation, the dataset is divided into k folds. The model is trained on k-1 folds and validated on the remaining fold, repeating the process until every fold has been used for validation."
            )

        # Hyperparameter Tuning
        if contains_phrase(text, ["hyperparameter tuning", "tune hyperparameters", "hyperparameter optimization", "hyperparameter optimisation"]):
            return format_answer(
                "Hyperparameter tuning is the process of finding suitable settings for a Machine Learning algorithm before training.",
                "Hyperparameter tuning involves testing different hyperparameter values and selecting settings that provide good model performance on validation data.",
                "Hyperparameter tuning means trying different model settings to find a configuration that works well.",
                "Hyperparameters are settings chosen before or around model training, such as tree depth, number of neighbors or learning rate. Tuning methods include grid search and randomized search, usually evaluated with validation or cross-validation."
            )

        # Hyperparameter
        if contains_phrase(text, ["hyperparameter", "hyperparameters", "what is hyperparameter"]):
            return format_answer(
                "A hyperparameter is a setting chosen to control how a Machine Learning algorithm learns.",
                "A hyperparameter is a configuration value set before or around model training rather than learned directly from the training examples. Examples include learning rate, tree depth and the number of neighbors in KNN.",
                "A hyperparameter is a model setting that we choose to control the learning process.",
                "Hyperparameters influence the behavior of a learning algorithm and are generally selected using validation, cross-validation or tuning procedures. They are different from model parameters, which are learned from data during training."
            )

        # Train-Test Split
        if contains_phrase(text, ["train test split", "train-test split", "training and testing split", "split the data"]):
            return format_answer(
                "Train-test split divides a dataset into training data and testing data.",
                "A train-test split separates data into a training portion used to learn the model and a testing portion used to evaluate it on unseen examples.",
                "It means keeping one part of the data for learning and another part for checking the model.",
                "A common workflow is to train the model on one portion of the dataset and evaluate it on a separate portion. The exact split ratio depends on the dataset and problem, and the test set should not be used to tune the final model."
            )

        # Bias and Variance
        if contains_phrase(text, ["bias and variance", "bias variance", "what is bias and variance"]):
            return format_answer(
                "Bias is error from an overly simple model, while variance is error from a model that is too sensitive to the training data.",
                "In Machine Learning, high bias is commonly associated with underfitting, while high variance is commonly associated with overfitting. The goal is to balance the two for good generalization.",
                "Bias happens when a model is too simple; variance happens when it changes too much based on the training data.",
                "The bias-variance trade-off describes the balance between a model that is too simple and one that is too sensitive to the training examples. High bias can lead to underfitting, while high variance can lead to overfitting."
            )

        # Feature Scaling
        if contains_phrase(text, ["feature scaling", "what is feature scaling", "scale features", "scaling features"]):
            return format_answer(
                "Feature scaling puts numerical features onto comparable scales.",
                "Feature scaling transforms numerical input features so that their ranges or distributions are more comparable. It can be important for algorithms that are sensitive to feature magnitude, such as KNN and SVM.",
                "Feature scaling makes numerical features easier for some algorithms to compare fairly.",
                "Common feature-scaling methods include normalization and standardization. Scaling can help distance-based and gradient-based algorithms, while some tree-based algorithms are generally less sensitive to feature scale."
            )

        # Normalization
        if contains_phrase(text, ["normalization", "what is normalization", "normalize data"]):
            return format_answer(
                "Normalization is a scaling method that commonly transforms values to a fixed range such as 0 to 1.",
                "Min-max normalization commonly transforms a feature so that its values fall within a chosen range, often 0 to 1. It can be useful when features have different numerical ranges.",
                "Normalization changes values to a common range, often between 0 and 1.",
                "A common min-max normalization formula is (x - minimum) / (maximum - minimum). The appropriate scaling method depends on the data and the Machine Learning algorithm."
            )

        # Standardization
        if contains_phrase(text, ["standardization", "what is standardization", "standardize data", "standardisation"]):
            return format_answer(
                "Standardization transforms a feature so it is centered around a mean of 0 with a standard deviation of 1.",
                "Standardization commonly transforms a numerical feature using its mean and standard deviation, producing a standardized value with an approximately zero-centered scale.",
                "Standardization changes data using the mean and standard deviation so features are on a comparable scale.",
                "A common standardization formula is (x - mean) / standard deviation. Standardization is often used with algorithms where feature magnitude affects learning or distance calculations."
            )

        # Decision Tree
        if contains_phrase(text, ["decision tree", "decision trees", "what is decision tree"]):
            return format_answer(
                "A Decision Tree is a Machine Learning model that makes predictions using a sequence of decision rules.",
                "A Decision Tree splits data into branches using feature-based rules and reaches a prediction at a leaf node. It can be used for classification and regression.",
                "A Decision Tree makes decisions step by step, like a flowchart, until it reaches a final prediction.",
                "Decision Trees recursively split data according to selected feature conditions. Internal nodes represent decisions, branches represent outcomes of those decisions, and leaf nodes provide the final prediction."
            )

        # Random Forest
        if contains_phrase(text, ["random forest", "random forests", "what is random forest"]):
            return format_answer(
                "Random Forest is an ensemble Machine Learning method that combines predictions from multiple Decision Trees.",
                "Random Forest builds multiple Decision Trees using different samples or feature selections and combines their predictions. It can be used for both classification and regression.",
                "Random Forest combines many Decision Trees to make a more robust prediction than one tree alone.",
                "Random Forest is an ensemble approach. For classification, trees typically vote on the predicted class; for regression, their predictions can be averaged. Using multiple trees can reduce the effect of individual-tree variation."
            )

        # KNN
        if contains_phrase(text, ["knn", "k nearest neighbors", "k-nearest neighbors", "nearest neighbors", "what is knn"]):
            return format_answer(
                "KNN predicts an observation using the labels or values of nearby data points.",
                "K-Nearest Neighbors (KNN) is a supervised Machine Learning algorithm that makes predictions based on the closest training examples according to a distance measure.",
                "KNN looks at nearby examples and uses them to decide the prediction.",
                "In KNN classification, the most common class among the selected nearest neighbors can be used as the prediction. In regression, the neighboring target values can be combined, often using an average. Feature scaling is commonly important because distance is used."
            )

        # SVM
        if contains_phrase(text, ["support vector machine", "support vector machines", "svm", "what is svm"]):
            return format_answer(
                "SVM is a supervised Machine Learning algorithm that finds a decision boundary between classes.",
                "Support Vector Machine (SVM) is a supervised learning algorithm that finds a boundary that separates classes while aiming for a suitable margin between them.",
                "SVM finds a boundary that separates different classes of data.",
                "SVM can be used for classification and related tasks. The algorithm identifies a decision boundary using important training observations called support vectors, and kernels can be used to represent certain nonlinear relationships."
            )

        # Logistic Regression
        if contains_phrase(text, ["logistic regression", "logistic regressor", "what is logistic regression"]):
            return format_answer(
                "Logistic Regression is a supervised Machine Learning algorithm commonly used for classification.",
                "Logistic Regression models the probability of a class and is commonly used for binary classification, with extensions available for multiple classes.",
                "Logistic Regression predicts the probability of a category, such as spam or not spam.",
                "Logistic Regression applies a logistic function to a weighted combination of input features to estimate class probabilities. A decision rule can then be used to assign a class based on the predicted probability."
            )

        # Linear Regression
        if contains_phrase(text, ["linear regression", "linear regressor", "what is linear regression"]):
            return format_answer(
                "Linear Regression is a supervised Machine Learning algorithm used to predict numerical values.",
                "Linear Regression models the relationship between input features and a continuous target using a linear equation.",
                "Linear Regression predicts a number, such as house price, using a linear relationship between features and the target.",
                "Linear Regression estimates coefficients for a linear equation so that the model can predict a continuous numerical target. It is commonly used as a basic regression method and can include one or multiple input features."
            )

        # Mean Absolute Error
        if contains_phrase(text, ["mean absolute error", "mae", "what is mae"]):
            return format_answer(
                "Mean Absolute Error (MAE) measures the average absolute difference between actual and predicted values.",
                "MAE is a regression evaluation metric calculated as the average of the absolute errors between predicted and actual target values. Lower MAE indicates smaller average prediction errors.",
                "MAE tells us the average size of the prediction error without considering whether the error is positive or negative.",
                "Mean Absolute Error is calculated by taking the absolute difference between each actual and predicted value and then averaging those differences. It is expressed in the same units as the target variable."
            )

        # Mean Squared Error
        if contains_phrase(text, ["mean squared error", "mse", "what is mse"]):
            return format_answer(
                "Mean Squared Error (MSE) measures the average of squared prediction errors.",
                "MSE is a regression metric calculated by averaging the squared differences between actual and predicted values. Squaring gives larger errors more influence on the metric.",
                "MSE finds the average squared difference between what the model predicted and the actual value.",
                "Mean Squared Error is useful for comparing regression models. Because errors are squared, larger mistakes contribute more strongly to the final value. Lower MSE indicates smaller squared prediction errors."
            )

        # Root Mean Squared Error
        if contains_phrase(text, ["root mean squared error", "rmse", "what is rmse"]):
            return format_answer(
                "Root Mean Squared Error (RMSE) is the square root of Mean Squared Error.",
                "RMSE is a regression evaluation metric that measures the typical size of prediction errors while giving larger errors more influence because the errors are squared before taking the root.",
                "RMSE is the square root of MSE and shows prediction error in the same units as the target.",
                "RMSE is calculated by taking the square root of the average squared differences between actual and predicted values. Lower RMSE generally indicates better predictive accuracy for the same target and dataset."
            )

        # R-squared
        if contains_phrase(text, ["r squared", "r-squared", "r2 score", "r2", "coefficient of determination"]):
            return format_answer(
                "R-squared is a regression metric that describes how much variation in the target is explained by a model relative to a baseline.",
                "R-squared, also called the coefficient of determination, is commonly used to evaluate regression models by comparing the model's residual variation with the variation around the target mean.",
                "R-squared gives an indication of how well a regression model explains variation in the target compared with a simple baseline.",
                "R-squared is often interpreted using values relative to a baseline, but its meaning depends on the model, data and evaluation setup. It should be considered together with other regression metrics and domain context."
            )

        # Loss Function
        if contains_phrase(text, ["loss function", "what is loss function", "loss in machine learning"]):
            return format_answer(
                "A loss function measures how different a model's predictions are from the expected outputs.",
                "A loss function assigns a numerical value to prediction error during training. Learning algorithms use the loss to guide parameter updates toward better predictions.",
                "A loss function tells the model how wrong its predictions are so the learning process can improve them.",
                "Different tasks use different loss functions. Examples include Mean Squared Error for regression and cross-entropy loss for many classification models. During training, optimization methods try to reduce the selected loss."
            )

        # Gradient Descent
        if contains_phrase(text, ["gradient descent", "what is gradient descent"]):
            return format_answer(
                "Gradient Descent is an optimization method used to reduce a model's loss by updating parameters step by step.",
                "Gradient Descent uses the gradient of a loss function to determine a direction for updating model parameters so that the loss can decrease.",
                "Gradient Descent improves a model by repeatedly changing its parameters in a direction that reduces error.",
                "Gradient Descent starts with parameter values and repeatedly calculates how the loss changes with respect to those parameters. It then updates the parameters using a learning rate that controls the step size."
            )

        # Learning Rate
        if contains_phrase(text, ["learning rate", "what is learning rate"]):
            return format_answer(
                "Learning rate is a hyperparameter that controls the size of parameter updates during optimization.",
                "The learning rate determines how large each update is when an optimization method such as Gradient Descent changes model parameters during training.",
                "Learning rate controls how big a step the model takes while learning.",
                "A learning rate that is too large can cause unstable updates, while one that is too small can make training slow. The suitable value depends on the model, data and optimization method."
            )

        # Regularization
        if contains_phrase(text, ["regularization", "regularisation", "what is regularization"]):
            return format_answer(
                "Regularization is a technique used to reduce overfitting by discouraging overly complex model solutions.",
                "Regularization adds a penalty related to model complexity to the training objective. Common forms include L1 and L2 regularization.",
                "Regularization helps stop a model from becoming too complex and fitting the training data too closely.",
                "L1 regularization can encourage some coefficients to become exactly zero, while L2 regularization penalizes large coefficients. The regularization strength is typically treated as a hyperparameter."
            )

        # Data Leakage
        if contains_phrase(text, ["data leakage", "data leak", "what is data leakage"]):
            return format_answer(
                "Data leakage occurs when information that should not be available during training is used by a model.",
                "Data leakage happens when information from outside the appropriate training process, often from the validation or test data, influences model training or feature creation. It can make evaluation results look better than real-world performance.",
                "Data leakage means the model accidentally gets information it should not have while learning.",
                "Examples include using future information to predict the past or calculating features using the full dataset before splitting it. Leakage can produce overly optimistic validation or test performance."
            )

        # Feature Engineering
        if contains_phrase(text, ["feature engineering", "feature engineering in machine learning", "what is feature engineering"]):
            return format_answer(
                "Feature Engineering is the process of creating, transforming or selecting useful input features for a Machine Learning model.",
                "Feature Engineering uses domain knowledge and data-processing techniques to create informative features from raw data, which can help a model learn useful patterns.",
                "Feature Engineering means preparing or creating better inputs so the Machine Learning model can learn more effectively.",
                "Feature Engineering can include transformations, extracting information from dates or text, combining variables, encoding categories and selecting useful features. The process should avoid information leakage."
            )

        # Dimensionality Reduction
        if contains_phrase(text, ["dimensionality reduction", "what is dimensionality reduction"]):
            return format_answer(
                "Dimensionality Reduction reduces the number of input variables while trying to preserve useful information.",
                "Dimensionality Reduction transforms high-dimensional data into a lower-dimensional representation. It can simplify visualization, reduce computation and sometimes help with noise or redundancy.",
                "Dimensionality Reduction means reducing the number of features while keeping important information from the data.",
                "Common dimensionality-reduction techniques include Principal Component Analysis (PCA) and some manifold-learning methods. The appropriate technique depends on the data and purpose of the analysis."
            )

        # PCA
        if contains_phrase(text, ["principal component analysis", "pca", "what is pca"]):
            return format_answer(
                "PCA is a dimensionality-reduction technique that creates new components from the original features.",
                "Principal Component Analysis (PCA) transforms correlated numerical features into a smaller set of components that capture important directions of variation in the data.",
                "PCA reduces many features into fewer new components while trying to retain important variation in the data.",
                "PCA is commonly used for dimensionality reduction and visualization. The resulting principal components are combinations of the original numerical features and are ordered by the amount of variance they capture."
            )

        # Ensemble Learning
        if contains_phrase(text, ["ensemble learning", "what is ensemble learning"]):
            return format_answer(
                "Ensemble Learning combines predictions from multiple models to produce a final prediction.",
                "Ensemble Learning uses multiple learners and combines their outputs to improve robustness or predictive performance. Random Forest is an example based on multiple Decision Trees.",
                "Ensemble Learning combines several models instead of relying on only one model.",
                "Common ensemble approaches include bagging, boosting and stacking. The way models are trained and their predictions are combined depends on the ensemble method."
            )

        # Bagging
        if contains_phrase(text, ["bagging", "bootstrap aggregating", "what is bagging"]):
            return format_answer(
                "Bagging is an ensemble technique that trains models on different bootstrap samples and combines their predictions.",
                "Bagging, short for Bootstrap Aggregating, creates multiple training samples by sampling with replacement, trains separate models and combines their predictions.",
                "Bagging trains several models on different sampled versions of the data and combines their results.",
                "Bagging can reduce the variance of unstable learners. Random Forest is a well-known ensemble method that builds on the idea of combining many decision trees with additional randomization."
            )

        # Boosting
        if contains_phrase(text, ["boosting", "what is boosting"]):
            return format_answer(
                "Boosting is an ensemble technique that builds models sequentially, with later models focusing on errors made by earlier models.",
                "Boosting combines a sequence of relatively simple learners so that later learners improve the combined model by emphasizing observations or residual errors that previous learners handled poorly.",
                "Boosting builds models one after another, with each new model helping correct earlier mistakes.",
                "Boosting is used in methods such as Gradient Boosting and related algorithms. The exact way errors are emphasized and models are combined depends on the boosting method."
            )

        # Epoch
        if contains_phrase(text, ["epoch", "epochs", "what is epoch"]):
            return format_answer(
                "An epoch is one complete pass through the training dataset during model training.",
                "In iterative Machine Learning training, an epoch represents one complete pass through all training examples. Multiple epochs may be used so the model can update its parameters repeatedly.",
                "One epoch means the model has gone through the training data once.",
                "The number of epochs is a training setting that depends on the model, dataset and optimization process. Too few epochs may leave the model under-trained, while excessive training can contribute to overfitting in some settings."
            )

        # Class Imbalance
        if contains_phrase(text, [
            "class imbalance", "imbalanced data", "imbalanced dataset",
            "what is class imbalance", "imbalanced classes"
        ]):
            return format_answer(
                "Class imbalance occurs when some classes have many more examples than others.",
                "Class imbalance occurs when the classes in a classification dataset are unevenly represented. It can make accuracy misleading and may require suitable metrics or sampling strategies.",
                "Class imbalance means one class has many more examples than another class.",
                "With imbalanced classification data, a model may perform well on the majority class while missing the minority class. Metrics such as precision, recall, F1-score and appropriate validation strategies can provide more useful information than accuracy alone."
            )

        # Sensitivity
        if contains_phrase(text, [
            "sensitivity", "what is sensitivity", "sensitivity in machine learning"
        ]):
            return format_answer(
                "Sensitivity measures the proportion of actual positive cases correctly identified.",
                "Sensitivity is another name commonly used for Recall. It measures the proportion of actual positive cases that a classification model correctly identifies.",
                "Sensitivity tells us how many of the real positive cases the model found.",
                "Sensitivity is commonly calculated as True Positives divided by True Positives plus False Negatives. It is especially relevant when failing to identify a positive case has important consequences."
            )

        # Specificity
        if contains_phrase(text, [
            "specificity", "what is specificity", "specificity in machine learning"
        ]):
            return format_answer(
                "Specificity measures the proportion of actual negative cases correctly identified.",
                "Specificity is the proportion of actual negative cases that are correctly identified by a classification model.",
                "Specificity tells us how many of the real negative cases the model correctly found.",
                "Specificity is commonly calculated as True Negatives divided by True Negatives plus False Positives. It helps describe how well a classifier identifies negative cases."
            )

        # ROC Curve
        if contains_phrase(text, [
            "roc curve", "what is roc curve", "receiver operating characteristic",
            "roc in machine learning"
        ]):
            return format_answer(
                "A ROC Curve shows the trade-off between True Positive Rate and False Positive Rate at different classification thresholds.",
                "A Receiver Operating Characteristic (ROC) Curve plots True Positive Rate against False Positive Rate across different classification thresholds.",
                "A ROC Curve helps us see how a classifier behaves at different decision thresholds.",
                "The ROC Curve is commonly used for binary classification to study the trade-off between sensitivity or True Positive Rate and False Positive Rate across thresholds. It can be summarized using the Area Under the Curve (AUC)."
            )

        # AUC
        if contains_phrase(text, [
            "auc", "what is auc", "area under curve", "area under the curve"
        ]):
            return format_answer(
                "AUC is the Area Under the ROC Curve and summarizes ranking performance across classification thresholds.",
                "AUC, or Area Under the ROC Curve, is a metric commonly used to summarize how well a classifier separates positive and negative classes across different thresholds.",
                "AUC is a value related to the ROC Curve that summarizes how well a classifier separates the classes.",
                "ROC-AUC measures the area under the Receiver Operating Characteristic curve. It evaluates ranking or discrimination across thresholds and should be interpreted with the problem context and class distribution."
            )

        # Naive Bayes
        if contains_phrase(text, [
            "naive bayes", "naive bayes classifier", "what is naive bayes"
        ]):
            return format_answer(
                "Naive Bayes is a supervised probabilistic Machine Learning algorithm based on Bayes' theorem.",
                "Naive Bayes is a family of supervised classification algorithms based on Bayes' theorem with a simplifying assumption about feature independence.",
                "Naive Bayes predicts a class using probabilities calculated from the training data.",
                "Naive Bayes applies Bayes' theorem to estimate class probabilities while making a simplifying conditional-independence assumption about features. It is commonly used for classification tasks such as text classification."
            )

        # K-Means
        if contains_phrase(text, [
            "k means", "k-means", "what is k means", "what is k-means"
        ]):
            return format_answer(
                "K-Means is an unsupervised clustering algorithm that groups data into a chosen number of clusters.",
                "K-Means is an unsupervised Machine Learning algorithm that assigns observations to clusters based on their distance from cluster centroids.",
                "K-Means groups similar data points into a chosen number of groups.",
                "K-Means begins with a selected number of clusters, assigns observations to the nearest centroid, updates the centroids and repeats the process until the assignments stabilize or a stopping condition is reached."
            )

        # DBSCAN
        if contains_phrase(text, [
            "dbscan", "what is dbscan"
        ]):
            return format_answer(
                "DBSCAN is an unsupervised clustering algorithm that groups dense regions of data and can identify noise points.",
                "DBSCAN, or Density-Based Spatial Clustering of Applications with Noise, forms clusters from dense regions and can label isolated observations as noise.",
                "DBSCAN finds groups based on data density and can mark unusual points as noise.",
                "DBSCAN uses neighborhood density to form clusters rather than requiring the number of clusters in advance. It can identify noise or outlier observations and is useful when clusters have suitable density-based structure."
            )

        # Gradient Boosting
        if contains_phrase(text, [
            "gradient boosting", "what is gradient boosting"
        ]):
            return format_answer(
                "Gradient Boosting builds models sequentially, with later models helping correct earlier errors.",
                "Gradient Boosting is an ensemble technique that builds models sequentially, with each new model focusing on reducing errors made by the existing ensemble.",
                "Gradient Boosting builds several models one after another, with each new model helping improve the previous result.",
                "Gradient Boosting combines a sequence of relatively simple models, commonly decision trees. Each stage is fitted to improve the current ensemble by reducing a chosen loss function."
            )

        # XGBoost
        if contains_phrase(text, [
            "xgboost", "xg boost", "what is xgboost"
        ]):
            return format_answer(
                "XGBoost is a gradient boosting implementation widely used for structured-data Machine Learning tasks.",
                "XGBoost is an optimized gradient boosting library that builds an ensemble of decision trees sequentially and includes techniques for efficient and regularized learning.",
                "XGBoost is a Machine Learning method based on gradient boosting and decision trees.",
                "XGBoost is a scalable implementation of gradient boosting that builds decision-tree ensembles sequentially. It includes regularization and engineering optimizations that can make it effective for many structured-data problems."
            )

        # Bagging vs Boosting
        if (
            contains_phrase(text, ["difference", "different", "distinguish", "vs", "versus"])
            and contains_phrase(text, ["bagging", "boosting"])
        ):
            return format_answer(
                "Bagging builds models independently and combines them, while Boosting builds models sequentially to improve errors.",
                "Bagging trains multiple models using different samples and combines their predictions, while Boosting builds models sequentially so later models focus on improving the ensemble.",
                "Bagging builds many models separately and combines them. Boosting builds models one after another to improve the result.",
                "Bagging is an ensemble strategy that can reduce variance by combining models trained on different samples. Boosting builds models sequentially, with each stage contributing to reducing errors according to the chosen boosting method."
            )

        # Ensemble Learning vs Single Model
        if contains_phrase(text, [
            "ensemble learning", "what is ensemble learning"
        ]):
            return format_answer(
                "Ensemble Learning combines multiple models to produce a final prediction.",
                "Ensemble Learning combines predictions from multiple models to create a final prediction, often improving robustness or predictive performance.",
                "Ensemble Learning means using several models together instead of relying on only one model.",
                "Ensemble methods combine multiple base learners. Bagging, Random Forest and Boosting are common ensemble approaches, with the exact combination strategy depending on the method."
            )

        # Model Deployment
        if contains_phrase(text, [
            "model deployment", "deploy a model", "deploy machine learning model",
            "what is model deployment"
        ]):
            return format_answer(
                "Model deployment is the process of making a trained Machine Learning model available for real-world use.",
                "Model deployment involves integrating a trained Machine Learning model into an application, service or workflow so it can receive new data and produce predictions.",
                "Deployment means putting the trained model into a system where it can be used to make predictions.",
                "After a model is trained and evaluated, deployment can expose it through an application, API, batch process or other production workflow. Monitoring and maintenance may be needed after deployment."
            )

        # Model Monitoring
        if contains_phrase(text, [
            "model monitoring", "monitor a model", "machine learning model monitoring",
            "what is model monitoring"
        ]):
            return format_answer(
                "Model monitoring checks whether a deployed Machine Learning model continues to work as expected.",
                "Model monitoring tracks a deployed model's performance, data quality and other useful signals to identify problems after deployment.",
                "Model monitoring means checking a model after deployment to make sure it still works properly.",
                "Monitoring can include tracking prediction quality when labels become available, input-data changes, data drift, system errors and other operational signals. It helps identify when a model may need investigation or retraining."
            )

        # Model Drift
        if contains_phrase(text, [
            "model drift", "data drift", "concept drift", "what is data drift",
            "what is model drift"
        ]):
            return format_answer(
                "Data or model drift refers to changes that can reduce the usefulness of a deployed Machine Learning model.",
                "Data drift occurs when the distribution of input data changes over time, while concept drift can involve changes in the relationship between inputs and the target.",
                "Drift means the real-world data or patterns can change after a model is trained.",
                "A deployed model may encounter data distributions or relationships that differ from those present during training. Monitoring these changes can help determine whether the model should be investigated, recalibrated or retrained."
            )

        # General Machine Learning answer
        return format_answer(
            "Machine Learning allows computers to learn patterns from data and make predictions or decisions.",
            "Machine Learning is a branch of AI where algorithms learn patterns from data instead of being explicitly programmed for every decision.",
            "Machine Learning means teaching a computer to learn patterns from examples or data so it can make predictions or decisions.",
            "Machine Learning is a branch of Artificial Intelligence in which algorithms learn patterns from data. Depending on the problem, models can be used for prediction, classification, clustering or other tasks. The usual process includes preparing data, selecting features, training a model, evaluating it and improving it."
        )

    # ------------------------------------------------------------
    # NLP
    # ------------------------------------------------------------
    if contains_phrase(text, [
        "nlp", "natural language processing", "text processing"
    ]):
        return format_answer(
            "NLP helps computers understand and process human language.",
            "Natural Language Processing (NLP) is a field of AI that helps computers process human language. Examples include chatbots, translation and sentiment analysis.",
            "NLP means teaching computers to work with human language, such as text and speech.",
            "Natural Language Processing, or NLP, is a field of AI concerned with processing and understanding human language. Common techniques include tokenization, stemming, lemmatization, text classification, sentiment analysis and information extraction."
        )

    # ------------------------------------------------------------
    # SQL / DATABASES
    # ------------------------------------------------------------
    if contains_phrase(text, [
        "sql", "database", "dbms", "mysql", "postgresql"
    ]):
        if contains_phrase(text, [
            "select", "query", "queries", "join", "joins"
        ]):
            return (
                "SQL is used to work with relational databases. Common commands "
                "include SELECT, INSERT, UPDATE and DELETE. JOIN is used to "
                "combine related data from tables."
            )

        if contains_phrase(text, ["database", "dbms"]):
            return format_answer(
                "A database is an organized collection of data that can be stored and managed efficiently.",
                "A database is an organized collection of data that can be stored, retrieved and managed efficiently. Examples include MySQL and PostgreSQL.",
                "A database is simply a place where data is organized and stored so that we can easily find and manage it.",
                "A database is an organized collection of data designed for efficient storage, retrieval and management. Database Management Systems such as MySQL and PostgreSQL provide tools for creating tables, storing records, querying data and managing relationships."
            )

        return format_answer(
            "SQL is a language used to store, retrieve and manage data in relational databases.",
            "SQL (Structured Query Language) is used to create, read, update and manage data in relational databases such as MySQL and PostgreSQL.",
            "SQL is a language used to communicate with databases. It can be used to add, find, change and delete data.",
            "SQL is a standard language for interacting with relational databases. It can be used to create tables, insert and update records, retrieve information with SELECT queries, filter data with WHERE, group data with GROUP BY, and combine tables using JOIN operations."
        )

    # ------------------------------------------------------------
    # DATA STRUCTURES / PROGRAMMING BASICS
    # ------------------------------------------------------------
    if contains_phrase(text, [
        "data structure", "data structures", "array",
        "list", "stack", "queue"
    ]):
        return (
            "A data structure is a way of organizing and storing data so it "
            "can be used efficiently. Common examples are arrays, linked "
            "lists, stacks, queues, trees and graphs."
        )

    if contains_phrase(text, [
        "oops", "oop", "object oriented programming",
        "object oriented", "object-oriented"
    ]):
        return (
            "OOP means Object-Oriented Programming. Its common concepts are "
            "Encapsulation, Inheritance, Polymorphism and Abstraction. "
            "These concepts help organize programs using classes and objects."
        )

    # ------------------------------------------------------------
    # RECURSION
    # ------------------------------------------------------------
    if contains_phrase(text, ["recursion", "recursive"]):
        return format_answer(
            "Recursion is when a function calls itself to solve a problem.",
            "Recursion is a programming technique where a function calls itself with a smaller part of the problem. It needs a base condition to stop.",
            "Recursion means a function solves a problem by calling itself again on a smaller version of the same problem. A stopping condition is required.",
            "Recursion is a programming technique in which a function calls itself to solve smaller instances of the same problem. Every recursive solution should have a base case that stops further calls. Recursion is commonly used for tasks such as traversing trees, processing nested structures and solving divide-and-conquer problems."
        )

    # ------------------------------------------------------------
    # PROJECTS / INTERNSHIPS / CAREER
    # ------------------------------------------------------------
    if contains_phrase(text, ["project", "projects"]):
        return (
            "A good student project should solve a clear problem and demonstrate "
            "practical skills. 💡\n\n"
            "For example: a Data Science project can include data cleaning, EDA, "
            "visualization, Machine Learning and a simple dashboard or application."
        )

    if contains_phrase(text, ["internship", "internships", "intern"]):
        return (
            "An internship gives students practical exposure to real or realistic "
            "work. 💼\n\n"
            "Useful things to focus on are learning the tools, completing projects, "
            "documenting your work, and keeping your GitHub and resume updated."
        )

    if contains_phrase(text, ["resume", "cv", "curriculum vitae"]):
        return (
            "For a fresher resume, keep it clear and preferably one page. Include "
            "your education, technical skills, projects, internships, certifications "
            "and relevant achievements. Use measurable project details where possible."
        )

    # ------------------------------------------------------------
    # STUDY TIPS
    # ------------------------------------------------------------
    if contains_phrase(text, [
        "study tips", "how to study", "study better",
        "exam preparation", "prepare for exam"
    ]):
        return (
            "Try this simple study routine 📚:\n\n"
            "1. Break the syllabus into small topics.\n"
            "2. Study one topic at a time.\n"
            "3. Make short notes.\n"
            "4. Practice questions instead of only reading.\n"
            "5. Revise regularly and take short breaks."
        )

    # ------------------------------------------------------------
    # GENERAL DEFINITION REQUEST
    # ------------------------------------------------------------
    if contains_phrase(text, ["what is", "define", "meaning of", "explain"]):
        return (
            "I can explain that, but I don't have a predefined explanation "
            "for this topic yet. 😊\n\n"
            "Try asking about Python, Python libraries, Data Science, "
            "Machine Learning, NLP, SQL, databases, recursion, programming, "
            "projects, internships or study topics."
        )

    # ------------------------------------------------------------
    # FALLBACK
    # ------------------------------------------------------------
    return (
        "I'm a rule-based student chatbot, so I currently answer questions "
        "from my supported topics. 🤖\n\n"
        "Try asking me about **Python, Python libraries, Data Science, "
        "Machine Learning, NLP, SQL, databases, recursion, projects, "
        "internships or study tips**."
    )


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"],
        avatar="🤖" if message["role"] == "assistant" else "👤"
    ):

        st.markdown(message["content"])


# ============================================================
# QUICK QUESTIONS
# ============================================================

st.markdown(
    '<div class="section-title">⚡ Quick Questions</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)


with col1:

    python_button = st.button(
        "🐍 Python",
        use_container_width=True
    )


with col2:

    ds_button = st.button(
        "📊 Data Science",
        use_container_width=True
    )


with col3:

    ml_button = st.button(
        "🤖 Machine Learning",
        use_container_width=True
    )


col4, col5, col6 = st.columns(3)


with col4:

    internship_button = st.button(
        "💼 Internship",
        use_container_width=True
    )


with col5:

    project_button = st.button(
        "🧑‍💻 Projects",
        use_container_width=True
    )


with col6:

    study_button = st.button(
        "📚 Study Tips",
        use_container_width=True
    )


# ============================================================
# PROCESS QUICK QUESTION
# ============================================================

quick_question = None

if python_button:
    quick_question = "Tell me about Python"

elif ds_button:
    quick_question = "What is Data Science?"

elif ml_button:
    quick_question = "What is Machine Learning?"

elif internship_button:
    quick_question = "Tell me about internships"

elif project_button:
    quick_question = "Tell me about projects"

elif study_button:
    quick_question = "Give me study tips"


if quick_question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": quick_question
        }
    )

    response = get_response(quick_question)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    st.rerun()


# ============================================================
# CHAT INPUT
# ============================================================

user_input = st.chat_input(
    "💬 Ask me something..."
)


if user_input:

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Generate response
    response = get_response(user_input)

    # Add assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    # Refresh application
    st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<style>

    /* =========================
       MAIN APP
       ========================= */

    .stApp {
        background: linear-gradient(135deg, #f5f7ff 0%, #eef2ff 100%);
    }

    .block-container {
        max-width: 1000px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* =========================
       HEADER
       ========================= */

    .main-header {
        text-align: center;
        padding: 30px 25px;
        border-radius: 24px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.30);
        margin-bottom: 30px;
    }

    .main-header h1 {
        color: #ffffff !important;
        font-size: 2.5rem;
        margin: 0 0 10px 0;
        font-weight: 800;
    }

    .main-header p {
        color: #f5f7ff !important;
        font-size: 1rem;
        margin: 0;
    }


    /* =========================
       SECTION TITLE
       ========================= */

    .section-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #343a70 !important;
        margin-top: 25px;
        margin-bottom: 14px;
    }


    /* =========================
       CHAT MESSAGES
       ========================= */

    [data-testid="stChatMessage"] {
        border-radius: 16px;
        padding: 10px 14px;
        margin-bottom: 12px;
    }

    [data-testid="stChatMessageContent"] {
        color: #1f2937 !important;
    }

    [data-testid="stChatMessageContent"] p {
        color: #1f2937 !important;
    }

    [data-testid="stChatMessageContent"] strong {
        color: #111827 !important;
    }

    [data-testid="stChatMessageContent"] li {
        color: #1f2937 !important;
    }

    [data-testid="stChatMessageContent"] ul,
    [data-testid="stChatMessageContent"] ol {
        color: #1f2937 !important;
    }


    /* =========================
       QUICK QUESTION BUTTONS
       ========================= */

    .stButton > button {
        width: 100%;
        border-radius: 14px;
        border: 1px solid #d8dcff;
        background: #ffffff;
        color: #4b4f8a !important;
        font-weight: 600;
        padding: 11px;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        border-color: #667eea;
        color: #667eea !important;
        background: #f5f6ff;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.15);
    }


    /* =========================
       CHAT INPUT
       ========================= */

    [data-testid="stChatInput"] {
        border-radius: 18px;
    }

    [data-testid="stChatInput"] textarea,
    [data-testid="stChatInput"] textarea:focus {
        color: #111827 !important;
        -webkit-text-fill-color: #111827 !important;
        caret-color: #111827 !important;
        background-color: #ffffff !important;
        opacity: 1 !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #6b7280 !important;
        -webkit-text-fill-color: #6b7280 !important;
        opacity: 1 !important;
    }


    /* =========================
       SIDEBAR
       ========================= */

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #171a3a 0%, #242858 100%);
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    .sidebar-title {
        font-size: 1.35rem;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .sidebar-subtitle {
        font-size: 0.9rem;
        opacity: 0.8;
        margin-bottom: 25px;
    }

    .feature-card {
        background: rgba(255, 255, 255, 0.08);
        padding: 13px;
        border-radius: 12px;
        margin-bottom: 10px;
        border: 1px solid rgba(255, 255, 255, 0.12);
    }


    /* =========================
       STATUS CARD
       ========================= */

    .status-card {
        background: rgba(46, 204, 113, 0.15);
        border: 1px solid rgba(46, 204, 113, 0.35);
        padding: 12px;
        border-radius: 12px;
        margin-top: 20px;
    }


    /* =========================
       FOOTER
       ========================= */

    .footer {
        text-align: center;
        color: #6b7280 !important;
        font-size: 0.85rem;
        margin-top: 35px;
        padding: 15px;
    }

</style>
""", unsafe_allow_html=True)