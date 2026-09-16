📘 [English Version](Readme.md)

🏫 Sistema de Gestão Escolar em Python

CRUD de estudantes, professores, disciplinas, turmas e matrículas, com interface via terminal e persistência em JSON.

Desenvolvi este projeto durante minha graduação em Gestão da Tecnologia da Informação na PUCPR, para aplicar lógica de programação, organização em funções, manipulação de arquivos e regras de relacionamento entre cadastros.

O sistema permite gerenciar os registros de uma rotina escolar e verifica os vínculos entre eles antes de executar determinadas alterações ou exclusões.

🛠️ Tecnologias utilizadas

Recurso

Aplicação no projeto

🐍 Python

Lógica do sistema, funções e menus interativos

📄 JSON

Armazenamento local dos registros entre execuções

📦 Módulo json

Leitura e gravação dos arquivos, usando a biblioteca padrão do Python

💻 Terminal

Entrada de dados e exibição de menus, listagens e mensagens

O programa utiliza funções, listas e dicionários. Não exige instalação de pacotes externos nem configuração de banco de dados SQL.

⚙️ Funcionalidades

Todos os cadastros oferecem as quatro operações de um CRUD:

➕ Incluir: adicionar novos registros.

📋 Listar: visualizar os registros cadastrados.

✏️ Atualizar: modificar informações de um registro pelo código.

🗑️ Excluir: remover um registro, respeitando as dependências verificadas pelo sistema.

📚 Cadastros disponíveis

Cadastro

Informações armazenadas

🎓 Estudantes

Código, nome e CPF

👩‍🏫 Professores

Código, nome e CPF

📖 Disciplinas

Código e nome

🏫 Turmas

Código, código do professor e código da disciplina

📝 Matrículas

Código, código da turma e código do estudante

Na listagem de turmas, o sistema também exibe os nomes do professor e da disciplina. Na listagem de matrículas, apresenta o nome do estudante e a referência da turma.

✅ Validações e regras implementadas

Códigos inteiros: solicita uma nova entrada quando o usuário digita um valor que não pode ser convertido para inteiro.

Códigos únicos por cadastro: impede incluir ou alterar um registro para um código já utilizado na mesma entidade.

Vínculos existentes: verifica se o professor e a disciplina existem ao cadastrar uma turma e se a turma e o estudante existem ao cadastrar uma matrícula. Também verifica novas referências nas atualizações.

Proteção de registros vinculados: bloqueia a exclusão e a alteração de código quando há dependências, conforme a tabela abaixo.

Atualização parcial: permite pressionar Enter para manter o valor atual de um campo.

Navegação: informa quando uma opção de menu é inválida e permite voltar ao menu principal.

Registro

Dependência que impede sua exclusão ou mudança de código

Estudante

Matrículas vinculadas

Professor

Turmas vinculadas

Disciplina

Turmas vinculadas

Turma

Matrículas vinculadas

💡 Exemplo: para excluir um estudante com matrícula cadastrada, é necessário remover ou atualizar a matrícula antes. Isso evita deixar uma matrícula apontando para um estudante que foi excluído pelo programa.

💾 Armazenamento dos dados

Os registros são organizados em listas de dicionários e salvos em cinco arquivos:

Arquivo

Conteúdo

estudantes.json

Estudantes

professores.json

Professores

disciplinas.json

Disciplinas

turmas.json

Turmas

matriculas.json

Matrículas

Os arquivos são criados conforme os dados são salvos, na pasta de onde o programa é executado. A gravação usa UTF-8 e indentação para preservar acentos e facilitar a leitura.

🚀 Como executar

1. Prepare o ambiente

Tenha o Python 3 instalado e baixe os arquivos do projeto. Se utilizar Git, você pode clonar o repositório:

git clone https://github.com/davidribeiro-cmd/school-management-crud-Portuguese.git
cd school-management-crud-Portuguese

2. Execute o programa

Abra o terminal na pasta do projeto e execute o arquivo Python que contém a função main():

python nome_do_arquivo.py

Substitua nome_do_arquivo.py pelo nome real do arquivo do projeto. Dependendo da instalação, o comando pode ser python3 ou, no Windows, py.

Não é necessário executar pip install: o código utiliza apenas o módulo json, incluído no Python.

3. Navegue pelos menus

Escolha o cadastro desejado no menu principal e, em seguida, selecione Incluir, Listar, Atualizar ou Excluir. Use 0 para voltar; no menu principal, 0 encerra o sistema.

🧪 Exemplo de uso

Para experimentar o fluxo de uma matrícula, utilize dados fictícios:

Cadastre um professor e uma disciplina.

Cadastre uma turma, informando os códigos desses dois registros.

Cadastre um estudante.

Crie uma matrícula, vinculando o estudante à turma.

Liste as matrículas para consultar o vínculo criado.

Tente excluir o estudante: o sistema informará que há uma matrícula vinculada.

🧠 Conceitos aplicados

Programação procedural e decomposição do problema em funções.

Reutilização de funções para leitura, gravação, busca e listagem.

Manipulação de listas e dicionários.

Estruturas condicionais e laços de repetição.

Persistência de dados em arquivos JSON.

Relacionamento entre registros por meio de códigos.

Tratamento de ValueError, FileNotFoundError e json.JSONDecodeError.

<details>
<summary>🔎 Comportamentos e limites da versão atual</summary>

A interação acontece pelo terminal; o código não inclui interface gráfica ou autenticação.

O CPF é armazenado como texto, sem validação de formato, dígitos verificadores ou duplicidade. Nomes e CPFs vazios não são bloqueados na inclusão.

A validação de códigos exige números inteiros, mas não restringe os valores a números positivos.

Matrículas com códigos diferentes podem vincular o mesmo estudante à mesma turma.

Quando um arquivo não existe, está vazio ou contém JSON inválido, a leitura retorna uma lista vazia. Isso não recupera dados corrompidos: uma gravação posterior pode substituir o conteúdo desse arquivo.

O código pressupõe que o JSON válido siga a estrutura esperada e não implementa controle para gravações simultâneas por várias instâncias.

</details>

👨‍💻 Autor

David Ribeiro Dias
Graduando em Gestão da Tecnologia da Informação — PUCPR

💻 GitHub · 💼 LinkedIn
