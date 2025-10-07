import json

# -------------------------
# Funções de Ler/Salvar JSON
# -------------------------


def ler_arquivo(nome_arquivo):
    """Lê e retorna uma lista de dicionários do arquivo JSON.
    Se o arquivo não existir ou estiver vazio/corrompido retorna lista vazia.
    """
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Se o arquivo ainda não existe -> retorna lista vazia
        return []
    except json.JSONDecodeError:
        # Se o arquivo estiver vazio ou com conteúdo inválido -> trata como lista vazia
        return []


def salvar_arquivo(lista_qualquer, nome_arquivo):
    """Salva a lista de dicionários no arquivo JSON.
    """
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(lista_qualquer, f, ensure_ascii=False, indent=4)


# -------------------------
# Funções utilitárias
# -------------------------
# Essas funções são reutilizadas por todos os módulos (estudantes, professores, ...)


def input_int(prompt, allow_empty=False):
    """Pede um número inteiro ao usuário com tratamento de erro.
    """
    while True:
        valor = input(prompt).strip()
        if allow_empty and valor == "":
            return None
        try:
            return int(valor)
        except ValueError:
            print("Por favor, digite um número inteiro válido.")


def encontrar_por_codigo(lista, codigo):
    """Procura e retorna o dicionário cujo campo 'Código' == codigo.
    Caso não encontre, retorna None.
    """
    for item in lista:
        if item.get("Código") == codigo:
            return item
    return None


def existe_codigo(nome_arquivo, codigo):
    """Verifica se já existe um registro com o código informado no arquivo.
    Usada para impedir duplicidade ao incluir.
    """
    lista = ler_arquivo(nome_arquivo)
    return any(item.get("Código") == codigo for item in lista)


def listar_registros(nome_arquivo, titulo="Registros"):
    """Mostra todos os registros do arquivo em formato legível.
    Reaproveitada por várias entidades.
    """
    lista = ler_arquivo(nome_arquivo)
    if not lista:
        print(f"Não há {titulo} cadastrados.")
        return
    print(f"---- {titulo} ----")
    for item in lista:
        # Concatena chave: valor de cada dicionário para exibir em uma linha
        linha = " | ".join([f"{k}: {v}" for k, v in item.items()])
        print(linha)
    print("-------------------")


def tem_dependencia(nome_arquivo_dependente, campo_referencia, codigo):
    """Verifica se existe algum registro no arquivo dependente
    que referencia o código fornecido (ex.: matrículas referenciam estudante).
    Retorna True se existir dependência.
    """
    lista = ler_arquivo(nome_arquivo_dependente)
    return any(item.get(campo_referencia) == codigo for item in lista)


# -------------------------
# Menus (principal, operações)
# -------------------------

def mostrar_menu_principal():
    print("\nBem-vindo(a) ao MENU PRINCIPAL")
    print("1. Gerenciar Estudantes")
    print("2. Gerenciar Disciplinas")
    print("3. Gerenciar Turmas")
    print("4. Gerenciar Matrículas")
    print("5. Gerenciar Professores")
    print("0. Sair")
    return input("Digite uma opção listada a cima: ").strip()


def mostrar_menu_operacoes(entidade):
    # entidade: texto para exibir qual conjunto estamos gerenciando
    print(f"\nMENU DE OPERAÇÕES - {entidade}")
    print("1. Incluir")
    print("2. Listar")
    print("3. Atualizar")
    print("4. Excluir")
    print("0. Voltar ao MENU PRINCIPAL")
    return input("Digite uma opção listada a cima: ").strip()


# -------------------------
# Arquivos.json
# -------------------------
ARQ_ESTUDANTES = "estudantes.json"
ARQ_PROFESSORES = "professores.json"
ARQ_DISCIPLINAS = "disciplinas.json"
ARQ_TURMAS = "turmas.json"
ARQ_MATRICULAS = "matriculas.json"


# -------------------------
# CRUD - Estudantes
# -------------------------
# Cada bloco (incluir/listar/atualizar/excluir) usa as funções utilitárias acima.
# validações de integridade (ex.: não excluir estudante com matrícula).


