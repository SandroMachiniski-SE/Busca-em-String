🔍 Comparador de Algoritmos de Busca em Strings
Uma aplicação web interativa para explorar, visualizar e comparar diferentes algoritmos de busca de padrões em textos.

📋 Descrição
Esta aplicação permite implementar e testar 4 algoritmos clássicos de busca em strings:

Naive Search (Força Bruta)
Rabin-Karp (Hash)
Knuth-Morris-Pratt (KMP)
Boyer-Moore
Visualize a execução passo a passo, compare desempenho e entenda como cada algoritmo funciona.

✨ Funcionalidades
✅ Upload de arquivos .txt ou cole texto diretamente
✅ Busca com múltiplos algoritmos simultaneamente
✅ Modo passo a passo (debug) com visualização detalhada
✅ Métricas de desempenho em tempo real:
Tempo de execução (ms)
Número de comparações
Posições encontradas
✅ Exibição de estruturas auxiliares:
Tabela LPS (KMP)
Tabela Bad Character (Boyer-Moore)
Hash do padrão (Rabin-Karp)
✅ Interface responsiva e intuitiva
✅ Padrão Strategy para arquitetura extensível
🚀 Como Usar
Pré-requisitos
Python 3.7+
Flask
pip
Instalação
bash
Copiar

# Clone ou baixe o projeto
cd comparador-algoritmos-busca

# Instale as dependências
pip install flask

# Execute a aplicação
python app.py
Acessar a Aplicação
Abra seu navegador e acesse:

http://localhost:5000
Usando a Aplicação
Carregar Texto:

Clique em "Carregar arquivo .txt" para fazer upload
Ou cole o texto diretamente na textarea
Inserir Padrão:

Digite a string que deseja buscar
Executar Busca:

Clique em "Executar Busca" para resultado rápido
Clique em "Passo a Passo" para visualizar cada etapa
Analisar Resultados:

Compare tempo, comparações e complexidade
Veja as posições onde o padrão foi encontrado
📁 Estrutura do Projeto
comparador-algoritmos-busca/
├── app.py                 # Aplicação Flask (backend)
├── templates/
│   └── index.html        # Interface web (frontend)
├── README.md             # Este arquivo
└── requirements.txt      # Dependências (opcional)
🏗️ Arquitetura
A aplicação usa o padrão Strategy para implementar os algoritmos:

python
Copiar

SearchStrategy (interface abstrata)
├── NaiveSearch
├── RabinKarpSearch
├── KMPSearch
└── BoyerMooreSearch
Cada algoritmo implementa a interface SearchStrategy com o método search().

📊 Complexidade dos Algoritmos
Algoritmo	Pior Caso	Caso Médio	Melhor Caso	Espaço
Naive	O(n × m)	O(n × m)	O(n)	O(1)
Rabin-Karp	O(n × m)	O(n + m)	O(n + m)	O(1)
KMP	O(n + m)	O(n + m)	O(n + m)	O(m)
Boyer-Moore	O(n × m)	O(n / m)	O(n / m)	O(σ)

Exportar

Copiar
💡 Quando Usar Cada Algoritmo
Naive Search
✅ Padrões muito curtos (1-3 caracteres)
✅ Textos pequenos (< 1.000 caracteres)
✅ Fins educacionais
Rabin-Karp
✅ Múltiplos padrões simultaneamente
✅ Detecção de plágio
✅ Busca em 2D (imagens)
KMP
✅ Garantia de complexidade linear necessária
✅ Padrões com muitas repetições
✅ Sistemas em tempo real
Boyer-Moore
✅ Melhor escolha geral para padrões longos
✅ Editores de texto (Ctrl+F)
✅ Processamento de documentos
🎯 Exemplos de Uso
Exemplo 1: Busca Simples
Texto: "banana"
Padrão: "ana"
Resultado: Encontrado em [1, 3]
Exemplo 2: Múltiplas Ocorrências
Texto: "AABAACAADAABAABA"
Padrão: "AABA"
Resultado: Encontrado em [0, 9, 12]
Exemplo 3: Padrão Não Encontrado
Texto: "hello world"
Padrão: "xyz"
Resultado: Nenhuma ocorrência
🔧 Endpoints da API
POST /api/search
Executa a busca com todos os algoritmos.

Request:

json
Copiar

{
  "text": "seu texto aqui",
  "pattern": "padrão",
  "step_by_step": false
}
Response:

json
Copiar

{
  "results": [
    {
      "algorithm": "Naive Search",
      "matches": [0, 5, 10],
      "comparisons": 150,
      "time_ms": 0.5234,
      "complexity": "O(n * m)",
      "steps": []
    }
  ],
  "comparison": {
    "fastest": "Boyer-Moore",
    "fastest_time": 0.2341,
    "least_comparisons": "KMP",
    "least_comparisons_count": 45
  }
}
POST /api/upload
Faz upload de arquivo .txt.

Request: multipart/form-data com arquivo

Response:

json
Copiar

{
  "content": "conteúdo do arquivo",
  "filename": "documento.txt"
}
📝 Exemplo de Arquivo de Teste
Crie um arquivo teste.txt:

O algoritmo de busca em strings é fundamental em ciência da computação.
A busca eficiente permite encontrar padrões rapidamente em textos grandes.
Diferentes algoritmos têm diferentes características de desempenho.
🎓 Aprendizado
Esta aplicação é ideal para:

Estudar algoritmos de busca
Entender complexidade de tempo e espaço
Visualizar execução passo a passo
Comparar desempenho prático vs teórico
Trabalhos acadêmicos e apresentações
📚 Referências
Cormen et al. - Introduction to Algorithms (3rd ed.)
Knuth, Morris & Pratt - Fast pattern matching in strings
Boyer & Moore - A fast string searching algorithm
Rabin & Karp - Efficient randomized pattern-matching algorithms
🐛 Troubleshooting
Erro: "Port 5000 already in use"

bash
Copiar

# Use outra porta
python app.py --port 5001
Arquivo não carrega

Certifique-se que é um arquivo .txt
Máximo 16MB por arquivo
Aplicação lenta com textos muito grandes

Textos > 1MB podem ser lentos
Use padrões específicos para melhor desempenho
📄 Licença
Este projeto é fornecido para fins educacionais.
