import sqlite3 # banco de dados
import tkinter as tk # interface basica
from tkinter import messagebox # caixas de mensagens
from tkinter import ttk # interface grafica tb

def conectar():
    return sqlite3.connect('teste.db')

def criar_tabela():
    conn = conectar()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios(
        id TEXT NOT NULL,
        nome TEXT NOT NULL,
        email TEXT NOT NULL,
        PRIMARY KEY (id)
        )
    ''')
    conn.commit()
    conn.close()

# CREATE
def inserir_usuario():
    nome = entry_nome.get().strip()
    email = entry_email.get().strip()
    cpf = entry_cpf.get().strip()

    if nome and email and cpf:
        conn = conectar()
        c = conn.cursor()
        try:
            c.execute('INSERT INTO usuarios(id, nome, email) VALUES(?,?,?)', (cpf, nome, email))
            conn.commit()
            messagebox.showinfo('AVISO', 'DADOS INSERIDOS COM SUCESSO!')
            # Clear input fields after successful insertion
            entry_nome.delete(0, tk.END)
            entry_email.delete(0, tk.END)
            entry_cpf.delete(0, tk.END)
        except sqlite3.IntegrityError:
            messagebox.showerror('ERRO', 'CPF já cadastrado. Por favor, insira um CPF único.')
        except Exception as e:
            messagebox.showerror('ERRO', f'Ocorreu um erro ao inserir os dados: {e}')
        finally:
            conn.close()
        mostrar_usuario()
    else:
        messagebox.showerror('ERRO', 'Por favor, preencha todos os campos: Nome, E-mail e CPF!')

# READ
def mostrar_usuario():
    for row in tree.get_children():
        tree.delete(row)
    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT * FROM usuarios')
    usuarios = c.fetchall()
    for usuario in usuarios:
        tree.insert("", "end", values=(usuario[0], usuario[1], usuario[2]))
    conn.close()

# DELETE
def delete_usuario():
    dado_del = tree.selection()
    if dado_del:
        confirm = messagebox.askyesno('Confirmação', 'Tem certeza que deseja deletar o usuário selecionado?')
        if confirm:
            user_id = tree.item(dado_del)['values'][0]
            conn = conectar()
            c = conn.cursor()
            c.execute('DELETE FROM usuarios WHERE id = ? ', (user_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo('Sucesso', 'Dado deletado com sucesso!')
            mostrar_usuario()
    else:
        messagebox.showerror('Erro', 'Nenhum usuário selecionado para deletar.')

# UPDATE
def editar():
    selecao = tree.selection()
    if selecao:
        user_id = tree.item(selecao)['values'][0]
        novo_nome = entry_nome.get().strip()
        novo_email = entry_email.get().strip()

        if novo_nome and novo_email:
            conn = conectar()
            c = conn.cursor()
            c.execute('UPDATE usuarios SET nome = ?, email = ? WHERE id = ? ', (novo_nome, novo_email, user_id))
            conn.commit()
            conn.close()
            messagebox.showinfo('Sucesso', 'Dados atualizados com sucesso!')
            mostrar_usuario()
            # Clear input fields after successful update
            entry_nome.delete(0, tk.END)
            entry_email.delete(0, tk.END)
            entry_cpf.delete(0, tk.END) # Clear CPF too, as it's not editable directly here
        else:
            messagebox.showwarning('Aviso', 'Preencha os campos Nome e E-mail para atualizar.')
    else:
        messagebox.showerror('Erro', 'Nenhum usuário selecionado para editar.')

# VAMOS COMPLETAR A INTERFACE GRÁFICA...
janela = tk.Tk()
janela.title('CRUD de Usuários')
janela.geometry('600x500') # Set a default window size
janela.resizable(False, False) # Make the window not resizable

# Input Frame
input_frame = tk.LabelFrame(janela, text="Dados do Usuário", padx=10, pady=10)
input_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

label_nome = tk.Label(input_frame, text='Nome:')
label_nome.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_nome = tk.Entry(input_frame, width=40)
entry_nome.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

label_email = tk.Label(input_frame, text='E-mail:')
label_email.grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_email = tk.Entry(input_frame, width=40)
entry_email.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

label_cpf = tk.Label(input_frame, text='CPF:')
label_cpf.grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_cpf = tk.Entry(input_frame, width=40)
entry_cpf.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

# Buttons Frame
button_frame = tk.Frame(janela, padx=10, pady=10)
button_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

btn_salvar = tk.Button(button_frame, text='SALVAR', command=inserir_usuario, width=15, height=2)
btn_salvar.grid(row=0, column=0, padx=5, pady=5)

btn_deletar = tk.Button(button_frame, text='DELETAR', command=delete_usuario, width=15, height=2)
btn_deletar.grid(row=0, column=1, padx=5, pady=5)

btn_atualizar = tk.Button(button_frame, text='ATUALIZAR', command=editar, width=15, height=2)
btn_atualizar.grid(row=0, column=2, padx=5, pady=5)

# Treeview Frame
tree_frame = tk.Frame(janela, padx=10, pady=10)
tree_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

columns = ('ID', 'NOME', 'EMAIL')

tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
tree.pack(side="left", fill="both", expand=True)

# Add a scrollbar to the Treeview
scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
scrollbar.pack(side="right", fill="y")
tree.configure(yscrollcommand=scrollbar.set)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150, anchor=tk.CENTER) # Set column width and center text

# Function to load selected item into entry fields for editing
def carregar_dados_selecionados(event):
    selected_item = tree.focus()
    if selected_item:
        values = tree.item(selected_item, 'values')
        entry_cpf.delete(0, tk.END)
        entry_nome.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        
        entry_cpf.insert(0, values[0])
        entry_nome.insert(0, values[1])
        entry_email.insert(0, values[2])

tree.bind('<<TreeviewSelect>>', carregar_dados_selecionados)

criar_tabela()
mostrar_usuario()

janela.mainloop()