def incluir_estudante():
    lista = ler_arquivo(ARQ_ESTUDANTES)
    codigo = input_int("Digite o código do estudante: ")
    if existe_codigo(ARQ_ESTUDANTES, codigo):
        print("Código já existe. Escolha outro código.")
        return
    nome = input("Digite o nome: ").strip()
    cpf = input("Digite o CPF: ").strip()
    d = {"Código": codigo, "Nome": nome, "CPF": cpf}
    lista.append(d)
    salvar_arquivo(lista, ARQ_ESTUDANTES)
    print("Estudante incluído com sucesso.")


def listar_estudantes():
    listar_registros(ARQ_ESTUDANTES, "Estudantes")


def atualizar_estudante():
    lista = ler_arquivo(ARQ_ESTUDANTES)
    if not lista:
        print("Nenhum estudante cadastrado.")
        return
    codigo = input_int("Digite o código do estudante que deseja atualizar: ")
    estudante = encontrar_por_codigo(lista, codigo)
    if not estudante:
        print("Estudante não encontrado.")
        return

    novo_codigo = input_int(
        "Digite o novo código (enter para manter): ", allow_empty=True)
    if novo_codigo is None:
        novo_codigo = estudante["Código"]
    else:
        # Se o novo código for diferente do antigo, valida duplicidade e dependências
        if novo_codigo != estudante["Código"] and existe_codigo(ARQ_ESTUDANTES, novo_codigo):
            print("Já existe estudante com esse código. Atualização cancelada.")
            return
        if novo_codigo != estudante["Código"] and tem_dependencia(ARQ_MATRICULAS, "CodEstudante", estudante["Código"]):
            print("Existem matrículas vinculadas a este estudante. Primeiro remova/atualize as matrículas para alterar o código.")
            return

    novo_nome = input("Digite o novo nome (enter para manter): ").strip()
    if novo_nome == "":
        novo_nome = estudante["Nome"]
    novo_cpf = input("Digite o novo CPF (enter para manter): ").strip()
    if novo_cpf == "":
        novo_cpf = estudante["CPF"]

    estudante["Código"] = novo_codigo
    estudante["Nome"] = novo_nome
    estudante["CPF"] = novo_cpf
    salvar_arquivo(lista, ARQ_ESTUDANTES)
    print("Estudante atualizado com sucesso.")


def excluir_estudante():
    lista = ler_arquivo(ARQ_ESTUDANTES)
    if not lista:
        print("Nenhum estudante cadastrado.")
        return
    codigo = input_int("Digite o código do estudante que deseja excluir: ")
    estudante = encontrar_por_codigo(lista, codigo)
    if not estudante:
        print("Estudante não encontrado.")
        return
    # Verifica dependências (matrículas) antes de remover
    if tem_dependencia(ARQ_MATRICULAS, "CodEstudante", codigo):
        print("Não é possível excluir: existem matrículas vinculadas a este estudante.")
        return
    lista.remove(estudante)
    salvar_arquivo(lista, ARQ_ESTUDANTES)
    print("Estudante excluído com sucesso.")


# -------------------------
# CRUD - Professores
# -------------------------

def incluir_professor():
    lista = ler_arquivo(ARQ_PROFESSORES)
    codigo = input_int("Digite o código do professor: ")
    if existe_codigo(ARQ_PROFESSORES, codigo):
        print("Código já existe. Escolha outro código.")
        return
    nome = input("Digite o nome: ").strip()
    cpf = input("Digite o CPF: ").strip()
    d = {"Código": codigo, "Nome": nome, "CPF": cpf}
    lista.append(d)
    salvar_arquivo(lista, ARQ_PROFESSORES)
    print("Professor incluído com sucesso.")


def listar_professores():
    listar_registros(ARQ_PROFESSORES, "Professores")


