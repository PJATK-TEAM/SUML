FROM continuumio/miniconda3:latest

WORKDIR /app

COPY environment.yml .

RUN conda env create -f environment.yml

COPY . .

EXPOSE 8501

ENTRYPOINT ["conda", "run", "-n", "bird-drone-classifier-front"]
CMD ["streamlit", "run", "main.py"]