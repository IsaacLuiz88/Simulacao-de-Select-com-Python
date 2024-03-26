import tkinter as tk
from tkinter import ttk
import mysql.connector


class Array:
    def __init__(self, size):
        self.data = [None] * size
        self.size = size

    def __len__(self):
        return self.size

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        self.data[index] = value

    def append(self, value):
        if self.size == len(self.data):
            pass
        self.data[self.size] = value
        self.size += 1


def executar_select():
    mydb = mysql.connector.connect(
        host="localhost", port=3307, user="root", password="", database="simulacao_select"
    )
    mycursor = mydb.cursor()

    select_query = select_entry.get()

    mycursor.execute(select_query)

    results = Array(len(mycursor.fetchall()))
    mycursor.execute(select_query)
    for i, row in enumerate(mycursor):
        results[i] = row

    result_text.delete(1.0, tk.END)
    for i in range(results.size):
        result_text.insert(tk.END, str(results[i]) + "\n")

    mydb.close()


def inserir_dados(tabela, dados):
    mydb = mysql.connector.connect(
        host="localhost", port=3307, user="root", password="", database="simulacao_select"
    )
    mycursor = mydb.cursor()

    # Criar lista de placeholders para valores
    placeholders = [f"%s" for _ in range(len(dados[0]))]
    insert_query = f"INSERT INTO {tabela} VALUES ({','.join(placeholders)})"

    mycursor.execute(insert_query, dados)
    mydb.commit()

    print(f"Inseridos {mycursor.rowcount} registros com sucesso!")

    mydb.close()


root = tk.Tk()
root.title("Interface para SELECT e INSERT SQL")

root = tk.Tk()
root.title("Interface para SELECT SQL")

style = ttk.Style()
style.theme_use("clam") 
style.configure("TButton", padding=10, font=('Helvetica', 12))
style.configure("TLabel", font=('Helvetica', 12))
style.configure("TEntry", font=('Helvetica', 12))

main_frame = ttk.Frame(root, padding=(20, 10))
main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

select_label = ttk.Label(main_frame, text="Insira seu SELECT SQL:")
select_label.grid(column=0, row=0, sticky=tk.W)

select_entry = ttk.Entry(main_frame, width=50)
select_entry.grid(column=0, row=1, padx=5, pady=5, sticky=tk.W)

executar_button = ttk.Button(main_frame, text="Executar SELECT", command=executar_select)
executar_button.grid(column=0, row=2, pady=10)

result_text = tk.Text(main_frame, width=60, height=10)
result_text.grid(column=0, row=3, padx=5, pady=5, sticky=(tk.W, tk.E))

scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=result_text.yview)
scrollbar.grid(column=1, row=3, sticky=(tk.N, tk.S))
result_text['yscrollcommand'] = scrollbar.set


# Botão para executar INSERT
inserir_button = ttk.Button(main_frame, text="Inserir Dados", command=lambda: inserir_dados_window())
inserir_button.grid(column=1, row=2, pady=10)


def inserir_dados_window():
    # Nova janela para inserir dados
    insert_window = tk.Toplevel(root)
    insert_window.title("Inserir Dados")

    # Elementos para definir tabela e dados
    tabela_label = ttk.Label(insert_window, text="Tabela:")
    tabela_entry = ttk.Entry(insert_window)
    dados_label = ttk.Label(insert_window, text="Dados (array de arrays):")
    dados_text = tk.Text(insert_window, width=40, height=10)

    # Botão para executar INSERT na nova janela
    confirmar_insercao = ttk.Button(insert_window, text="Inserir", command=lambda: confirmar_insercao(tabela_entry.get(), dados_text.get(1.0, tk.END)))

    # Layout da nova janela
    tabela_label.grid(column=0, row=0, pady=5)
    tabela_entry.grid(column=1, row=0, padx=5, pady=5)
    dados_label.grid(column=0, row=1, pady=5)
    dados_text.grid(column=0, row=2, columnspan=2, padx=5)
    confirmar_insercao.grid(column=0, columnspan=2, pady=10)

    insert_window.mainloop()


def confirmar_insercao(tabela, dados_string):
    # Converter string de dados para array de arrays
    try:
        dados_array = eval(dados_string)
    except:
        print("Erro: Formato de dados inválido. Use um array de arrays.")
        return

    inserir_dados(tabela, dados_array)
    insert_window.destroy()  # Fechar a janela de inserção


root.mainloop()