def atualizar_professor():
    lista = ler_arquivo(ARQ_PROFESSORES)
    if not lista:
        print("Nenhum professor cadastrado.")
        return
    codigo = input_int("Digite o código do professor que deseja atualizar: ")
    professor = encontrar_por_codigo(lista, codigo)
    if not professor:
        print("Professor não encontrado.")
        return

    novo_codigo = input_int(
        "Digite o novo código (enter para manter): ", allow_empty=True)
    if novo_codigo is None:
        novo_codigo = professor["Código"]
    else:
        if novo_codigo != professor["Código"] and existe_codigo(ARQ_PROFESSORES, novo_codigo):
            print("Já existe professor com esse código. Atualização cancelada.")
            return
        if novo_codigo != professor["Código"] and tem_dependencia(ARQ_TURMAS, "CodProfessor", professor["Código"]):
            print("Existem turmas vinculadas a este professor. Primeiro remova/atualize as turmas para alterar o código.")
            return

    novo_nome = input("Digite o novo nome (enter para manter): ").strip()
    if novo_nome == "":
        novo_nome = professor["Nome"]
    novo_cpf = input("Digite o novo CPF (enter para manter): ").strip()
    if novo_cpf == "":
        novo_cpf = professor["CPF"]

    professor["Código"] = novo_codigo
    professor["Nome"] = novo_nome
    professor["CPF"] = novo_cpf
    salvar_arquivo(lista, ARQ_PROFESSORES)
    print("Professor atualizado com sucesso.")


def excluir_professor():
    lista = ler_arquivo(ARQ_PROFESSORES)
    if not lista:
        print("Nenhum professor cadastrado.")
        return
    codigo = input_int("Digite o código do professor que deseja excluir: ")
    professor = encontrar_por_codigo(lista, codigo)
    if not professor:
        print("Professor não encontrado.")
        return
    # Impede exclusão se houver turmas vinculadas
    if tem_dependencia(ARQ_TURMAS, "CodProfessor", codigo):
        print("Não é possível excluir: existem turmas vinculadas a este professor.")
        return
    lista.remove(professor)
    salvar_arquivo(lista, ARQ_PROFESSORES)
    print("Professor excluído com sucesso.")


# -------------------------
# CRUD - Disciplinas
# -------------------------

def incluir_disciplina():
    lista = ler_arquivo(ARQ_DISCIPLINAS)
    codigo = input_int("Digite o código da disciplina: ")
    if existe_codigo(ARQ_DISCIPLINAS, codigo):
        print("Código já existe. Escolha outro código.")
        return
    nome = input("Digite o nome da disciplina: ").strip()
    d = {"Código": codigo, "Nome": nome}
    lista.append(d)
    salvar_arquivo(lista, ARQ_DISCIPLINAS)
    print("Disciplina incluída com sucesso.")


def listar_disciplinas():
    listar_registros(ARQ_DISCIPLINAS, "Disciplinas")


def atualizar_disciplina():
    lista = ler_arquivo(ARQ_DISCIPLINAS)
    if not lista:
        print("Nenhuma disciplina cadastrada.")
        return
    codigo = input_int("Digite o código da disciplina que deseja atualizar: ")
    disciplina = encontrar_por_codigo(lista, codigo)
    if not disciplina:
        print("Disciplina não encontrada.")
        return

    novo_codigo = input_int(
        "Digite o novo código (enter para manter): ", allow_empty=True)
    if novo_codigo is None:
        novo_codigo = disciplina["Código"]
    else:
        if novo_codigo != disciplina["Código"] and existe_codigo(ARQ_DISCIPLINAS, novo_codigo):
            print("Já existe disciplina com esse código. Atualização cancelada.")
            return
        if novo_codigo != disciplina["Código"] and tem_dependencia(ARQ_TURMAS, "CodDisciplina", disciplina["Código"]):
            print("Existem turmas vinculadas a esta disciplina. Primeiro remova/atualize as turmas para alterar o código.")
            return

    novo_nome = input("Digite o novo nome (enter para manter): ").strip()
    if novo_nome == "":
        novo_nome = disciplina["Nome"]

    disciplina["Código"] = novo_codigo
    disciplina["Nome"] = novo_nome
    salvar_arquivo(lista, ARQ_DISCIPLINAS)
    print("Disciplina atualizada com sucesso.")


