import tkinter as tk
from tkinter import messagebox
from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime

# Função para buscar os dados do clima
def buscar_clima():
    try:
        url = "https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/558/saopaulo-sp" #Site utilizado para fazer a previsão do tempo
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        temperatura = soup.find("span", class_= "-bold").text.strip()
        umidade = soup.find("span", class_= "-gray-light").text.strip()

        resultado_label.config(
            text=f"Clima em São Paulo:\n"
                 f"Temperatura:{temperatura}C\n"
                 f"Umidade:{umidade}\n"
        )
        return {
            "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "cidade": "São Paulo",
            "temperatura": temperatura,
            "umidade": umidade,
        }
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao obter dados: {e}")

# Função para salvar os dados em um arquivo JSON possibilitando futura manipulação
def salvar_dados():
    dados = buscar_clima()
    if dados:
        try:
            try:
                with open("historico_clima.json", "r", encoding="utf-8") as arquivo:
                    historico = json.load(arquivo)
            except FileNotFoundError:
                historico = []
                
            historico.append(dados)

            # Salva o arquivo JSON com os dados da busca e muda a manipulação do arquivo para Escrita
            with open("historico_clima.json", "w", encoding="utf-8") as arquivo:
                json.dump(historico, arquivo, indent=4, ensure_ascii=False)

            messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar dados: {e}")

# Interface gráfica com Tkinter
app = tk.Tk()
app.title("Previsão do Tempo - São Paulo")

titulo_label = tk.Label(app, text="Previsão do tempo em São Paulo", font=("Arial", 16))
titulo_label.pack(pady=10)

resultado_label = tk.Label(app, text="Clique no botão para obter a previsão.", font=("Arial", 12))
resultado_label.pack(pady=10)

buscar_botao = tk.Button(app, text="Obter temperatura", command=buscar_clima, bg="#3674B5", fg="white",border=1)
buscar_botao.pack(pady=5)

salvar_btn = tk.Button(app, text="Salvar Dados", command=salvar_dados, bg="#578FCA", fg="white",border=1)
salvar_btn.pack(pady=5)

app.mainloop()