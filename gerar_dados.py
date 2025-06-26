from faker import Faker
import random
import pandas as pd
import mysql.connector
from datetime import datetime, timedelta

#inicializa o gerador de dados falsos
fake = Faker('pt-br')

#conectar ao sql

conn = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="livro",
    database="clinica"
)

#if conn.is_connected():
    #print("Conexao realizada com sucesso")

cursor = conn.cursor()

#parametro para gerar os dados
ESPECIALIDADES =  ['Cardiologia', 'Ortopedia', 'Pediatria', 'Neurologia', 'Dermatologia']
LOCAIS = ["Morumbi", "Vila Santa Catarina", "Vila Mariana"]
MOTIVOS_ATRASOS =  ['Médico atrasado', 'Paciente atrasado', 'Alta demanda', 'Problema no sistema', 'Outros']

# ETAPA 1: gerar pacientes
pacientes = []
for _ in range(100):
    sexo = random.choice(["Masculino", "Feminino"])
    
    if sexo == "Masculino":
        nome = fake.name_male()
    else:
        nome = fake.name_female()
        
    idade = random.randint(1, 99)
    pacientes.append((nome, idade, sexo))

#inserir pacientes no banco:

for paciente in pacientes:
    cursor.execute("INSERT INTO pacientes (nome,idade,sexo) VALUES (%s, %s, %s)", paciente)
conn.commit()

#buscar os IDs gerados
cursor.execute("SELECT paciente_id FROM pacientes")
ids_pacientes = [id_[0] for id_ in cursor.fetchall()]

#ETAPA 2 GERAR AGENDAMENTOS:
for _ in range(300):
    paciente_id = random.choice(ids_pacientes)
    especialidade = random.choice(ESPECIALIDADES)
    local = random.choice(LOCAIS)
    motivo_atraso = random.choice(MOTIVOS_ATRASOS)

    #gerar data aleatoria nos ultimos 3 meses
    data_base = datetime.today()
    dias_atras = random.randint(0,99)
    data_agendamento = data_base - timedelta(days=dias_atras)

    #gerar hora agendada 
    hora_agendada = fake.time_object(end_datetime=None)
    atraso_min = random.choice([0,5,10,15,30,45,60])
    hora_atendimento = (datetime.combine(datetime.today(), hora_agendada) + timedelta(minutes=atraso_min)).time()

    cursor.execute("""
        INSERT INTO agendamentos (paciente_id, especialidade, data_agendamento, hora_agendada, hora_atendimento, local, motivo_atraso)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (paciente_id, especialidade, data_agendamento.date(), hora_agendada, hora_atendimento, local, motivo_atraso))

conn.commit()
conn.close()

print("Dados inseridos com sucesso")