def excluir_disciplina():
    lista = ler_arquivo(ARQ_DISCIPLINAS)
    if not lista:
        print("Nenhuma disciplina cadastrada.")
        return
    codigo = input_int("Digite o código da disciplina que deseja excluir: ")
    disciplina = encontrar_por_codigo(lista, codigo)
    if not disciplina:
        print("Disciplina não encontrada.")
        return
    # Impede exclusão se houver turmas vinculadas
    if tem_dependencia(ARQ_TURMAS, "CodDisciplina", codigo):
        print("Não é possível excluir: existem turmas vinculadas a esta disciplina.")
        return
    lista.remove(disciplina)
    salvar_arquivo(lista, ARQ_DISCIPLINAS)
    print("Disciplina excluída com sucesso.")


# -------------------------
# CRUD - Turmas
# -------------------------

def incluir_turma():
    lista = ler_arquivo(ARQ_TURMAS)
    codigo = input_int("Digite o código da turma: ")
    if existe_codigo(ARQ_TURMAS, codigo):
        print("Código já existe. Escolha outro código.")
        return
    cod_prof = input_int("Digite o código do professor responsável: ")
    # Valida se o professor existe antes de criar a turma
    if not existe_codigo(ARQ_PROFESSORES, cod_prof):
        print("Professor não encontrado. Cadastre o professor antes de criar a turma.")
        return
    cod_disc = input_int("Digite o código da disciplina: ")
    # Valida se a disciplina existe antes de criar a turma
    if not existe_codigo(ARQ_DISCIPLINAS, cod_disc):
        print("Disciplina não encontrada. Cadastre a disciplina antes de criar a turma.")
        return

    d = {"Código": codigo, "CodProfessor": cod_prof, "CodDisciplina": cod_disc}
    lista.append(d)
    salvar_arquivo(lista, ARQ_TURMAS)
    print("Turma incluída com sucesso.")


def listar_turmas():
    lista = ler_arquivo(ARQ_TURMAS)
    if not lista:
        print("Não há turmas cadastradas.")
        return
    print("---- Turmas ----")
    for t in lista:
        # Mostra também o nome do professor e da disciplina para facilitar leitura
        prof = encontrar_por_codigo(ler_arquivo(
            ARQ_PROFESSORES), t.get("CodProfessor"))
        disc = encontrar_por_codigo(ler_arquivo(
            ARQ_DISCIPLINAS), t.get("CodDisciplina"))
        nome_prof = prof["Nome"] if prof else "Professor não encontrado"
        nome_disc = disc["Nome"] if disc else "Disciplina não encontrada"
        print(
            f"Código: {t['Código']} | Professor: ({t['CodProfessor']}) {nome_prof} | Disciplina: ({t['CodDisciplina']}) {nome_disc}")
    print("----------------")


def atualizar_turma():
    lista = ler_arquivo(ARQ_TURMAS)
    if not lista:
        print("Nenhuma turma cadastrada.")
        return
    codigo = input_int("Digite o código da turma que deseja atualizar: ")
    turma = encontrar_por_codigo(lista, codigo)
    if not turma:
        print("Turma não encontrada.")
        return

    novo_codigo = input_int(
        "Digite o novo código (enter para manter): ", allow_empty=True)
    if novo_codigo is None:
        novo_codigo = turma["Código"]
    else:
        if novo_codigo != turma["Código"] and existe_codigo(ARQ_TURMAS, novo_codigo):
            print("Já existe turma com esse código. Atualização cancelada.")
            return
        if novo_codigo != turma["Código"] and tem_dependencia(ARQ_MATRICULAS, "CodTurma", turma["Código"]):
            print("Existem matrículas vinculadas a esta turma. Primeiro remova/atualize as matrículas para alterar o código.")
            return

    novo_prof = input_int(
        "Digite o novo código do professor (enter para manter): ", allow_empty=True)
    if novo_prof is None:
        novo_prof = turma["CodProfessor"]
    else:
        if not existe_codigo(ARQ_PROFESSORES, novo_prof):
            print("Professor não encontrado. Atualização cancelada.")
            return

    novo_disc = input_int(
        "Digite o novo código da disciplina (enter para manter): ", allow_empty=True)
    if novo_disc is None:
        novo_disc = turma["CodDisciplina"]
    else:
        if not existe_codigo(ARQ_DISCIPLINAS, novo_disc):
            print("Disciplina não encontrada. Atualização cancelada.")
            return

    turma["Código"] = novo_codigo
    turma["CodProfessor"] = novo_prof
    turma["CodDisciplina"] = novo_disc
    salvar_arquivo(lista, ARQ_TURMAS)
    print("Turma atualizada com sucesso.")


