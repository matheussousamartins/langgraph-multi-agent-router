# LangGraph Multi-Agent Router

Sistema multiagente construído com **LangGraph**, implementando roteamento semântico de intenções, subgrafos especializados e execução de tarefas com ferramentas (ToolNode), seguindo o padrão **ReAct (Reason + Act)**.

Este projeto demonstra uma arquitetura modular e escalável para agentes baseados em grafos, com separação clara de responsabilidades entre classificação, resposta conceitual, pesquisa aprofundada e execução estruturada de tarefas.

## Objetivo

Demonstrar na prática:

- Arquitetura multiagente baseada em grafos
- Roteamento dinâmico de intenções via LLM
- Subgrafos especializados (FAQ, Research, Task)
- Execução de ferramentas com ToolNode
- Implementação do padrão ReAct
- Integração com LangGraph Studio
- Separação clara entre definição do grafo e execução

## Arquitetura

![Fluxo principal:](docs/fluxo.png)


## Componentes

### Router

Responsável por classificar a intenção do usuário em:

-   **faq**: Perguntas conceituais ou simples
-   **research**: Explicações técnicas e aprofundadas
-   **task**: Execução estruturada de tarefas

A decisão é feita dinamicamente por um modelo LLM.

### FAQ Graph

Subgrafo especializado para respostas objetivas e técnicas sobre LangGraph.

-   Uso de `SystemMessage` para controlar comportamento
-   Respostas diretas e contextualizadas

### Research Graph

Subgrafo voltado para explicações aprofundadas.

-   Prompt especializado
-   Respostas longas e analíticas

### Task Graph (ReAct Agent)

Agente executor baseado no padrão ReAct:

-   LLM decide quando usar ferramenta
-   `ToolNode` executa
-   Resultado retorna ao agente
-   Finalização da resposta

Ferramenta implementada:

-   `generate_structured_plan`: Gera planos estruturados para objetivos técnicos.

## Padrão Arquitetural Utilizado

Este projeto utiliza:

-   `StateGraph`
-   `add_conditional_edges`
-   `ToolNode`
-   Subgraphs compilados
-   State tipado com `TypedDict`
-   Execução compatível com LangGraph Studio

## Como Executar Localmente

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar variável de ambiente

Crie um arquivo `.env` na raiz do projeto e adicione sua chave de API do OpenAI:

```dotenv
OPENAI_API_KEY=sua_chave_aqui
```

### 3. Rodar no modo Studio

```bash
langgraph dev
```

Abra seu navegador e acesse:

`http://127.0.0.1:2024`

## Exemplos de Uso

-   **FAQ**: `O que é LangGraph?`
-   **Research**: `Explique profundamente como funciona o StateGraph e suas implicações arquiteturais.`
-   **Task**: `Crie um roadmap para aprender LangGraph em 30 dias.`

## Decisões de Design

-   Separação entre definição de grafo e execução
-   Uso de subgrafos para modularidade
-   Roteamento semântico com fallback seguro
-   Tool calling contextual (não didático)
-   Arquitetura preparada para expansão (RAG, múltiplos agentes, persistência externa)

## Possíveis Evoluções

-   Implementação de RAG no Research Graph
-   Persistência externa (Postgres)
-   Paralelismo entre subagentes
-   Observabilidade via LangSmith
-   Deploy via LangGraph Cloud

## Diferenciais Técnicos

-   Arquitetura multiagente real
-   Padrão ReAct implementado manualmente
-   Separação clara de responsabilidades
-   Compatível com LangGraph Studio
-   Estrutura pronta para produção

## Estrutura do Projeto

```
langgraph-multi-agent-router/
├── graphs/
│   ├── router.py
│   ├── faq_graph.py
│   ├── research_graph.py
│   ├── task_graph.py
│   └── tools.py
├── state.py
├── app.py
├── langgraph.json
└── README.md
```

## Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
