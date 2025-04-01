from setuptools import setup, find_packages

setup(
    name="basic_llm_call",
    version="0.1.0",
    package_dir={"basic_llm_call": "src"},
    packages=["basic_llm_call", "basic_llm_call.core", "basic_llm_call.tools"],
    install_requires=[
        "openai>=1.0.0",
        "python-dotenv>=0.19.0",
        "tenacity>=8.0.0",
        "pytz>=2021.1",
        "pydantic>=2.0.0",
        "typing-extensions>=4.0.0"
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "black>=21.0.0",
            "isort>=5.0.0",
            "mypy>=0.900"
        ]
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A framework for handling tool-enabled conversations with Azure OpenAI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/basic-llm-call",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)