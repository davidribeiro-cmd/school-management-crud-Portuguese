📘 [Versão em Português](Readme-ptBR.md)

🏫 School Management System in Python

CRUD operations for students, teachers, subjects, classes, and enrollments, with a terminal interface and JSON persistence.

I developed this project during my undergraduate studies in Information Technology Management at PUCPR to practice programming logic, function-based organization, file handling, and rules governing relationships between records.

The system manages school records and checks their relationships before performing certain updates or deletions.

🛠️ Technologies Used

Resource

Role in the Project

🐍 Python

System logic, functions, and interactive menus

📄 JSON

Local storage of records between runs

📦 json module

Reading and writing files using Python's standard library

💻 Terminal

Data entry and display of menus, record listings, and messages

The program uses functions, lists, and dictionaries. It requires no external packages or SQL database setup.

⚙️ Features

All record types support the four CRUD operations:

➕ Create: add new records.

📋 Read: list existing records.

✏️ Update: modify a record's information using its code.

🗑️ Delete: remove a record while respecting the dependencies checked by the system.

📚 Available Record Types

Record Type

Stored Information

🎓 Students

Code, name, and CPF (Brazilian individual taxpayer ID)

👩‍🏫 Teachers

Code, name, and CPF

📖 Subjects

Code and name

🏫 Classes

Code, teacher code, and subject code

📝 Enrollments

Code, class code, and student code

Class listings also display the teacher's name and the subject's name. Enrollment listings display the student's name and the class reference.

✅ Implemented Validations and Rules

Integer codes: prompts for another entry when the user enters a value that cannot be converted to an integer.

Unique codes within each record type: prevents creating or updating a record with a code already used by the same entity type.

Existing references: checks that the teacher and subject exist when creating a class, and that the class and student exist when creating an enrollment. New references are also checked during updates.

Protection of linked records: blocks deletion and code changes when dependencies exist, as shown below.

Partial updates: allows the user to press Enter to keep a field's current value.

Navigation: reports invalid menu options and allows the user to return to the main menu.

Record

Dependency That Blocks Deletion or a Code Change

Student

Linked enrollments

Teacher

Linked classes

Subject

Linked classes

Class

Linked enrollments

💡 Example: before deleting a student with an existing enrollment, the enrollment must be removed or updated. This prevents an enrollment from referencing a student deleted through the program.

💾 Data Storage

Records are organized as lists of dictionaries and saved in five files:

File

Contents

estudantes.json

Students

professores.json

Teachers

disciplinas.json

Subjects

turmas.json

Classes

matriculas.json

Enrollments

Files are created as data is saved, in the directory from which the program is run. UTF-8 encoding and indentation preserve accented characters and make the files easier to read.

🚀 How to Run

1. Prepare the Environment

Install Python 3 and download the project files. If you use Git, you can clone the repository:

git clone https://github.com/davidribeiro-cmd/school-management-crud-Portuguese.git
cd school-management-crud-Portuguese

2. Run the Program

Open a terminal in the project directory and run the Python file containing the main() function:

python your_filename.py

Replace your_filename.py with the actual project filename. Depending on your installation, the command may be python3 or, on Windows, py.

There is no need to run pip install: the code only uses the json module, which is included with Python.

3. Navigate the Menus

Choose the record type from the main menu, then select Incluir (Create), Listar (List), Atualizar (Update), or Excluir (Delete). Use 0 to go back; in the main menu, 0 exits the system.

🧪 Usage Example

To try the enrollment workflow, use fictional data:

Create a teacher and a subject.

Create a class, entering the codes of those two records.

Create a student.

Create an enrollment, linking the student to the class.

List the enrollments to view the relationship you created.

Try deleting the student: the system will report that a linked enrollment exists.

🧠 Concepts Applied

Procedural programming and breaking a problem down into functions.

Reusing functions for reading, writing, searching, and listing.

Working with lists and dictionaries.

Conditional statements and loops.

Data persistence in JSON files.

Linking records through codes.

Handling ValueError, FileNotFoundError, and json.JSONDecodeError.

<details>
<summary>🔎 Current Behavior and Limitations</summary>

Interaction takes place through the terminal; the code does not include a graphical interface or authentication.

CPF values are stored as text, without format, check-digit, or uniqueness validation. Empty names and CPF values are not blocked when creating records.

Code validation requires integers but does not restrict values to positive numbers.

Enrollments with different codes may link the same student to the same class.

When a file is missing, empty, or contains invalid JSON, the read function returns an empty list. This does not recover corrupted data: a later write may overwrite the file's contents.

The code assumes that valid JSON follows the expected structure and does not implement controls for simultaneous writes by multiple instances.

</details>

👨‍💻 Author

David Ribeiro Dias
Undergraduate student in Information Technology Management — PUCPR

💻 GitHub · 💼 LinkedIn
