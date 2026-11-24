# -*- coding: utf-8 -*-
"""
Conteúdo aprofundado (escrito à mão) para as certificações mais buscadas.
Usado pelo gerar.py: cada código abaixo ganha, na sua página, as seções
"Plano de estudo", "O que mais confunde na prova", "Vale a pena?" e a comparação.

Campos:
  semanas:   [(título da semana, o que estudar, como praticar)]
  confusoes: [(tema, explicação curta)]
  vale:      parágrafo sobre para quem vale a pena (e para quem não vale)
  compara:   (código da outra certificação, título da comparação, [parágrafos])
  dica:      um conselho final para o dia da prova
Regras: nada de preço, número de questões ou datas que não estejam nos dados oficiais.
"""

EXTRA = {

"AZ-900": dict(
    semanas=[
        ("Conceitos de nuvem", "Modelos de serviço (IaaS, PaaS, SaaS), modelos de implantação (pública, privada, híbrida), modelo de responsabilidade compartilhada, CapEx x OpEx, elasticidade, escalabilidade e alta disponibilidade.",
         "Monte uma tabela com um exemplo real de cada modelo de serviço e marque, em cada um, o que é responsabilidade sua e o que é da Microsoft."),
        ("Arquitetura e serviços do Azure", "Regiões, pares de regiões, zonas de disponibilidade, grupos de recursos e assinaturas; máquinas virtuais, App Service, contêineres e Functions; redes virtuais, VPN e ExpressRoute; tipos de armazenamento e camadas de acesso.",
         "Crie uma conta gratuita do Azure, suba uma máquina virtual pequena e uma conta de armazenamento, e apague tudo no fim para não gerar custo."),
        ("Identidade, governança e custos", "Microsoft Entra ID, autenticação multifator e acesso condicional, RBAC, Azure Policy, bloqueios de recursos, tags, calculadora de preços, calculadora de TCO e Cost Management.",
         "Aplique uma tag e um bloqueio de exclusão no grupo de recursos que você criou e veja o que acontece ao tentar apagá-lo."),
        ("Revisão e simulados", "Ferramentas de gerenciamento (portal, CLI, PowerShell, ARM e Bicep), Azure Monitor, Service Health e Advisor. Releia as áreas em que você errou mais.",
         "Faça simulados completos e só agende a prova quando passar de 800 com folga em pelo menos dois seguidos."),
    ],
    confusoes=[
        ("Zona de disponibilidade x par de regiões", "Zona protege contra a falha de um datacenter dentro da mesma região. Par de regiões protege contra um desastre na região inteira e define a ordem de recuperação da Microsoft."),
        ("RBAC x Azure Policy x bloqueio", "RBAC diz quem pode fazer o quê. Policy diz quais configurações são permitidas, para qualquer pessoa. O bloqueio impede apagar ou alterar um recurso, mesmo para quem tem permissão."),
        ("Calculadora de preços x calculadora de TCO", "A de preços estima o custo de serviços que você vai usar no Azure. A de TCO compara o custo de manter a infraestrutura no seu datacenter com o custo de migrar para o Azure."),
        ("Escalabilidade x elasticidade", "Escalabilidade é a capacidade de aumentar recursos. Elasticidade é fazer isso automaticamente, para cima e para baixo, conforme a demanda."),
        ("Camadas de acesso do Blob Storage", "Hot é para dados acessados com frequência, Cool e Cold para acesso cada vez mais raro e Archive para guardar por muito tempo, com custo baixo de armazenamento e alto de leitura e espera para recuperar."),
    ],
    vale="Vale a pena para quem está começando em nuvem, para quem trabalha com vendas, compras ou gestão de projetos que envolvem Azure e para quem quer um primeiro selo no currículo antes de uma certificação técnica. Ela não expira e não exige experiência. Para quem já administra o Azure no dia a dia, ela é opcional: dá para ir direto à AZ-104.",
    compara=("SC-900", "AZ-900 ou SC-900: qual fazer primeiro?", [
        "Faça a AZ-900 primeiro se o seu objetivo é infraestrutura, desenvolvimento ou dados no Azure. Ela dá o vocabulário de nuvem que todas as outras provas assumem que você já tem.",
        "Faça a SC-900 primeiro se você quer seguir para segurança, identidade ou conformidade. Ela fala menos de serviços do Azure e mais de Microsoft Entra, Defender, Sentinel e Purview.",
        "As duas são Fundamentals, não expiram e se complementam. Muita gente faz as duas em sequência: os temas de identidade e segurança da AZ-900 reaparecem, com mais profundidade, na SC-900.",
    ]),
    dica="A prova cobra o conceito certo para cada cenário. Quando duas alternativas parecerem corretas, procure a palavra que define o requisito: custo, disponibilidade, conformidade ou controle.",
),

"SC-900": dict(
    semanas=[
        ("Conceitos e identidade", "Zero Trust, defesa em profundidade, modelo de responsabilidade compartilhada, criptografia e hashing, autenticação x autorização, provedores de identidade e federação. Tipos de identidade no Microsoft Entra ID, autenticação multifator, acesso condicional e governança de identidade.",
         "Abra o centro de administração do Microsoft Entra (um locatário de desenvolvedor ou de avaliação serve) e veja onde ficam usuários, grupos e políticas de acesso condicional."),
        ("Soluções de segurança", "Segurança de infraestrutura no Azure (NSG, Firewall, DDoS Protection, Bastion), Microsoft Defender for Cloud, Microsoft Sentinel (SIEM e SOAR) e a família Microsoft Defender XDR.",
         "Faça um mapa com uma linha por produto: o que ele protege, quem usa e um exemplo de alerta que ele gera."),
        ("Conformidade com o Microsoft Purview", "Portal de Confiança do Serviço, Compliance Manager, rótulos de confidencialidade, prevenção contra perda de dados (DLP), retenção, gestão de registros, risco interno, eDiscovery e auditoria.",
         "Para cada recurso do Purview, escreva uma pergunta de negócio que ele responde, por exemplo: \"como impedir que um CPF saia por e-mail?\" (DLP)."),
        ("Revisão e simulados", "Revise a área de soluções de segurança, que é a de maior peso, e os pontos de licenciamento que aparecem nos cenários.",
         "Faça simulados completos e anote as alternativas que confundem produtos parecidos; revise só esses pares no dia anterior."),
    ],
    confusoes=[
        ("Microsoft Sentinel x Microsoft Defender XDR", "O Sentinel é o SIEM e SOAR na nuvem: junta registros de muitas fontes, inclusive de fora da Microsoft, e automatiza respostas. O Defender XDR correlaciona alertas dos produtos Defender (endpoint, identidade, e-mail, apps) num só incidente."),
        ("Defender for Cloud x Defender XDR", "O Defender for Cloud cuida da postura e da proteção de cargas de nuvem (Azure, outras nuvens e servidores). O Defender XDR cuida de usuários, dispositivos, e-mail e apps do Microsoft 365."),
        ("Rótulo de confidencialidade x rótulo de retenção", "O de confidencialidade classifica e protege o conteúdo (criptografia, marca d'água). O de retenção define por quanto tempo o conteúdo é guardado ou quando é apagado."),
        ("Autenticação x autorização", "Autenticação prova quem você é. Autorização define o que você pode fazer depois de entrar."),
        ("NSG x Azure Firewall", "O NSG filtra tráfego por IP, porta e protocolo na sub-rede ou na placa de rede. O Azure Firewall é um serviço gerenciado e central, com regras de aplicação, inteligência de ameaças e registro de tudo que passa."),
    ],
    vale="Vale a pena para quem quer entrar em segurança da informação, para profissionais de TI que passaram a cuidar de identidade ou conformidade e para quem trabalha com auditoria, jurídico ou proteção de dados (LGPD) e precisa entender as ferramentas da Microsoft. Não exige experiência e não expira. Para quem já atua num SOC, ela é um degrau curto; o ganho maior está na SC-200.",
    compara=("SC-200", "SC-900 ou direto para a SC-200?", [
        "A SC-900 mostra o mapa: o que cada produto de segurança, identidade e conformidade faz. A SC-200 exige operar esses produtos, escrever consultas KQL e investigar incidentes no Defender XDR e no Sentinel.",
        "Se você nunca trabalhou com segurança, comece pela SC-900: ela evita que a SC-200 vire um choque de nomes e produtos.",
        "Se você já é analista de SOC, pode ir direto para a SC-200. A SC-900 não é pré-requisito de nenhuma certificação.",
    ]),
    dica="Muitas questões trazem um requisito e pedem o produto. Antes de olhar as alternativas, responda mentalmente: isso é identidade (Entra), proteção contra ameaças (Defender ou Sentinel) ou dados e conformidade (Purview)?",
),

"AI-901": dict(
    semanas=[
        ("Conceitos de IA e IA responsável", "Cargas de trabalho de IA (visão, linguagem, fala, extração de informações, IA generativa e agentes), os seis princípios de IA responsável da Microsoft e os componentes de um modelo: parâmetros, tokens, temperatura, prompt de sistema.",
         "Escreva um exemplo de risco para cada princípio de IA responsável e como evitá-lo num app real."),
        ("Microsoft Foundry: apps e agentes generativos", "Recursos e projetos do Foundry, catálogo de modelos, playground de chat, prompts de sistema, fundamentação com dados próprios (RAG), filtros de conteúdo e criação de agentes.",
         "No Microsoft Foundry, implante um modelo de chat, teste prompts no playground e crie um agente simples com instruções e uma fonte de conhecimento."),
        ("Texto, fala, visão e extração", "Análise de texto, tradução, fala para texto e texto para fala, visão computacional, geração de imagens e extração de informações de documentos.",
         "Teste cada serviço pelo portal com arquivos seus: um áudio, uma foto e um PDF de nota fiscal ou formulário."),
        ("Revisão e simulados", "A parte de implementação com o Foundry vale mais da metade da prova. Revise a ordem dos passos e as configurações de cada tipo de solução.",
         "Faça simulados completos e, a cada erro, refaça no portal o passo que você errou."),
    ],
    confusoes=[
        ("AI-900 x AI-901", "A AI-901 substituiu a AI-900. Ela mantém os conceitos de IA, mas dá muito mais peso à prática no Microsoft Foundry, com IA generativa e agentes. Material de estudo antigo da AI-900 cobre só parte da prova."),
        ("Temperatura x prompt de sistema", "A temperatura controla o quanto a resposta varia (mais baixa, mais previsível). O prompt de sistema define o papel, o tom e os limites do modelo."),
        ("Fundamentação (RAG) x ajuste fino", "Fundamentar é dar ao modelo os seus documentos na hora da pergunta, sem treiná-lo de novo. Ajuste fino muda o comportamento do modelo com novos exemplos de treino."),
        ("Agente x app de chat", "Um app de chat responde a perguntas. Um agente recebe um objetivo, usa ferramentas e fontes de conhecimento e pode executar várias etapas para cumpri-lo."),
        ("Filtros de conteúdo x IA responsável", "Os filtros bloqueiam entradas e saídas nocivas em tempo real. IA responsável é o conjunto de princípios que orienta todo o projeto, do dado usado até a forma de apresentar o resultado."),
    ],
    vale="Vale a pena para quem quer entender IA generativa e agentes na prática, para desenvolvedores e analistas que vão usar o Microsoft Foundry e para profissionais de negócio que precisam conversar com times técnicos sobre IA. Não exige programação avançada. Quem já tem a AI-900 continua certificado; a AI-901 é o caminho para quem está começando agora.",
    compara=("AZ-900", "AI-901 ou AZ-900 primeiro?", [
        "A AZ-900 ensina a base do Azure: regiões, assinaturas, custos e governança. A AI-901 assume que você entende o básico de nuvem e vai direto para modelos, agentes e serviços de IA.",
        "Se você nunca usou o Azure, a AZ-900 deixa a AI-901 mais fácil, porque o Foundry usa os mesmos conceitos de recursos, assinaturas e permissões.",
        "Se o seu foco é IA e você já navega no portal do Azure, pode começar pela AI-901. Nenhuma das duas é pré-requisito da outra.",
    ]),
    dica="Nos cenários de implementação, siga a ordem natural do trabalho no Foundry: criar o recurso ou projeto, escolher e implantar o modelo, configurar e testar. Alternativas fora dessa ordem costumam estar erradas.",
),

"AZ-104": dict(
    semanas=[
        ("Identidade e governança", "Usuários e grupos no Microsoft Entra ID, unidades administrativas, RBAC com funções internas e personalizadas, Azure Policy, bloqueios, tags, grupos de gerenciamento e orçamentos.",
         "Crie um usuário, dê a ele a função Leitor num grupo de recursos e confirme no portal o que ele consegue e o que não consegue fazer."),
        ("Armazenamento", "Contas de armazenamento, redundância (LRS, ZRS, GRS, GZRS), camadas de acesso e regras de ciclo de vida, chaves de acesso e SAS, Azure Files, Blob Storage e AzCopy.",
         "Gere uma SAS com validade de uma hora para um contêiner e teste o acesso antes e depois do vencimento."),
        ("Computação", "Máquinas virtuais, conjuntos de dimensionamento, conjuntos e zonas de disponibilidade, ARM templates e Bicep, Azure Container Instances, Container Apps e App Service com slots de implantação.",
         "Implante a mesma VM pelo portal e por um arquivo Bicep, e redimensione-a; depois publique um app no App Service usando um slot de homologação."),
        ("Redes", "Redes virtuais e sub-redes, emparelhamento, NSG e ASG, rotas definidas pelo usuário, Azure Bastion, endpoints de serviço e privados, DNS do Azure, Load Balancer e Application Gateway.",
         "Monte duas redes emparelhadas com uma VM em cada e libere só a porta necessária no NSG; teste com o Network Watcher."),
        ("Monitoramento e backup", "Azure Monitor, métricas, logs e alertas, Log Analytics, Network Watcher, Azure Backup e Site Recovery.",
         "Crie um alerta de CPU para uma VM e um backup com política diária; restaure um arquivo."),
        ("Revisão e simulados", "Revise os temas em que errou e refaça os laboratórios correspondentes.",
         "Faça simulados cronometrados de 100 minutos; a AZ-104 tem cenários longos e o tempo pesa."),
    ],
    confusoes=[
        ("LRS x ZRS x GRS x GZRS", "LRS copia os dados dentro de um datacenter, ZRS entre zonas da mesma região, GRS para uma região secundária e GZRS combina zonas na primária com a cópia para a secundária."),
        ("Conjunto de disponibilidade x zona de disponibilidade", "O conjunto espalha as VMs por racks e domínios de atualização dentro de um datacenter. A zona coloca as VMs em datacenters diferentes da mesma região, com proteção maior."),
        ("Endpoint de serviço x endpoint privado", "O endpoint de serviço leva o tráfego da sub-rede ao serviço pela rede da Microsoft, mas o serviço continua com IP público. O endpoint privado dá ao serviço um IP privado dentro da sua rede virtual."),
        ("Load Balancer x Application Gateway", "O Load Balancer distribui tráfego na camada 4 (IP e porta). O Application Gateway trabalha na camada 7 (HTTP), com roteamento por caminho, terminação TLS e firewall de aplicação web."),
        ("Chave de acesso x SAS", "A chave dá acesso total à conta de armazenamento. A SAS dá acesso limitado por tempo, permissão e recurso, e é a opção certa para compartilhar com terceiros."),
    ],
    vale="Vale a pena para quem administra ou quer administrar ambientes Azure, para analistas de infraestrutura migrando para nuvem e para quem mira cargos de cloud engineer. É uma das certificações do Azure mais pedidas em vagas e é pré-requisito da AZ-305 (arquiteto). Para quem só precisa entender a nuvem sem operá-la, a AZ-900 basta.",
    compara=("AZ-305", "AZ-104 x AZ-305: qual a diferença?", [
        "A AZ-104 pergunta como fazer: configurar, implantar e corrigir recursos. A AZ-305 pergunta o que escolher: desenhar a solução que atende requisitos de custo, disponibilidade, segurança e conformidade.",
        "Para receber a certificação de arquiteto (AZ-305), a Microsoft exige ter a AZ-104. Por isso a ordem natural é AZ-104 primeiro.",
    ]),
    dica="Leia o fim da pergunta primeiro: o requisito (\"com o menor custo\", \"sem tempo de inatividade\", \"com o mínimo de esforço administrativo\") decide entre alternativas tecnicamente corretas.",
),

"PL-300": dict(
    semanas=[
        ("Preparar os dados", "Conexão a fontes (Excel, SQL, SharePoint, web), modos de armazenamento, perfil de dados, Power Query: tipos, colunas calculadas na consulta, mesclar e acrescentar consultas, dinamizar e despivotar, parâmetros.",
         "Pegue uma planilha bagunçada do seu trabalho e limpe tudo só com o Power Query, sem editar o arquivo original."),
        ("Modelar os dados", "Esquema estrela, tabelas fato e dimensão, relacionamentos e cardinalidade, direção de filtro, tabela de datas, hierarquias e funções de papel.",
         "Transforme uma tabela única de vendas num modelo estrela com dimensões de produto, cliente e data."),
        ("DAX", "Medidas x colunas calculadas, contexto de linha e de filtro, CALCULATE, funções de inteligência de tempo (acumulado no ano, mesmo período do ano anterior), variáveis e funções de iteração (SUMX).",
         "Escreva medidas de total, acumulado no ano, variação em relação ao ano anterior e porcentagem do total, e confira os resultados numa matriz."),
        ("Visualizar e analisar", "Escolha do visual certo, formatação condicional, segmentações, indicadores e botões, dicas de ferramenta, detalhamento, análise de tendências e anomalias, design para celular.",
         "Monte um relatório de duas páginas com navegação por botões e uma página de detalhe acessada por drill-through."),
        ("Gerenciar e proteger", "Workspaces e funções, aplicativos, atualização agendada e gateway, segurança em nível de linha (RLS), rótulos de confidencialidade, endosso e compartilhamento.",
         "Crie uma regra de RLS por região e teste com \"Exibir como função\" antes de publicar."),
        ("Revisão e simulados", "As três primeiras áreas valem quase o mesmo; revise a que tiver mais erros.",
         "Faça simulados e repita no Power BI Desktop todo exercício de DAX que você errou."),
    ],
    confusoes=[
        ("Medida x coluna calculada", "A coluna calculada é gravada linha a linha no modelo e ocupa memória. A medida é calculada na hora, no contexto do visual, e é a escolha certa para totais e porcentagens."),
        ("Mesclar x acrescentar consultas", "Mesclar junta colunas de duas tabelas por uma chave (como um PROCV). Acrescentar empilha as linhas de tabelas com a mesma estrutura."),
        ("Importação x DirectQuery", "Na importação, os dados ficam no modelo e o relatório é rápido, mas depende de atualização. No DirectQuery, cada visual consulta a fonte na hora: dados mais recentes, desempenho menor e algumas limitações de DAX."),
        ("Filtro de relatório x segmentação x RLS", "Filtros e segmentações mudam o que o usuário vê por escolha dele. A RLS restringe as linhas por quem ele é, e o usuário não consegue removê-la."),
        ("Workspace x aplicativo", "O workspace é onde o time cria e edita. O aplicativo é o pacote publicado para os consumidores, com navegação própria e sem acesso de edição."),
    ],
    vale="Vale a pena para analistas de dados e de negócio, para quem já usa Excel avançado e quer migrar para o Power BI e para quem quer uma certificação muito presente em vagas de BI. É prática: quem nunca montou um relatório no Power BI Desktop deve fazer alguns projetos antes. Para quem só consome relatórios, a PL-900 ou a DP-900 são suficientes.",
    compara=("DP-600", "PL-300 x DP-600: qual escolher?", [
        "A PL-300 é sobre construir relatórios e modelos no Power BI. A DP-600 vai um nível acima: preparar dados em escala no Microsoft Fabric, com lakehouses, warehouses, notebooks e modelos semânticos grandes.",
        "Para quem está começando em BI, a PL-300 vem primeiro. A DP-600 aproveita boa parte do conteúdo de modelagem e DAX da PL-300.",
        "Se você já trabalha com engenharia de dados ou com o Fabric, a DP-600 conversa mais com o seu dia a dia.",
    ]),
    dica="Nas questões de DAX, identifique primeiro o contexto: a fórmula vai rodar numa coluna (linha a linha) ou numa medida (no filtro do visual)? Isso elimina metade das alternativas.",
),

"PL-900": dict(
    semanas=[
        ("Valor de negócio e ambientes", "O que é o Power Platform e onde cada produto entra, ambientes, Microsoft Dataverse (tabelas, colunas, relacionamentos), conectores, segurança e políticas de prevenção contra perda de dados (DLP) no centro de administração.",
         "Crie um ambiente de desenvolvedor gratuito e uma tabela no Dataverse com três colunas e um relacionamento."),
        ("Power Apps", "Apps de tela x apps baseados em modelo, criação a partir de dados, formulários e galerias, compartilhamento e quando usar cada tipo.",
         "Crie um app de tela a partir de uma lista do SharePoint ou da tabela do Dataverse e compartilhe com um colega."),
        ("Power Automate", "Fluxos de nuvem (automatizados, instantâneos e agendados), fluxos da área de trabalho (RPA), aprovações, gatilhos e ações, conectores padrão e premium.",
         "Monte um fluxo que, ao receber um anexo por e-mail, salva no OneDrive e pede aprovação no Teams."),
        ("Agentes no Copilot Studio", "Criação de agentes, tópicos, fontes de conhecimento, ações, canais de publicação e gerenciamento de agentes.",
         "Crie um agente que responde dúvidas a partir de um site ou documento seu e publique no Teams."),
        ("Revisão e simulados", "As quatro áreas técnicas têm pesos parecidos; não deixe nenhuma de fora.",
         "Faça simulados e revise as diferenças entre tipos de app e tipos de fluxo, que caem muito."),
    ],
    confusoes=[
        ("App de tela x app baseado em modelo", "O de tela começa do layout e se liga a muitas fontes de dados. O baseado em modelo começa dos dados no Dataverse e gera a interface automaticamente, com formulários e visões padrão."),
        ("Fluxo de nuvem x fluxo da área de trabalho", "O de nuvem conecta serviços online por APIs e conectores. O da área de trabalho (RPA) automatiza cliques e digitação em sistemas antigos que não têm API."),
        ("Dataverse x SharePoint", "O Dataverse é um banco de dados com relacionamentos, regras de negócio e segurança por linha. O SharePoint guarda listas e documentos; serve para cenários simples, mas não substitui o Dataverse em apps complexos."),
        ("Conector padrão x premium", "Os padrão (como Outlook e SharePoint) já vêm na maioria das licenças do Microsoft 365. Os premium (como SQL Server e HTTP) exigem uma licença do Power Apps ou do Power Automate."),
    ],
    vale="Vale a pena para profissionais de qualquer área que querem automatizar tarefas, para quem trabalha com processos e planilhas no Microsoft 365 e para quem quer entrar no mundo low-code. Não exige programação nem experiência em TI, e não expira. Para quem já desenvolve soluções no Power Platform, o próximo passo é uma certificação Associate.",
    compara=("PL-300", "PL-900 ou PL-300?", [
        "A PL-900 cobre todo o Power Platform em nível básico: Power Apps, Power Automate, Dataverse e agentes no Copilot Studio, além de uma visão do Power BI.",
        "A PL-300 é só Power BI, em profundidade: Power Query, modelagem, DAX e governança.",
        "Se o seu objetivo é análise de dados, vá direto para a PL-300. Se você quer automatizar processos e criar apps, a PL-900 é o começo certo.",
    ]),
    dica="Quando a questão citar \"sem código\" ou \"usuário de negócio\", a resposta tende a ser o recurso mais simples e pronto (modelo, conector padrão, criação a partir de dados), não uma solução personalizada.",
),

"DP-900": dict(
    semanas=[
        ("Conceitos de dados", "Dados estruturados, semiestruturados e não estruturados, formatos de arquivo (CSV, JSON, Parquet), processamento transacional (OLTP) x analítico (OLAP), e os papéis em dados: administrador de banco, engenheiro e analista.",
         "Pegue um mesmo conjunto de dados e salve em CSV, JSON e Parquet; compare tamanho e legibilidade."),
        ("Dados relacionais no Azure", "Tabelas, chaves, normalização, SQL básico (SELECT, INSERT, UPDATE, DELETE, JOIN), visões, índices e procedimentos. Azure SQL Database, Instância Gerenciada de SQL, SQL Server em VM e os bancos de código aberto gerenciados (PostgreSQL e MySQL).",
         "Crie um Azure SQL Database com o banco de exemplo e escreva consultas com JOIN e GROUP BY."),
        ("Dados não relacionais", "Azure Blob Storage, Data Lake Storage, Azure Files e Table Storage. Azure Cosmos DB e suas APIs (NoSQL, MongoDB, PostgreSQL, Apache Cassandra, Table, Apache Gremlin).",
         "Crie uma conta do Cosmos DB no nível gratuito e grave alguns documentos JSON."),
        ("Analytics", "Ingestão e ETL, data warehouse x data lake x lakehouse, Microsoft Fabric, Azure Databricks, analytics em tempo real e visualização com o Power BI.",
         "Abra uma avaliação do Microsoft Fabric e carregue um arquivo num lakehouse; depois crie um relatório simples."),
        ("Revisão e simulados", "Conceitos fundamentais e analytics são as áreas de maior peso.",
         "Faça simulados e revise principalmente a diferença entre os serviços de banco de dados."),
    ],
    confusoes=[
        ("OLTP x OLAP", "OLTP registra muitas transações pequenas do dia a dia (vendas, cadastros). OLAP consulta grandes volumes de dados históricos para análise e relatórios."),
        ("Azure SQL Database x Instância Gerenciada x SQL em VM", "O SQL Database é o mais gerenciado e serve a um banco. A Instância Gerenciada tem compatibilidade quase total com o SQL Server, ideal para migrar. O SQL em VM dá controle total do sistema operacional e do SQL Server."),
        ("Data lake x data warehouse x lakehouse", "O lake guarda arquivos brutos de qualquer formato. O warehouse guarda dados estruturados e prontos para consulta SQL. O lakehouse junta os dois: arquivos no lake com recursos de tabela e SQL por cima."),
        ("Lote x tempo real", "Em lote, os dados são processados em intervalos (a cada hora, a cada dia). Em tempo real (streaming), cada evento é processado assim que chega."),
    ],
    vale="Vale a pena para quem quer começar em dados (análise, engenharia ou banco de dados), para desenvolvedores que precisam entender as opções de banco no Azure e para profissionais de negócio que trabalham com BI. Não exige experiência e não expira. Quem já trabalha com bancos de dados pode ir direto para uma certificação Associate.",
    compara=("PL-300", "DP-900 ou PL-300?", [
        "A DP-900 dá a visão geral de dados no Azure: tipos de dados, bancos relacionais e não relacionais e analytics. A PL-300 é prática e focada no Power BI.",
        "Se você quer ser analista de dados e já usa Excel, pode ir direto para a PL-300; a DP-900 ajuda a entender de onde vêm os dados que você vai analisar.",
        "Se você quer seguir para engenharia de dados (DP-600, DP-700) ou administração de banco (DP-300), comece pela DP-900.",
    ]),
    dica="Muitas questões pedem o serviço certo para um tipo de dado. Classifique o dado primeiro (relacional, documento, arquivo, evento) e só depois olhe as alternativas.",
),

"AZ-305": dict(
    semanas=[
        ("Identidade, governança e monitoramento", "Desenho de autenticação e autorização com Microsoft Entra ID, identidades gerenciadas, Key Vault, grupos de gerenciamento, Azure Policy em escala, estratégia de logs e monitoramento com Azure Monitor e Log Analytics.",
         "Desenhe a hierarquia de grupos de gerenciamento e assinaturas de uma empresa fictícia com três áreas e dois ambientes."),
        ("Armazenamento de dados", "Escolha entre Azure SQL, Cosmos DB, armazenamento e opções analíticas; redundância, camadas, particionamento e integração de dados com Data Factory.",
         "Para três cenários diferentes (cadastro, catálogo global, histórico de logs), escolha o armazenamento e justifique custo, latência e consistência."),
        ("Continuidade de negócios", "RPO e RTO, Azure Backup, Site Recovery, replicação geográfica de bancos, zonas e regiões, e desenho para alta disponibilidade.",
         "Monte uma tabela com RPO e RTO para cada camada de um sistema e a tecnologia que atende cada meta."),
        ("Infraestrutura e aplicações", "Escolha de computação (VM, App Service, contêineres, AKS, Functions), arquitetura de aplicações (filas, mensageria, cache, API Management), rede (hub-spoke, conectividade híbrida, balanceadores) e migração.",
         "Desenhe uma arquitetura hub-spoke com conexão ao datacenter e saída por um firewall central."),
        ("Frameworks e revisão", "Well-Architected Framework (confiabilidade, segurança, custo, excelência operacional, desempenho) e Cloud Adoption Framework.",
         "Pegue uma arquitetura de referência do Azure Architecture Center e identifique como ela atende cada pilar."),
        ("Simulados", "Estudos de caso longos são comuns; treine ler o cenário inteiro antes das perguntas.",
         "Faça simulados cronometrados e revise cada erro pelo requisito que você deixou passar."),
    ],
    confusoes=[
        ("RPO x RTO", "RPO é quanto dado você aceita perder (o ponto no tempo para onde volta). RTO é quanto tempo o sistema pode ficar fora até voltar."),
        ("Alta disponibilidade x recuperação de desastres", "Alta disponibilidade mantém o sistema no ar durante falhas comuns, geralmente dentro de uma região. Recuperação de desastres traz o sistema de volta depois de uma falha grande, normalmente em outra região."),
        ("Azure Front Door x Traffic Manager x Application Gateway", "O Front Door é global e trabalha com HTTP, com cache e WAF. O Traffic Manager é global e decide por DNS. O Application Gateway é regional, na camada 7."),
        ("Identidade gerenciada x entidade de serviço", "A identidade gerenciada é criada e rotacionada pelo Azure para um recurso, sem segredo para guardar. A entidade de serviço é uma identidade de app que você mesmo gerencia, inclusive os segredos ou certificados."),
    ],
    vale="Vale a pena para administradores Azure com experiência que querem passar para arquitetura, para consultores que desenham soluções para clientes e para quem lidera migrações para a nuvem. Exige a AZ-104 para emitir a certificação e muita prática: sem experiência real, os estudos de caso ficam difíceis. Para quem ainda está aprendendo a operar o Azure, a AZ-104 vem antes.",
    compara=("AZ-104", "Por que a AZ-104 vem antes da AZ-305?", [
        "A Microsoft só emite a certificação de arquiteto para quem tem a AZ-104. Além da regra, a AZ-305 supõe que você já sabe configurar o que vai desenhar.",
        "A AZ-104 treina a execução (como configurar). A AZ-305 treina a decisão (o que escolher e por quê, diante de requisitos de custo, disponibilidade e conformidade).",
        "Quem tenta a AZ-305 sem prática costuma errar justamente os detalhes de limite e comportamento dos serviços que a AZ-104 ensina.",
    ]),
    dica="Em cada questão, sublinhe mentalmente o requisito decisivo: menor custo, menor esforço de gestão, maior disponibilidade ou conformidade. A AZ-305 quase sempre tem duas soluções que funcionam; só uma atende esse requisito.",
),

"SC-200": dict(
    semanas=[
        ("KQL", "Kusto Query Language: where, project, summarize, extend, join, render e funções de tempo. Base para tudo no Sentinel e na caça avançada do Defender XDR.",
         "Use o ambiente de demonstração do Log Analytics e escreva consultas que respondem perguntas como \"quais usuários tiveram mais falhas de login na última semana\"."),
        ("Microsoft Sentinel", "Workspaces, conectores de dados, regras de análise (agendadas, quase em tempo real, de anomalias), incidentes, playbooks com Logic Apps, pastas de trabalho e regras de automação.",
         "Ative o Sentinel num workspace de teste, conecte uma fonte e crie uma regra agendada que gera incidente."),
        ("Microsoft Defender XDR", "Incidentes e alertas unificados, Defender for Endpoint (proteção, investigação e resposta em dispositivos), Defender for Office 365, Defender for Identity e Defender for Cloud Apps.",
         "Num locatário de avaliação, explore um incidente de exemplo e siga a linha do tempo do dispositivo envolvido."),
        ("Resposta a incidentes", "Triagem, investigação, ações de resposta (isolar dispositivo, bloquear usuário, quarentena de e-mail), investigação e resposta automatizadas e investigação no Microsoft 365 com o Purview.",
         "Escreva um roteiro de resposta para um caso de phishing, do alerta até o fechamento do incidente."),
        ("Caça a ameaças", "Caça avançada no Defender XDR, consultas de caça e livros de notas no Sentinel, marcadores e transformação de achados em regras de detecção.",
         "Transforme uma consulta de caça que encontrou algo em uma regra de análise agendada."),
        ("Revisão e simulados", "Gerenciar o ambiente de operações é a área de maior peso.",
         "Faça simulados e treine KQL todos os dias por 15 minutos até a prova."),
    ],
    confusoes=[
        ("Regra de análise x regra de automação x playbook", "A regra de análise detecta e gera alertas ou incidentes. A regra de automação reage a incidentes de forma simples (atribuir, marcar, fechar). O playbook (Logic App) executa ações complexas e integra outros sistemas."),
        ("Caça avançada no Defender XDR x caça no Sentinel", "A do Defender XDR consulta os dados dos produtos Defender. A do Sentinel consulta tudo o que foi ingerido no workspace, inclusive fontes de fora da Microsoft."),
        ("Alerta x incidente", "O alerta é um sinal isolado de um produto. O incidente agrupa alertas relacionados ao mesmo ataque para investigação conjunta."),
        ("Isolar dispositivo x restringir execução de apps", "Isolar corta a comunicação de rede do dispositivo, mantendo só a conexão com o Defender. Restringir a execução impede que programas não assinados pela Microsoft rodem."),
    ],
    vale="Vale a pena para analistas de SOC, profissionais de resposta a incidentes e para quem quer trabalhar com segurança operacional usando ferramentas Microsoft. Exige prática com KQL e com os portais do Defender e do Sentinel. Para quem ainda não conhece o ecossistema de segurança da Microsoft, a SC-900 é um bom primeiro passo.",
    compara=("SC-300", "SC-200 ou SC-300?", [
        "A SC-200 é sobre detectar e responder a ataques: Sentinel, Defender XDR e KQL. A SC-300 é sobre identidade: usuários, autenticação, acesso condicional e governança no Microsoft Entra.",
        "Se você quer trabalhar num SOC, vá de SC-200. Se você cuida de contas, acessos e logins da empresa, a SC-300 é mais útil.",
        "As duas abrem caminho para a SC-100 (arquiteto de segurança), que exige uma destas: SC-200, SC-300 ou SC-500.",
    ]),
    dica="Quando a pergunta pedir \"o mínimo de esforço\", prefira o recurso nativo e automático (regra de automação, investigação automatizada) a montar um playbook ou uma consulta do zero.",
),

"SC-300": dict(
    semanas=[
        ("Locatário e identidades de usuários", "Configuração do locatário do Microsoft Entra, domínios personalizados, funções administrativas e unidades administrativas, usuários, grupos e licenças, usuários externos (B2B) e identidade híbrida com sincronização na nuvem e Entra Connect.",
         "Num locatário de desenvolvedor, crie um domínio, um grupo dinâmico e convide um usuário externo."),
        ("Autenticação", "Métodos de autenticação, MFA, autenticação sem senha (passkeys, Windows Hello, Authenticator), redefinição de senha por autoatendimento e proteção de senha.",
         "Ative um método sem senha para um usuário de teste e faça o primeiro login com ele."),
        ("Acesso condicional e proteção", "Políticas de acesso condicional (atribuições, condições, controles), modo somente relatório, ID Protection (risco de usuário e de entrada) e Global Secure Access.",
         "Crie uma política que exige MFA fora da rede da empresa, teste em modo somente relatório e só depois ative."),
        ("Identidades de workload", "Registros de aplicativos, aplicações empresariais, entidades de serviço, identidades gerenciadas, consentimento de permissões e SSO com SAML e OpenID Connect.",
         "Registre um app, dê a ele uma permissão de API e veja como o consentimento de administrador aparece."),
        ("Governança de identidade", "Gerenciamento de direitos (pacotes de acesso), revisões de acesso, Privileged Identity Management (PIM), termos de uso e monitoramento com logs de entrada e auditoria.",
         "Configure o PIM para que a função Administrador Global seja só elegível, com aprovação e tempo limitado."),
        ("Revisão e simulados", "Autenticação e acesso é a área de maior peso; acesso condicional aparece em muitos cenários.",
         "Faça simulados e revise quais recursos dependem de qual licença do Entra ID."),
    ],
    confusoes=[
        ("Acesso condicional x ID Protection", "O acesso condicional aplica regras (exigir MFA, bloquear, exigir dispositivo em conformidade) quando as condições batem. O ID Protection calcula o risco do usuário e da entrada, e esse risco pode virar condição numa política."),
        ("Registro de app x aplicação empresarial", "O registro é a definição do app (a identidade global dele). A aplicação empresarial é a instância desse app dentro do seu locatário, onde você atribui usuários e configura o SSO."),
        ("PIM x gerenciamento de direitos", "O PIM controla funções privilegiadas com ativação por tempo limitado. O gerenciamento de direitos entrega pacotes de acesso (grupos, apps, sites) a usuários comuns e externos, com aprovação e expiração."),
        ("Usuário convidado (B2B) x membro", "O convidado entra com a própria conta da organização de origem e tem permissões padrão mais limitadas. O membro é um usuário do seu locatário."),
    ],
    vale="Vale a pena para administradores de identidade, analistas de infraestrutura que cuidam do Microsoft 365 e do Entra e para quem quer se especializar em Zero Trust. Identidade é o ponto de partida de quase todo ataque, por isso essa função é muito procurada. Para quem ainda não conhece os conceitos de identidade, a SC-900 ajuda a começar.",
    compara=("SC-200", "SC-300 ou SC-200?", [
        "A SC-300 protege a porta de entrada: contas, autenticação e acessos no Microsoft Entra. A SC-200 investiga e responde quando algo já aconteceu, com o Sentinel e o Defender XDR.",
        "Quem administra o Microsoft 365 ou o Azure no dia a dia costuma aproveitar mais a SC-300.",
        "As duas abrem caminho para a SC-100 (arquiteto de segurança). A SC-300 também é uma das opções aceitas para a MS-102 (administrador do Microsoft 365).",
    ]),
    dica="Em perguntas sobre acesso condicional, monte a política na cabeça na ordem do portal: quem (usuários), o quê (apps), quando (condições) e então (controles). A alternativa que pula uma dessas partes costuma estar incompleta.",
),

"DP-600": dict(
    semanas=[
        ("Microsoft Fabric e workspaces", "Capacidades e workspaces, itens do Fabric (lakehouse, warehouse, notebook, pipeline, fluxo de dados, modelo semântico), OneLake, atalhos e o ciclo de vida com Git e pipelines de implantação.",
         "Ative uma avaliação do Fabric, crie um workspace e conecte-o a um repositório Git."),
        ("Obter e transformar dados", "Pipelines e Dataflow Gen2, notebooks com PySpark, lakehouse e warehouse, formato Delta, carga incremental, limpeza, desduplicação e modelagem dimensional.",
         "Carregue um arquivo no lakehouse por um pipeline e transforme-o num notebook em tabelas Delta de fato e dimensão."),
        ("Consultar e analisar", "SQL no warehouse e no endpoint SQL do lakehouse, KQL em bancos de dados em tempo real, editor visual de consultas e funções de janela.",
         "Escreva a mesma consulta em SQL no endpoint do lakehouse e no warehouse, e compare o que cada um permite."),
        ("Modelos semânticos", "Modo Direct Lake x importação x DirectQuery, esquema estrela, DAX avançado, grupos de cálculo, campos de parâmetro, agregações e otimização com ferramentas externas.",
         "Crie um modelo em Direct Lake sobre as suas tabelas Delta e meça o desempenho de uma medida com o analisador de desempenho."),
        ("Segurança e governança", "Funções de workspace, permissões de item, segurança em nível de linha, de coluna e de objeto, rótulos de confidencialidade, endosso e linhagem.",
         "Aplique RLS no modelo semântico e uma permissão de item restrita no warehouse; teste com outro usuário."),
        ("Revisão e simulados", "Preparar dados vale quase metade da prova.",
         "Faça simulados e revise a escolha entre lakehouse, warehouse e cada modo de armazenamento."),
    ],
    confusoes=[
        ("Lakehouse x warehouse", "O lakehouse guarda arquivos e tabelas Delta e é trabalhado com Spark, com SQL só leitura pelo endpoint. O warehouse é SQL completo, com escrita por T-SQL e transações."),
        ("Direct Lake x importação x DirectQuery", "Direct Lake lê as tabelas Delta do OneLake direto na memória, sem cópia e sem consulta à fonte a cada visual. Importação copia os dados para o modelo. DirectQuery consulta a fonte a cada interação."),
        ("Pipeline x Dataflow Gen2 x notebook", "O pipeline orquestra e copia dados. O Dataflow Gen2 transforma com Power Query, sem código. O notebook transforma com código (PySpark, SQL) e escala para grandes volumes."),
        ("Atalho x cópia de dados", "O atalho aponta para dados em outro lugar (outro lakehouse, ADLS, S3) sem copiá-los. A cópia duplica os dados e precisa de atualização."),
    ],
    vale="Vale a pena para profissionais de BI que querem ir além do Power BI, para analistas que já dominam DAX e modelagem e para quem trabalha ou vai trabalhar com o Microsoft Fabric. Exige prática com SQL, DAX e um pouco de PySpark. Para quem está começando em BI, a PL-300 vem antes.",
    compara=("PL-300", "DP-600 ou PL-300 primeiro?", [
        "A PL-300 ensina a construir relatórios e modelos no Power BI. A DP-600 usa esse conhecimento e acrescenta engenharia de dados no Fabric: lakehouse, warehouse, pipelines e modelos semânticos grandes.",
        "Quem tem a PL-300 já domina boa parte da área de modelos semânticos e DAX da DP-600, que vale de 25% a 30% da prova.",
        "Se você vem da engenharia de dados e não do BI, a DP-600 pode vir primeiro, mas reforce DAX e modelagem antes.",
    ]),
    dica="Quando a questão falar de \"sem duplicar dados\" ou \"dados mais recentes com bom desempenho\", pense em atalhos e Direct Lake antes de cópias e importação.",
),

"AB-900": dict(
    semanas=[
        ("Serviços e segurança do Microsoft 365", "Objetos principais do Microsoft 365 (usuários, grupos, licenças, sites, equipes), princípios de Zero Trust, MFA, acesso condicional e os recursos de segurança do Microsoft 365.",
         "Num locatário de avaliação, crie usuários e grupos, atribua licenças e veja onde cada serviço é administrado."),
        ("Proteção de dados e o Copilot", "Como o Microsoft 365 Copilot acessa dados (só o que o usuário já pode ver), Microsoft Purview (rótulos de confidencialidade, DLP, retenção, auditoria), riscos de governança e excesso de compartilhamento no SharePoint.",
         "Procure sites e arquivos compartilhados com \"todos\" no seu ambiente de teste e corrija as permissões antes de imaginar o Copilot usando esses dados."),
        ("Administração do Copilot e de agentes", "Recursos do Microsoft 365 Copilot e de agentes, licenciamento e atribuição, configurações no centro de administração, controle de quem pode criar e usar agentes e monitoramento de uso.",
         "Percorra o centro de administração do Microsoft 365 nas áreas de Copilot e agentes e anote cada configuração e o efeito dela."),
        ("Revisão e simulados", "Proteção e governança de dados é a área de maior peso.",
         "Faça simulados e revise a relação entre permissões, rótulos e o que o Copilot pode mostrar."),
    ],
    confusoes=[
        ("O que o Copilot pode ver", "O Microsoft 365 Copilot respeita as permissões do usuário: ele só usa conteúdo que aquela pessoa já consegue abrir. O risco real é o excesso de compartilhamento, que faz o Copilot encontrar arquivos que deveriam estar restritos."),
        ("Rótulo de confidencialidade x permissão do SharePoint", "A permissão define quem acessa o site ou arquivo. O rótulo classifica e pode proteger o conteúdo com criptografia, que continua valendo mesmo se o arquivo for copiado para outro lugar."),
        ("Agente x Copilot", "O Copilot é o assistente geral do Microsoft 365. O agente é especializado num processo ou base de conhecimento e pode ser criado pela empresa, com controle do administrador sobre quem cria e quem usa."),
    ],
    vale="Vale a pena para administradores iniciantes do Microsoft 365, para profissionais de TI que vão implantar o Copilot na empresa e para quem cuida de governança de dados e precisa entender os riscos da IA no dia a dia. Não exige experiência e não expira. Para quem já administra o Microsoft 365 há anos, o ganho maior está nas certificações Associate da trilha.",
    compara=("AZ-900", "AB-900 ou AZ-900?", [
        "A AB-900 é sobre o Microsoft 365: usuários, licenças, proteção de dados e administração do Copilot e de agentes. A AZ-900 é sobre a nuvem Azure: infraestrutura, serviços, custos e governança.",
        "Se você trabalha com o ambiente de escritório da empresa (e-mail, Teams, SharePoint, Copilot), a AB-900 é mais útil.",
        "Se você trabalha com servidores, aplicações ou dados na nuvem, comece pela AZ-900.",
    ]),
    dica="Quando a questão falar de vazamento de dados pelo Copilot, a causa quase sempre está nas permissões e no compartilhamento, não no Copilot em si. Procure a alternativa que corrige o acesso ao conteúdo.",
),

}