def excluir_turma():
    lista = ler_arquivo(ARQ_TURMAS)
    if not lista:
        print("Nenhuma turma cadastrada.")
        return
    codigo = input_int("Digite o código da turma que deseja excluir: ")
    turma = encontrar_por_codigo(lista, codigo)
    if not turma:
        print("Turma não encontrada.")
        return
    # Se existir matrícula vinculada à turma, a exclusão é impedida
    if tem_dependencia(ARQ_MATRICULAS, "CodTurma", codigo):
        print("Não é possível excluir: existem matrículas vinculadas a esta turma.")
        return
    lista.remove(turma)
    salvar_arquivo(lista, ARQ_TURMAS)
    print("Turma excluída com sucesso.")


# -------------------------
# CRUD - Matrículas
# -------------------------

def incluir_matricula():
    lista = ler_arquivo(ARQ_MATRICULAS)
    codigo = input_int("Digite o código da matrícula: ")
    if existe_codigo(ARQ_MATRICULAS, codigo):
        print("Código já existe. Escolha outro código.")
        return
    cod_turma = input_int("Digite o código da turma: ")
    if not existe_codigo(ARQ_TURMAS, cod_turma):
        print("Turma não encontrada. Cadastre a turma antes de matricular.")
        return
    cod_est = input_int("Digite o código do estudante: ")
    if not existe_codigo(ARQ_ESTUDANTES, cod_est):
        print("Estudante não encontrado. Cadastre o estudante antes de matricular.")
        return
    d = {"Código": codigo, "CodTurma": cod_turma, "CodEstudante": cod_est}
    lista.append(d)
    salvar_arquivo(lista, ARQ_MATRICULAS)
    print("Matrícula incluída com sucesso.")


def listar_matriculas():
    lista = ler_arquivo(ARQ_MATRICULAS)
    if not lista:
        print("Não há matrículas cadastradas.")
        return
    print("---- Matrículas ----")
    for m in lista:
        # Exibe o nome do estudante e a referência da turma para facilitar leitura
        est = encontrar_por_codigo(ler_arquivo(
            ARQ_ESTUDANTES), m.get("CodEstudante"))
        turma = encontrar_por_codigo(
            ler_arquivo(ARQ_TURMAS), m.get("CodTurma"))
        nome_est = est["Nome"] if est else "Estudante não encontrado"
        info_turma = f"Turma {m.get('CodTurma')}" if turma else "Turma não encontrada"
        print(
            f"Código: {m['Código']} | Estudante: ({m['CodEstudante']}) {nome_est} | {info_turma}")
    print("---------------------")


def atualizar_matricula():
    lista = ler_arquivo(ARQ_MATRICULAS)
    if not lista:
        print("Nenhuma matrícula cadastrada.")
        return
    codigo = input_int("Digite o código da matrícula que deseja atualizar: ")
    matricula = encontrar_por_codigo(lista, codigo)
    if not matricula:
        print("Matrícula não encontrada.")
        return

    novo_codigo = input_int(
        "Digite o novo código (enter para manter): ", allow_empty=True)
    if novo_codigo is None:
        novo_codigo = matricula["Código"]
    else:
        if novo_codigo != matricula["Código"] and existe_codigo(ARQ_MATRICULAS, novo_codigo):
            print("Já existe matrícula com esse código. Atualização cancelada.")
            return

    novo_turma = input_int(
        "Digite o novo código da turma (enter para manter): ", allow_empty=True)
    if novo_turma is None:
        novo_turma = matricula["CodTurma"]
    else:
        if not existe_codigo(ARQ_TURMAS, novo_turma):
            print("Turma não encontrada. Atualização cancelada.")
            return

    novo_est = input_int(
        "Digite o novo código do estudante (enter para manter): ", allow_empty=True)
    if novo_est is None:
        novo_est = matricula["CodEstudante"]
    else:
        if not existe_codigo(ARQ_ESTUDANTES, novo_est):
            print("Estudante não encontrado. Atualização cancelada.")
            return

    matricula["Código"] = novo_codigo
    matricula["CodTurma"] = novo_turma
    matricula["CodEstudante"] = novo_est
    salvar_arquivo(lista, ARQ_MATRICULAS)
    print("Matrícula atualizada com sucesso.")


