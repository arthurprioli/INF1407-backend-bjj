<h1>Introdução</h1>
Esse é o repositório do backend do nosso projeto de posições de jiujitsu para a disciplina de programação para a web INF1407.
Projeto inteiramente desenvolvido por Felipe Barcellos e Arthur Prioli.
O objetivo desse site é que seja possível fazer login com um papel de estudante ou de professor. O aluno possuirá uma visão do site, em que ele poderá marcar as posições de luta como aprendidas, enquanto os professores poderão adicionar e remover as posições que são disponibilizadas no site.
Também é possível que o usuário esqueça a senha do seu login, então também foi implementado um email de redefinição de senha.
A dificuldade desse trabalho é o funcionamento totalmente isolado do front (typescript) e backend(Django/python), diferentemente do primeiro trabalho da disciplina.
link do frontend: https://github.com/arthurprioli/trabalho2-progweb.git
<h1>Descrição do projeto</h1>
Nosso projeto possui 3 aplicativos, sendo um deles o Labjj que atua como nosso core do projeto, o posições que atua como o aplicativo que gerencia o CRUD das posições de JiuJitsu e o accounts que gerencia tokens de autenticação e informações do usuário. 
<h2>Posições</h2>
É o CRUD da funcionalidade central do nosso projeto. Ele que gere todas as requisições relacionadas às posições de JiuJitsu. 
Ele possui apenas duas Views, o PosicaoView e o PosicoesView.
<h3>PosicoesView</h3>
O PosicoesView é utilizado no cenário em que você pode mexer em múltiplas views, como na página Home do nosso frontend.
A requisição get só pode ser feita por um usuário já autenticado e retorna todas as posições que existem no banco de dados.
A requisição delete só pode ser feita por um usuário com o papel de professor (chamado de admin no nosso programa) e ele deleta todas as posições que foram marcadas pelo professor na página inicial.
<h3>PosicaoView</h3>
O PosicaoView é utilizado para no cenário de mexer individualmente em uma posição e conta com requisições GET, POST, PUT. Todas essas requisições só podem ser feitas por um usuário autenticado.
A requisição get recebe um parâmetro _id_ e retorna todas as informações daquela posição, é chamada quando clicamos na posição no frontend.
A requisição post só pode ser feita por um professor, ele preenche um formulário sobre a posição e envia junto ao post e com isso consegue criar uma nova posição no banco de dados.
A requisição put também só pode ser feita por um professor, se ele quiser alterar qualquer informação sobre qualquer posição.
<h2>Accounts</h2>
É o app que gere Tokens de autenticação, Login, Logout, cadastro, mudança de senhas e informações do usuário.
Possui quatro Views, CustomAuthToken, Registro, Logged e GerenciarAprendizado.
<h3>CustomAuthToken</h3>
View de CustomAuthToken exatamente igual ao que vimos em sala. Uma view que gere os tokens de autenticação do usuário com as requisições GET, POST, PUT, DELETE.
A requisicão post recebe o username e a senha do usuário, valida o login e cria um token de autenticação para a sessão dele.
A requisição get recebe o token e verifica se existe um usuário vinculado à aquele token e retorna 'username' ou visitante.
A requisição put é utilizada quando o usuário troca de senha, gerando uma mudança de sessão.
A requisição delete é utilizada para fazer o logout do usuário, apagando seu token do contexto para que ele não possa ter acesso às rotas do backend mesmo estando deslogado.
<h3>Registro</h3>
View criada única e exclusivamente para efetuar o cadastro de novos usuários, conta apenas com um método post.
Recebe um formulário com diversos campos para criação de um User(classe de login nativa do Django) e de um UserProfile(Classe criada por nós que vincula um User com um papel de estudante ou admin/professor)
<h3>Logged</h3>
View que possui apenas a requisição get.
Recebe um token de autenticação e a partir desse token encontra o usuário que está logado e retorna todas as informações em relação ao seu perfil, como username, email, role.
<h3>GerenciarAprendizado</h3>
View que gerencia o aprendizado do aluno e possui dois métodos, GET e POST.
O get mostra todas as posições aprendidas do usuário atualmente loggado.
O Post adiciona a posição à lista de posições aprendidas do aluno.
<h2>Models</h2>
Agora que terminamos de falar de views vamos falar de models. 
As models são estruturas criadas dentro do django que são criadas equivalentemente dentro do banco de dados do sqlite. Portanto são estruturas muito importantes para fazer consultas e alterações de elementos no banco.
Nossas models são:<br>
<strong>UserProfile</strong> : Model que vincula usuário com seu papel de aluno ou professor.<br>
<strong>PosicaoAprendida</strong> : Model que vincula uma posição com um usuário .<br>
<strong>BJJPos</strong> : Model da posição de JiuJitsu criada pelos professores e aprendida pelos alunos.
<h2>O que funcionou?</h2>
Tudo que foi proposto no trabalho e mencionado acima é funcional. 
<h1>Instalação</h1>
Você irá abrir uma pasta no seu terminal e rodar esses comandos:<br>
git clone https://github.com/arthurprioli/trabalho2-progweb.git<br>
git clone https://github.com/arthurprioli/INF1407-backend-bjj.git<br>
Dessa maneira você terá instalado os dois repositórios, de front e backend respectivamente.

<h1>Instruções / Manual do usuário</h1>
Após clonar os repositórios vc irá abrir dois terminais e entrar no caminho dos repositórios e executar esse comando no terminal do frontend:<br>
cd .\frontend\public\<br>
python -m http.server 8080<br>
e esses comando no do backend:<br>
python -m venv .venv<br>
. .\.venv\Scripts\activate<br>
pip install -r requirements.txt
python .\LabJJ\manage.py runserver
Agora abra seu navegador e digite :<br>
http://127.0.0.1:8080<br>
para testar o swagger do backend é :<br>
http://127.0.0.1:8000/swagger/<br>


## Instruções para Rodar via Docker

1. Instale o Docker.
2. Puxe a imagem: `docker pull arthurprioli/t2-backend:latest`
3. Rode: `docker run -p 8000:8000 arthurprioli/t2-backend:latest`
4. Acesse http://localhost:8000 (para Swagger, acesse /api-docs ou o endpoint configurado).
5. Para CRUD: use ferramentas como Postman ou o frontend.
6. Nota: Use credenciais de teste (ex: user: admin, pass: 123). Dados SQLite não persistem após stop.