def excluir_matricula():
    lista = ler_arquivo(ARQ_MATRICULAS)
    if not lista:
        print("Nenhuma matrícula cadastrada.")
        return
    codigo = input_int("Digite o código da matrícula que deseja excluir: ")
    matricula = encontrar_por_codigo(lista, codigo)
    if not matricula:
        print("Matrícula não encontrada.")
        return
    lista.remove(matricula)
    salvar_arquivo(lista, ARQ_MATRICULAS)
    print("Matrícula excluída com sucesso.")


# -------------------------
# Loop de gerenciamento por entidade
# -------------------------

def gerenciar_entidade(opcao_entidade):
    """
    Recebe a opção do menu principal ("1".."5") e entra em um loop
    para gerenciar a entidade correspondente (ex.: estudantes).
    """
    while True:
        if opcao_entidade == "1":
            entidade_nome = "Estudantes"
        elif opcao_entidade == "2":
            entidade_nome = "Disciplinas"
        elif opcao_entidade == "3":
            entidade_nome = "Turmas"
        elif opcao_entidade == "4":
            entidade_nome = "Matrículas"
        elif opcao_entidade == "5":
            entidade_nome = "Professores"
        else:
            return

        oper = mostrar_menu_operacoes(entidade_nome)

        # Para cada entidade verificamos a operação escolhida e chamamos
        # a função correspondente.

        # Estudantes
        if opcao_entidade == "1":
            if oper == "1":
                incluir_estudante()
            elif oper == "2":
                listar_estudantes()
            elif oper == "3":
                atualizar_estudante()
            elif oper == "4":
                excluir_estudante()
            elif oper == "0":
                break
            else:
                print("Opção inválida.")

        # Disciplinas
        elif opcao_entidade == "2":
            if oper == "1":
                incluir_disciplina()
            elif oper == "2":
                listar_disciplinas()
            elif oper == "3":
                atualizar_disciplina()
            elif oper == "4":
                excluir_disciplina()
            elif oper == "0":
                break
            else:
                print("Opção inválida.")

        # Turmas
        elif opcao_entidade == "3":
            if oper == "1":
                incluir_turma()
            elif oper == "2":
                listar_turmas()
            elif oper == "3":
                atualizar_turma()
            elif oper == "4":
                excluir_turma()
            elif oper == "0":
                break
            else:
                print("Opção inválida.")

        # Matrículas
        elif opcao_entidade == "4":
            if oper == "1":
                incluir_matricula()
            elif oper == "2":
                listar_matriculas()
            elif oper == "3":
                atualizar_matricula()
            elif oper == "4":
                excluir_matricula()
            elif oper == "0":
                break
            else:
                print("Opção inválida.")

        # Professores
        elif opcao_entidade == "5":
            if oper == "1":
                incluir_professor()
            elif oper == "2":
                listar_professores()
            elif oper == "3":
                atualizar_professor()
            elif oper == "4":
                excluir_professor()
            elif oper == "0":
                break
            else:
                print("Opção inválida.")


# -------------------------
# Função main -> inicia o programa
# -------------------------

def main():
    # Loop principal: exibe menu principal e chama gerenciar_entidade
    while True:
        opcao = mostrar_menu_principal()
        if opcao in ["1", "2", "3", "4", "5"]:
            gerenciar_entidade(opcao)
        elif opcao == "0":
            print("Encerrando o sistema. Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
