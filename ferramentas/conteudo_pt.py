# -*- coding: utf-8 -*-
"""
Conteúdo em português de cada certificação (escrito à mão).
Os pesos, duração, idiomas e datas vêm do Microsoft Learn (ver base_learn.json).
Ordem dos domínios = mesma ordem do guia de estudo oficial.

Formato:
CODIGO: dict(
  nome_pt, trilha, nivel, status ('ativa' | 'beta' | 'aposentando'), aposenta (AAAA-MM-DD ou None),
  resumo (1 frase), publico (quem deve fazer), prereq (texto ou None),
  antes [códigos], depois [códigos],
  dominios [ (nome, [tópicos...]) ]
)
"""

TRILHAS = {
    "azure":     ("Azure e infraestrutura", "☁️"),
    "dev":       ("Desenvolvimento e DevOps", "🧩"),
    "ia":        ("IA e agentes", "🤖"),
    "dados":     ("Dados e analytics", "📊"),
    "seguranca": ("Segurança", "🛡️"),
    "m365":      ("Microsoft 365", "💼"),
    "power":     ("Power Platform", "⚡"),
    "dynamics":  ("Dynamics 365", "🏢"),
    "negocios":  ("IA para negócios", "🚀"),
}

C = {}

# ============================ FUNDAMENTALS ============================
C["AZ-900"] = dict(
    nome_pt="Fundamentos do Azure", trilha="azure", nivel="Fundamentals", status="ativa", aposenta=None,
    resumo="A porta de entrada da nuvem Microsoft: conceitos de nuvem, serviços do Azure, custos e governança.",
    publico="Quem está começando em nuvem, inclusive profissionais de vendas, compras e gestão que precisam falar a língua do Azure. Não exige experiência técnica.",
    prereq=None, antes=[], depois=["AZ-104", "AI-901", "DP-900", "SC-900"],
    dominios=[
        ("Descrever conceitos de nuvem", ["Computação em nuvem", "Benefícios dos serviços de nuvem", "Tipos de serviço (IaaS, PaaS, SaaS)"]),
        ("Descrever a arquitetura e os serviços do Azure", ["Componentes de arquitetura (regiões, zonas, assinaturas)", "Computação, rede e armazenamento", "Identidade, acesso e segurança"]),
        ("Descrever o gerenciamento e a governança do Azure", ["Gerenciamento de custos", "Governança e conformidade (Policy, bloqueios)", "Ferramentas de implantação e monitoramento"]),
    ])
C["AI-901"] = dict(
    nome_pt="Fundamentos de IA no Azure", trilha="ia", nivel="Fundamentals", status="ativa", aposenta=None,
    resumo="Conceitos de IA e IA generativa e como criar soluções com o Microsoft Foundry. Substitui a antiga AI-900.",
    publico="Estudantes e profissionais técnicos ou de negócio que querem entender IA, agentes e os serviços de IA do Azure.",
    prereq=None, antes=[], depois=["AI-103", "AI-200", "AB-730"],
    dominios=[
        ("Identificar conceitos e capacidades de IA", ["Princípios de IA responsável", "Componentes e configurações de modelos", "Cargas de trabalho de IA"]),
        ("Implementar soluções de IA com o Microsoft Foundry", ["Apps e agentes de IA generativa", "Texto e fala", "Visão computacional e geração de imagens", "Extração de informações"]),
    ])
C["DP-900"] = dict(
    nome_pt="Fundamentos de dados do Azure", trilha="dados", nivel="Fundamentals", status="ativa", aposenta=None,
    resumo="Conceitos de dados relacionais, não relacionais e analytics, e os serviços de dados do Azure.",
    publico="Quem quer começar em dados: futuros analistas, engenheiros e administradores de banco de dados.",
    prereq=None, antes=[], depois=["PL-300", "DP-300", "DP-600", "DP-700"],
    dominios=[
        ("Descrever conceitos fundamentais de dados", ["Formas de representar dados", "Opções de armazenamento", "Cargas de trabalho e papéis em dados"]),
        ("Identificar considerações sobre dados relacionais no Azure", ["Conceitos relacionais", "Serviços relacionais do Azure"]),
        ("Descrever dados não relacionais no Azure", ["Armazenamento do Azure", "Azure Cosmos DB"]),
        ("Descrever uma carga de trabalho de analytics", ["Analytics em larga escala", "Analytics em tempo real", "Visualização de dados"]),
    ])
C["SC-900"] = dict(
    nome_pt="Fundamentos de segurança, conformidade e identidade", trilha="seguranca", nivel="Fundamentals", status="ativa", aposenta=None,
    resumo="Zero Trust, Microsoft Entra, Defender, Sentinel e Purview: a base de segurança da Microsoft.",
    publico="Quem quer entrar em segurança da informação ou precisa entender identidade, proteção e conformidade no ecossistema Microsoft.",
    prereq=None, antes=[], depois=["SC-200", "SC-300", "SC-401", "SC-500"],
    dominios=[
        ("Descrever conceitos de segurança, conformidade e identidade", ["Conceitos de segurança e conformidade", "Conceitos de identidade"]),
        ("Descrever as capacidades do Microsoft Entra", ["Tipos de identidade no Entra ID", "Autenticação", "Gerenciamento de acesso", "Proteção e governança de identidade"]),
        ("Descrever as soluções de segurança da Microsoft", ["Segurança de infraestrutura no Azure", "Gerenciamento de segurança", "Microsoft Sentinel", "Defender XDR"]),
        ("Descrever as soluções de conformidade da Microsoft", ["Portal de Confiança e privacidade", "Microsoft Purview: conformidade", "Proteção e ciclo de vida de dados", "Risco interno, eDiscovery e auditoria"]),
    ])
C["PL-900"] = dict(
    nome_pt="Fundamentos do Power Platform", trilha="power", nivel="Fundamentals", status="ativa", aposenta=None,
    resumo="Power Apps, Power Automate, Dataverse e agentes no Copilot Studio para resolver problemas de negócio.",
    publico="Profissionais de qualquer área que querem automatizar processos e criar apps com pouco ou nenhum código.",
    prereq=None, antes=[], depois=["AB-410", "PL-300", "AB-620"],
    dominios=[
        ("Descrever o valor de negócio do Power Platform", []),
        ("Gerenciar o ambiente do Power Platform", ["Microsoft Dataverse", "Administração e governança"]),
        ("Demonstrar as capacidades do Power Apps", ["Casos de uso", "Criação de apps básicos"]),
        ("Demonstrar as capacidades do Power Automate", ["Casos de uso", "Criação de fluxos básicos"]),
        ("Descrever agentes no Microsoft Copilot Studio", ["Criação de agentes", "Gerenciamento de agentes"]),
    ])
C["AB-900"] = dict(
    nome_pt="Fundamentos de administração do Copilot e agentes", trilha="m365", nivel="Fundamentals", status="ativa", aposenta=None,
    resumo="Serviços do Microsoft 365, proteção de dados e administração básica do Microsoft 365 Copilot e de agentes.",
    publico="Administradores iniciantes e profissionais de TI que vão implantar ou dar suporte ao Copilot na empresa.",
    prereq=None, antes=[], depois=["AB-650", "MD-102", "MS-700"],
    dominios=[
        ("Identificar recursos e objetos dos serviços do Microsoft 365", ["Objetos principais do Microsoft 365", "Princípios de segurança", "Recursos de segurança"]),
        ("Entender proteção e governança de dados no Microsoft 365 e no Copilot", ["Microsoft Purview", "Segurança de dados no Copilot", "Riscos de governança", "Excesso de compartilhamento no SharePoint"]),
        ("Executar tarefas básicas de administração do Copilot e de agentes", ["Recursos do Copilot e de agentes", "Administração do Copilot", "Administração de agentes"]),
    ])

# ============================ AZURE E INFRAESTRUTURA ============================
C["AZ-104"] = dict(
    nome_pt="Administrador do Azure", trilha="azure", nivel="Associate", status="ativa", aposenta=None,
    resumo="Implementar, gerenciar e monitorar identidade, governança, armazenamento, computação e redes no Azure.",
    publico="Administradores de nuvem e de infraestrutura que operam ambientes Azure no dia a dia.",
    prereq=None, antes=["AZ-900"], depois=["AZ-305", "AZ-700", "AZ-400"],
    dominios=[
        ("Gerenciar identidades e governança do Azure", ["Usuários e grupos do Entra", "Acesso a recursos (RBAC)", "Assinaturas e governança"]),
        ("Implementar e gerenciar armazenamento", ["Acesso ao armazenamento", "Contas de armazenamento", "Azure Files e Blob Storage"]),
        ("Implantar e gerenciar recursos de computação", ["ARM templates e Bicep", "Máquinas virtuais", "Contêineres", "App Service"]),
        ("Implementar e gerenciar redes virtuais", ["Redes virtuais", "Acesso seguro às redes", "Resolução de nomes e balanceamento"]),
        ("Monitorar e manter recursos do Azure", ["Monitoramento", "Backup e recuperação"]),
    ])
C["AZ-700"] = dict(
    nome_pt="Engenheiro de redes do Azure", trilha="azure", nivel="Associate", status="ativa", aposenta=None,
    resumo="Projetar e implementar redes no Azure: conectividade híbrida, roteamento, entrega de aplicações e segurança de rede.",
    publico="Engenheiros de rede que levam a experiência on-premises para a nuvem.",
    prereq=None, antes=["AZ-104"], depois=["AZ-305"],
    dominios=[
        ("Projetar e implementar a infraestrutura de rede principal", ["Endereçamento IP", "Resolução de nomes", "Conectividade e roteamento entre VNets"]),
        ("Projetar, implementar e gerenciar serviços de conectividade", ["VPN site a site e ponto a site", "ExpressRoute", "Virtual WAN"]),
        ("Projetar e implementar serviços de entrega de aplicações", ["Load Balancer e Traffic Manager", "Application Gateway", "Front Door"]),
        ("Projetar e implementar acesso privado a serviços do Azure", ["Private Link e endpoints privados", "Service endpoints"]),
        ("Projetar e implementar segurança de rede", ["Grupos de segurança de rede (NSG)", "Azure Firewall", "Web Application Firewall"]),
    ])
C["AZ-802"] = dict(
    nome_pt="Administrador do Windows Server", trilha="azure", nivel="Associate", status="ativa", aposenta=None,
    resumo="Administrar Windows Server em ambientes locais e híbridos: AD DS, VMs, armazenamento, rede e segurança. Substitui AZ-800 e AZ-801.",
    publico="Administradores de servidores Windows que gerenciam ambientes locais integrados ao Azure.",
    prereq=None, antes=["AZ-900"], depois=["AZ-104"],
    dominios=[
        ("Implantar e gerenciar o AD DS", ["Ambientes multisite, multidomínio e multifloresta", "Entidades de segurança", "Políticas de grupo"]),
        ("Gerenciar instâncias e cargas do Windows Server em ambiente híbrido", ["Gerenciamento remoto", "Serviços do Azure para servidores híbridos", "Hyper-V e VMs no Azure"]),
        ("Gerenciar máquinas virtuais", []),
        ("Implementar redes locais e híbridas", ["Resolução de nomes", "Endereçamento IP"]),
        ("Gerenciar armazenamento e serviços de arquivos", ["Azure Files", "Compartilhamentos de arquivos", "Armazenamento do Windows Server"]),
        ("Proteger a infraestrutura do Windows Server", ["Sistema operacional", "AD DS"]),
        ("Monitorar e solucionar problemas", ["Ferramentas do Windows Server e do Azure", "Problemas do Windows Server", "Active Directory"]),
    ])
C["AZ-140"] = dict(
    nome_pt="Azure Virtual Desktop", trilha="azure", nivel="Specialty", status="ativa", aposenta=None,
    resumo="Planejar, implantar e operar desktops e aplicativos virtuais com o Azure Virtual Desktop.",
    publico="Administradores que entregam áreas de trabalho virtuais e apps remotos para usuários.",
    prereq=None, antes=["AZ-104"], depois=[],
    dominios=[
        ("Planejar e implementar a infraestrutura do Azure Virtual Desktop", ["Rede", "Armazenamento de dados do usuário", "Pools de hosts e hosts de sessão"]),
        ("Planejar e implementar identidade e segurança", ["Integração de identidade", "Segurança"]),
        ("Planejar e implementar ambientes de usuário e apps", ["FSLogix", "Experiência do usuário e configurações de cliente", "Instalação de apps"]),
        ("Monitorar e manter a infraestrutura", ["Monitoramento dos serviços", "Atualizações, backup e recuperação"]),
    ])
C["AZ-120"] = dict(
    nome_pt="Azure para cargas de trabalho SAP", trilha="azure", nivel="Specialty", status="ativa", aposenta=None,
    resumo="Migrar, projetar e manter soluções SAP no Azure, incluindo RISE with SAP.",
    publico="Arquitetos e engenheiros com experiência em SAP (HANA, NetWeaver) que levam esses ambientes para o Azure.",
    prereq=None, antes=["AZ-104"], depois=["AZ-305"],
    dominios=[
        ("Migrar cargas de trabalho SAP para o Azure", ["Requisitos da infraestrutura de destino", "Ambiente Azure para SAP", "Integração com RISE with SAP"]),
        ("Projetar e implementar a infraestrutura para SAP no Azure", ["Computação", "Rede", "Armazenamento"]),
        ("Projetar alta disponibilidade e recuperação de desastres", ["Alta disponibilidade", "Recuperação de desastres"]),
        ("Manter cargas de trabalho SAP no Azure", ["Desempenho e custos", "Monitoramento e manutenção"]),
    ])
C["AZ-305"] = dict(
    nome_pt="Arquiteto de soluções do Azure", trilha="azure", nivel="Expert", status="ativa", aposenta=None,
    resumo="Projetar soluções completas no Azure: identidade, governança, dados, continuidade de negócios e infraestrutura.",
    publico="Arquitetos de nuvem com experiência sólida em administração do Azure que tomam decisões de design.",
    prereq="Ter a certificação Azure Administrator Associate (AZ-104).", antes=["AZ-104"], depois=[],
    dominios=[
        ("Projetar soluções de identidade, governança e monitoramento", ["Log e monitoramento", "Autenticação e autorização", "Governança"]),
        ("Projetar soluções de armazenamento de dados", ["Dados relacionais e não relacionais", "Integração de dados"]),
        ("Projetar soluções de continuidade de negócios", ["Backup e recuperação de desastres", "Alta disponibilidade"]),
        ("Projetar soluções de infraestrutura", ["Computação", "Arquitetura de aplicações", "Migrações", "Rede"]),
    ])

# ============================ DESENVOLVIMENTO E DEVOPS ============================
C["AI-200"] = dict(
    nome_pt="Desenvolvedor de nuvem e IA do Azure", trilha="dev", nivel="Associate", status="ativa", aposenta=None,
    resumo="Desenvolver soluções na nuvem com contêineres, bancos de dados do Azure, mensageria e Functions, com foco em IA.",
    publico="Desenvolvedores que constroem e mantêm aplicações modernas e com IA no Azure.",
    prereq=None, antes=["AZ-900", "AI-901"], depois=["AZ-400", "AZ-401", "AI-103"],
    dominios=[
        ("Desenvolver soluções em contêineres no Azure", ["Hospedagem de aplicações em contêiner", "Orquestração de contêineres"]),
        ("Desenvolver soluções de IA com serviços de dados do Azure", ["Cosmos DB for NoSQL", "Azure Database for PostgreSQL", "Azure Managed Redis"]),
        ("Conectar e consumir serviços do Azure", ["Soluções orientadas a eventos e mensagens", "Azure Functions"]),
        ("Proteger, monitorar e solucionar problemas", ["Soluções seguras", "Monitoramento e troubleshooting"]),
    ])
C["AZ-400"] = dict(
    nome_pt="Engenheiro de DevOps", trilha="dev", nivel="Expert", status="aposentando", aposenta="2027-02-01",
    resumo="Processos, controle de código, pipelines de build e release, segurança e monitoramento com Azure DevOps e GitHub.",
    publico="Desenvolvedores ou administradores de infraestrutura que unem pessoas, processos e ferramentas para entrega contínua.",
    prereq="Ter Azure Administrator Associate (AZ-104) ou Azure Developer Associate.", antes=["AZ-104", "AI-200"], depois=["AZ-401"],
    dominios=[
        ("Projetar e implementar processos e comunicação", ["Rastreabilidade e fluxo de trabalho", "Métricas de DevOps", "Colaboração"]),
        ("Projetar e implementar a estratégia de controle de código", ["Estratégias de branch", "Repositórios"]),
        ("Projetar e implementar pipelines de build e release", ["Gerenciamento de pacotes", "Estratégia de testes", "Pipelines e implantações"]),
        ("Desenvolver o plano de segurança e conformidade", ["Autenticação e autorização", "Segredos em automação", "Varredura de segurança"]),
        ("Implementar a estratégia de instrumentação", ["Monitoramento do ambiente DevOps", "Análise de métricas"]),
    ])
C["AZ-401"] = dict(
    nome_pt="Engenheiro de DevOps com IA agêntica", trilha="dev", nivel="Expert", status="beta", aposenta=None,
    resumo="A nova geração do DevOps Expert: Azure DevOps, GitHub Actions e agentes de IA no ciclo de entrega. Chega enquanto a AZ-400 se aposenta.",
    publico="Engenheiros de DevOps experientes que usam ferramentas de IA da Microsoft e do GitHub, com domínio de YAML, KQL e Bicep.",
    prereq=None, antes=["AZ-400", "AZ-104", "AI-200"], depois=[],
    dominios=[
        ("Projetar e implementar processos e comunicação", ["Rastreabilidade e fluxo de trabalho", "Métricas de sucesso", "Colaboração"]),
        ("Projetar e implementar a estratégia de controle de código", ["Branches no Azure DevOps e GitHub", "Repositórios"]),
        ("Projetar e implementar pipelines de build e release", ["Pacotes", "Testes em pipelines e GitHub Actions", "Pipelines e implantações"]),
        ("Projetar e implementar o plano de segurança e conformidade", ["Autenticação e autorização", "Informações sensíveis em automação", "Varredura automatizada"]),
        ("Implementar a estratégia de instrumentação", ["Monitoramento das plataformas", "Monitoramento com agentes de IA", "Análise de métricas com agentes de IA"]),
    ])

# ============================ IA E AGENTES ============================
C["AI-103"] = dict(
    nome_pt="Desenvolvedor de apps e agentes de IA do Azure", trilha="ia", nivel="Associate", status="ativa", aposenta=None,
    resumo="Construir apps de IA generativa e agentes com o Microsoft Foundry, além de visão, texto, fala e extração de informações.",
    publico="Desenvolvedores e engenheiros de IA que criam soluções com modelos e agentes no Azure.",
    prereq=None, antes=["AI-901"], depois=["AI-500", "AI-300"],
    dominios=[
        ("Planejar e gerenciar uma solução de IA no Azure", ["Escolha de serviços do Foundry", "Configuração no Foundry", "Monitoramento, segurança e IA responsável"]),
        ("Implementar soluções generativas e agênticas", ["Aplicações generativas", "Agentes no Foundry", "Otimização e operação"]),
        ("Implementar soluções de visão computacional", ["Geração de imagem e vídeo", "Compreensão multimodal"]),
        ("Implementar soluções de análise de texto", ["Análise de texto com modelos de linguagem", "Soluções de fala"]),
        ("Implementar soluções de extração de informações", ["Pipelines de recuperação e grounding", "Extração de documentos"]),
    ])
C["AI-300"] = dict(
    nome_pt="Engenheiro de operações de machine learning (MLOps)", trilha="ia", nivel="Associate", status="ativa", aposenta=None,
    resumo="Operacionalizar machine learning e IA generativa: MLOps, GenAIOps, avaliação, observabilidade e otimização.",
    publico="Cientistas de dados e engenheiros de ML que colocam modelos e soluções generativas em produção.",
    prereq=None, antes=["AI-901", "AI-103"], depois=["AI-500"],
    dominios=[
        ("Projetar e implementar a infraestrutura de MLOps", ["Workspace de Machine Learning", "Ativos do workspace", "Infraestrutura como código"]),
        ("Implementar o ciclo de vida de modelos de ML", ["Treinamento", "Registro e versionamento", "Implantação e monitoramento"]),
        ("Projetar e implementar a infraestrutura de GenAIOps", ["Ambientes do Foundry", "Modelos de base em produção", "Versionamento de prompts"]),
        ("Garantir qualidade e observabilidade de IA generativa", ["Avaliação de apps e agentes", "Observabilidade"]),
        ("Otimizar sistemas e modelos de IA generativa", ["Desempenho de RAG", "Fine-tuning e customização"]),
    ])
C["AI-500"] = dict(
    nome_pt="Especialista em soluções de IA multiagente", trilha="ia", nivel="Expert", status="ativa", aposenta=None,
    resumo="Arquitetar, desenvolver, avaliar e governar soluções com vários agentes de IA no Azure.",
    publico="Profissionais experientes que projetam sistemas agênticos escaláveis e prontos para produção.",
    prereq="Ter a certificação Azure AI Apps and Agents Developer Associate (AI-103).", antes=["AI-103"], depois=[],
    dominios=[
        ("Arquitetar soluções multiagente", ["Arquitetura lógica", "Componentes de tecnologia"]),
        ("Desenvolver soluções multiagente no Azure", ["Engenharia de prompt avançada", "Memória e contexto", "Ferramentas e orquestração"]),
        ("Avaliar, otimizar e monitorar", ["Estratégias de avaliação", "Otimização de prompts e modelos", "Observabilidade"]),
        ("Proteger, governar e implantar", ["Segurança", "Guardrails", "Implantação no Azure"]),
    ])

# ============================ DADOS E ANALYTICS ============================
C["PL-300"] = dict(
    nome_pt="Analista de dados do Power BI", trilha="dados", nivel="Associate", status="ativa", aposenta=None,
    resumo="Preparar, modelar, visualizar e proteger dados com o Power BI, incluindo DAX.",
    publico="Analistas de dados e de negócio que constroem relatórios e dashboards.",
    prereq=None, antes=["DP-900", "PL-900"], depois=["DP-600"],
    dominios=[
        ("Preparar os dados", ["Conexão a fontes", "Perfil e limpeza", "Transformação e carga"]),
        ("Modelar os dados", ["Modelo de dados", "Cálculos com DAX", "Desempenho do modelo"]),
        ("Visualizar e analisar os dados", ["Relatórios", "Usabilidade e storytelling", "Padrões e tendências"]),
        ("Gerenciar e proteger o Power BI", ["Workspaces e itens", "Segurança e governança"]),
    ])
C["DP-300"] = dict(
    nome_pt="Administrador de banco de dados do Azure", trilha="dados", nivel="Associate", status="ativa", aposenta=None,
    resumo="Administrar SQL Server e Azure SQL: implantação, segurança, desempenho, automação e alta disponibilidade.",
    publico="DBAs e administradores de dados que gerenciam bancos SQL na nuvem e em ambientes híbridos.",
    prereq=None, antes=["DP-900"], depois=["DP-800"],
    dominios=[
        ("Planejar e implementar recursos da plataforma de dados", ["Soluções Azure SQL", "Escala e desempenho", "Estratégia de migração"]),
        ("Implementar um ambiente seguro", ["Autenticação e autorização", "Dados em repouso e em trânsito", "Dados sensíveis"]),
        ("Monitorar, configurar e otimizar recursos", ["Atividade e desempenho", "Desempenho de consultas", "Configuração ideal"]),
        ("Configurar e gerenciar a automação de tarefas", ["SQL Server Agent", "Implantação automatizada", "Tarefas no Azure"]),
        ("Planejar alta disponibilidade e recuperação de desastres", ["Estratégia HA/DR", "Backup e restauração", "Configuração HA/DR"]),
    ])
C["DP-420"] = dict(
    nome_pt="Desenvolvedor de IA com Azure Cosmos DB", trilha="dados", nivel="Specialty", status="ativa", aposenta=None,
    resumo="Modelar, desenvolver, proteger e otimizar soluções no Cosmos DB, incluindo recursos de IA e analytics.",
    publico="Desenvolvedores que criam aplicações nativas de nuvem e de IA sobre o Azure Cosmos DB.",
    prereq=None, antes=["DP-900", "AI-200"], depois=[],
    dominios=[
        ("Projetar e desenvolver soluções de banco de dados", ["Modelos de recursos e SDKs", "Operações", "Modelagem e particionamento", "Change feed"]),
        ("Proteger, otimizar e implantar", ["Segurança", "Disponibilidade e recuperação", "Desempenho", "Gestão de frota"]),
        ("Implementar recursos de IA e analytics", []),
    ])
C["DP-600"] = dict(
    nome_pt="Engenheiro de analytics do Fabric", trilha="dados", nivel="Associate", status="ativa", aposenta=None,
    resumo="Construir soluções de analytics no Microsoft Fabric: preparação de dados e modelos semânticos em escala.",
    publico="Profissionais de BI e analytics que trabalham com lakehouses, warehouses e modelos semânticos.",
    prereq=None, antes=["PL-300", "DP-900"], depois=["DP-700"],
    dominios=[
        ("Manter uma solução de analytics", ["Segurança e governança", "Ciclo de vida de desenvolvimento"]),
        ("Preparar dados", ["Obter dados", "Transformar dados", "Consultar e analisar"]),
        ("Implementar e gerenciar modelos semânticos", ["Projeto e construção", "Otimização em escala"]),
    ])
C["DP-700"] = dict(
    nome_pt="Engenheiro de dados do Fabric", trilha="dados", nivel="Associate", status="ativa", aposenta=None,
    resumo="Ingestão, transformação, orquestração e monitoramento de dados em lote e streaming no Microsoft Fabric.",
    publico="Engenheiros de dados que constroem pipelines no Fabric.",
    prereq=None, antes=["DP-900"], depois=["DP-600", "DP-750"],
    dominios=[
        ("Implementar e gerenciar uma solução de analytics", ["Workspaces do Fabric", "Ciclo de vida", "Segurança e governança", "Orquestração"]),
        ("Ingerir e transformar dados", ["Padrões de carga", "Dados em lote", "Dados em streaming"]),
        ("Monitorar e otimizar", ["Monitoramento de itens", "Erros", "Desempenho"]),
    ])
C["DP-750"] = dict(
    nome_pt="Engenheiro de dados do Azure Databricks", trilha="dados", nivel="Associate", status="ativa", aposenta=None,
    resumo="Configurar o Databricks, governar o Unity Catalog e construir pipelines de dados.",
    publico="Engenheiros de dados que trabalham com Azure Databricks e Lakeflow.",
    prereq=None, antes=["DP-900"], depois=["DP-700"],
    dominios=[
        ("Configurar o ambiente do Azure Databricks", ["Computação no workspace", "Objetos no Unity Catalog"]),
        ("Proteger e governar objetos do Unity Catalog", ["Segurança", "Governança"]),
        ("Preparar e processar dados", ["Modelagem", "Ingestão", "Limpeza, transformação e qualidade"]),
        ("Implantar e manter pipelines e cargas", ["Pipelines de dados", "Lakeflow Jobs", "Ciclo de desenvolvimento e otimização"]),
    ])
C["DP-800"] = dict(
    nome_pt="Desenvolvedor de IA para SQL", trilha="dados", nivel="Associate", status="ativa", aposenta=None,
    resumo="Desenvolver soluções de banco de dados com T-SQL avançado, CI/CD e recursos de IA como embeddings, busca inteligente e RAG.",
    publico="Desenvolvedores SQL que levam IA para dentro do banco de dados.",
    prereq=None, antes=["DP-300", "DP-900"], depois=[],
    dominios=[
        ("Projetar e desenvolver soluções de banco de dados", ["Objetos de banco", "Programabilidade", "T-SQL avançado", "Ferramentas com IA"]),
        ("Proteger, otimizar e implantar", ["Segurança e conformidade", "Desempenho", "CI/CD com SQL Database Projects"]),
        ("Implementar IA em soluções de banco de dados", ["Modelos e embeddings", "Busca inteligente", "RAG"]),
    ])

# ============================ SEGURANÇA ============================
C["SC-200"] = dict(
    nome_pt="Analista de operações de segurança", trilha="seguranca", nivel="Associate", status="ativa", aposenta=None,
    resumo="Detectar, investigar e responder a ameaças com Microsoft Defender XDR e Microsoft Sentinel.",
    publico="Analistas de SOC e profissionais de resposta a incidentes.",
    prereq=None, antes=["SC-900"], depois=["SC-100"],
    dominios=[
        ("Gerenciar o ambiente de operações de segurança", ["Automação no Defender XDR e Sentinel", "SIEM do Sentinel", "Ingestão de dados", "Detecções"]),
        ("Responder a incidentes de segurança", ["Alertas no Defender XDR", "Defender for Endpoint", "Investigação no Microsoft 365"]),
        ("Realizar caça a ameaças", ["Defender XDR", "Plataforma Microsoft Sentinel"]),
    ])
C["SC-300"] = dict(
    nome_pt="Administrador de identidade e acesso", trilha="seguranca", nivel="Associate", status="ativa", aposenta=None,
    resumo="Identidades, autenticação, acesso condicional, identidades de workload e governança com o Microsoft Entra.",
    publico="Administradores de identidade que protegem usuários, apps e acessos.",
    prereq=None, antes=["SC-900"], depois=["SC-100", "MS-102"],
    dominios=[
        ("Implementar e gerenciar identidades de usuários", ["Locatário do Entra", "Identidades", "Usuários externos", "Identidade híbrida"]),
        ("Implementar autenticação e gerenciamento de acesso", ["Autenticação", "Acesso condicional", "ID Protection", "Global Secure Access"]),
        ("Planejar e implementar identidades de workload", ["Identidades de apps e workloads", "Aplicações empresariais", "Registros de apps"]),
        ("Planejar e automatizar a governança de identidade", ["Gerenciamento de direitos", "Revisões de acesso", "Acesso privilegiado", "Monitoramento"]),
    ])
C["SC-401"] = dict(
    nome_pt="Administrador de segurança da informação", trilha="seguranca", nivel="Associate", status="ativa", aposenta=None,
    resumo="Classificação, rótulos de confidencialidade, DLP, retenção e gestão de riscos com o Microsoft Purview.",
    publico="Administradores de proteção de dados e conformidade.",
    prereq=None, antes=["SC-900"], depois=["SC-100", "MS-102"],
    dominios=[
        ("Implementar proteção de informações", ["Classificação de dados", "Rótulos de confidencialidade"]),
        ("Implementar prevenção contra perda de dados e retenção", []),
        ("Gerenciar riscos, alertas e atividades", []),
    ])
C["SC-500"] = dict(
    nome_pt="Engenheiro de segurança de nuvem e IA", trilha="seguranca", nivel="Associate", status="ativa", aposenta=None,
    resumo="Proteger identidade, dados, rede, computação e soluções de IA no Azure.",
    publico="Engenheiros de segurança que protegem cargas de trabalho na nuvem e soluções de IA.",
    prereq=None, antes=["SC-900", "AZ-104"], depois=["SC-100"],
    dominios=[
        ("Gerenciar identidade, acesso e governança", ["Entra ID", "Key Vault", "Governança e conformidade"]),
        ("Proteger armazenamento, bancos de dados e rede", ["Contas de armazenamento", "Bancos de dados", "Serviços de rede"]),
        ("Proteger computação", ["Segurança para IA", "Servidores e VMs", "Plataformas de aplicação"]),
        ("Gerenciar e monitorar a postura de segurança", ["Defender for Cloud", "Microsoft Sentinel", "Security Copilot"]),
    ])
C["SC-100"] = dict(
    nome_pt="Arquiteto de cibersegurança", trilha="seguranca", nivel="Expert", status="ativa", aposenta=None,
    resumo="Projetar estratégias de segurança: Zero Trust, operações, identidade, infraestrutura, aplicações e dados.",
    publico="Arquitetos de segurança experientes que definem a estratégia de proteção da organização.",
    prereq="Ter uma destas: Identity and Access Administrator (SC-300), Security Operations Analyst (SC-200) ou Cloud and AI Security Engineer (SC-500).",
    antes=["SC-200", "SC-300", "SC-500"], depois=[],
    dominios=[
        ("Projetar soluções alinhadas às boas práticas de segurança", ["Resiliência contra ransomware"]),
        ("Projetar operações de segurança, identidade e conformidade", ["Operações de segurança", "Identidade e acesso", "Acesso privilegiado", "Conformidade regulatória"]),
        ("Projetar segurança de infraestrutura", ["Postura em ambientes híbridos e multinuvem", "Endpoints", "SaaS, PaaS e IaaS", "Segurança de rede e SSE"]),
        ("Projetar segurança de aplicações e dados", ["Microsoft 365", "Aplicações", "Dados da organização"]),
    ])

# ============================ MICROSOFT 365 ============================
C["MD-102"] = dict(
    nome_pt="Administrador de endpoints", trilha="m365", nivel="Associate", status="ativa", aposenta=None,
    resumo="Implantar, configurar, proteger e monitorar dispositivos e aplicativos com Microsoft Intune.",
    publico="Administradores de desktop e dispositivos móveis em empresas que usam Microsoft 365.",
    prereq=None, antes=["AB-900"], depois=["MS-102"],
    dominios=[
        ("Preparar a infraestrutura para dispositivos", ["Dispositivos no Entra ID", "Registro no Intune", "Identidade e conformidade"]),
        ("Gerenciar e manter dispositivos", ["Implantação do Windows", "Perfis de configuração", "Intune Suite", "Ações remotas"]),
        ("Proteger dispositivos", ["Segurança de endpoints", "Atualizações"]),
        ("Gerenciar e proteger aplicativos", ["Implantação de apps", "Proteção e configuração de apps"]),
        ("Otimizar operações com automação, monitoramento e relatórios", ["Automação", "Saúde dos dispositivos"]),
    ])
C["MS-700"] = dict(
    nome_pt="Administrador do Teams", trilha="m365", nivel="Associate", status="ativa", aposenta=None,
    resumo="Configurar, governar e operar o Microsoft Teams: equipes, canais, apps, reuniões e chamadas.",
    publico="Administradores de colaboração responsáveis pelo Teams na organização.",
    prereq=None, antes=["AB-900"], depois=["MS-721", "MS-102"],
    dominios=[
        ("Configurar e gerenciar o ambiente do Teams", ["Rede", "Segurança e conformidade", "Governança", "Colaboração externa"]),
        ("Gerenciar equipes, canais, chats e apps", ["Equipes", "Canais e chats", "Apps"]),
        ("Gerenciar reuniões e chamadas", ["Reuniões e eventos", "Números e Teams Phone"]),
        ("Monitorar, relatar e solucionar problemas", ["Relatórios", "Áudio, vídeo e cliente"]),
    ])
C["MS-721"] = dict(
    nome_pt="Engenheiro de sistemas de comunicação e colaboração", trilha="m365", nivel="Associate", status="ativa", aposenta=None,
    resumo="Planejar e operar Teams Phone, reuniões, webinars, town halls e dispositivos Teams Rooms.",
    publico="Engenheiros de voz e colaboração que implantam telefonia e salas de reunião com Teams.",
    prereq=None, antes=["MS-700"], depois=[],
    dominios=[
        ("Planejar e projetar sistemas de comunicação", ["Reuniões", "Teams Phone e PSTN", "Dispositivos certificados", "Rede para o Teams"]),
        ("Configurar reuniões, webinars e town halls", ["Reuniões", "Audioconferência", "Webinars e town halls"]),
        ("Configurar e gerenciar o Teams Phone", []),
        ("Configurar Teams Rooms e dispositivos", ["Manutenção", "Dispositivos Android", "Teams Rooms no Windows"]),
    ])
C["AB-650"] = dict(
    nome_pt="Administrador de Microsoft 365 e serviços de IA", trilha="m365", nivel="Associate", status="ativa", aposenta=None,
    resumo="Administrar locatários do Microsoft 365, governança, segurança e serviços de IA como Copilot e Agent 365.",
    publico="Administradores de Microsoft 365 que também cuidam da adoção e da governança de IA.",
    prereq=None, antes=["AB-900"], depois=[],
    dominios=[
        ("Configurar e gerenciar locatários e cargas do Microsoft 365", ["Locatário", "Cargas de trabalho"]),
        ("Governar e proteger locatários e cargas", ["Identidades no Entra", "Autenticação e acesso", "Proteção com Purview"]),
        ("Gerenciar e proteger serviços de IA no Microsoft 365", ["Microsoft 365 Copilot", "Agentes e Agent 365", "Monitoramento de IA"]),
    ])
C["MS-102"] = dict(
    nome_pt="Administrador do Microsoft 365", trilha="m365", nivel="Expert", status="aposentando", aposenta="2026-11-30",
    resumo="Locatário do Microsoft 365, identidade com Entra, segurança com Defender XDR e conformidade com Purview.",
    publico="Administradores experientes que gerenciam todo o ambiente Microsoft 365.",
    prereq="Ter uma destas: MD-102, MS-700, SC-300 ou SC-401.", antes=["MD-102", "MS-700", "SC-300", "SC-401"], depois=["AB-650"],
    dominios=[
        ("Implantar e gerenciar um locatário do Microsoft 365", ["Locatário", "Usuários e grupos", "Funções"]),
        ("Implementar identidade e acesso com o Microsoft Entra", ["Sincronização de identidade", "Autenticação", "Acesso seguro"]),
        ("Gerenciar segurança e ameaças com o Defender XDR", ["Relatórios e alertas", "Defender for Office 365", "Defender for Endpoint"]),
        ("Gerenciar conformidade com o Microsoft Purview", ["Proteção e ciclo de vida de dados", "DLP"]),
    ])

# ============================ POWER PLATFORM ============================
C["AB-410"] = dict(
    nome_pt="Construtor de aplicações inteligentes", trilha="power", nivel="Associate", status="ativa", aposenta=None,
    resumo="Criar apps model-driven e canvas, fluxos e prompts de IA no Power Platform.",
    publico="Consultores e makers que entregam soluções de negócio com Power Apps e Power Automate.",
    prereq=None, antes=["PL-900"], depois=["AB-400", "AB-620"],
    dominios=[
        ("Criar a base para aplicações inteligentes", ["Design com ferramentas de IA", "Modelos de dados"]),
        ("Criar aplicações inteligentes", ["Apps model-driven", "Apps canvas"]),
        ("Construir lógica de negócio e automação", ["Fluxos de nuvem", "Prompts e modelos no AI Hub", "Regras de negócio"]),
    ])
C["AB-400"] = dict(
    nome_pt="Desenvolvedor do Power Platform", trilha="power", nivel="Associate", status="ativa", aposenta=None,
    resumo="Estender o Power Platform com código: PCF, code apps, plug-ins do Dataverse, APIs e integrações. Substitui a PL-400.",
    publico="Desenvolvedores que estendem o Power Platform além do low-code.",
    prereq=None, antes=["AB-410", "PL-900"], depois=["AB-100"],
    dominios=[
        ("Construir soluções do Power Platform", ["Arquitetura técnica", "Componentes", "ALM"]),
        ("Estender a experiência do usuário", ["Scripts em apps model-driven", "Componentes PCF", "Power Apps code apps"]),
        ("Estender o Power Platform", ["Plug-ins do Dataverse", "APIs da plataforma", "Azure Functions", "Fluxos e workflows"]),
        ("Desenvolver integrações", ["Eventos do Dataverse", "Sincronização de dados", "Conectores personalizados"]),
    ])
C["AB-620"] = dict(
    nome_pt="Construtor de agentes de IA", trilha="power", nivel="Associate", status="ativa", aposenta=None,
    resumo="Planejar, construir, integrar, testar e gerenciar agentes no Microsoft Copilot Studio.",
    publico="Makers e desenvolvedores que criam agentes de IA para processos de negócio.",
    prereq=None, antes=["PL-900", "AI-901"], depois=["AB-100"],
    dominios=[
        ("Planejar e configurar soluções de agentes", ["Planejamento", "Workflows", "Habilidades", "Identidade e comportamento do agente"]),
        ("Integrar e estender agentes no Copilot Studio", ["Ferramentas e dados corporativos", "Colaboração multiagente"]),
        ("Testar e gerenciar agentes", ["Avaliação de desempenho", "ALM de agentes"]),
    ])

# ============================ DYNAMICS 365 ============================
C["MB-800"] = dict(
    nome_pt="Consultor funcional do Business Central", trilha="dynamics", nivel="Associate", status="ativa", aposenta=None,
    resumo="Configurar e operar o Dynamics 365 Business Central: empresa, finanças, vendas e compras.",
    publico="Consultores e usuários-chave que implantam o ERP Business Central em pequenas e médias empresas.",
    prereq=None, antes=[], depois=["MB-820"],
    dominios=[
        ("Configurar o Business Central", ["Empresa", "Segurança", "Funcionalidades principais", "Dimensões"]),
        ("Configurar finanças", ["Gestão financeira", "Plano de contas", "Grupos de lançamento", "Diários e bancos"]),
        ("Configurar vendas e compras", ["Estoque", "Dados mestres", "Preços e descontos"]),
        ("Executar operações", ["Tarefas básicas", "Compras", "Vendas", "Documentos financeiros"]),
    ])
C["MB-820"] = dict(
    nome_pt="Desenvolvedor do Business Central", trilha="dynamics", nivel="Associate", status="ativa", aposenta=None,
    resumo="Desenvolver extensões em AL para o Business Central, com testes, telemetria, APIs e recursos de Copilot.",
    publico="Desenvolvedores que customizam e integram o Business Central.",
    prereq=None, antes=["MB-800"], depois=[],
    dominios=[
        ("Projetar soluções do Business Central", ["Arquitetura", "Apps"]),
        ("Instalar, desenvolver e implantar", ["Ambiente de desenvolvimento", "Extensões"]),
        ("Desenvolver objetos com AL", ["Tabelas e páginas", "Relatórios", "Codeunits", "Permissões"]),
        ("Desenvolver experiência e lógica com AL", ["Interface e onboarding", "Padrões de desenvolvimento"]),
        ("Testar e monitorar código AL", ["Testes", "Telemetria"]),
        ("Integrar com outras aplicações", ["Serviços REST", "APIs em AL", "Recursos de Copilot"]),
    ])
C["MB-230"] = dict(
    nome_pt="Consultor funcional de Atendimento ao Cliente", trilha="dynamics", nivel="Associate", status="ativa", aposenta=None,
    resumo="Configurar casos, base de conhecimento, roteamento e Copilot no Dynamics 365 Customer Service.",
    publico="Consultores que implantam soluções de atendimento ao cliente.",
    prereq=None, antes=[], depois=["AB-250"],
    dominios=[
        ("Gerenciar casos no Customer Service", ["Componentes fundamentais", "Base de conhecimento", "Colaboração", "Agentes e Copilot"]),
        ("Configurar a experiência do representante e o roteamento", ["Roteamento", "Ferramentas de produtividade", "Copilot Service workspace"]),
        ("Estender o Customer Service", ["Modelo de dados e interface", "Feedback com Customer Voice"]),
    ])
C["MB-310"] = dict(
    nome_pt="Consultor funcional de Finanças", trilha="dynamics", nivel="Associate", status="ativa", aposenta=None,
    resumo="Implementar gestão financeira, contas a receber e a pagar, orçamento e ativos fixos no Dynamics 365 Finance.",
    publico="Consultores financeiros que implantam o Dynamics 365 Finance.",
    prereq=None, antes=[], depois=["AB-100"],
    dominios=[
        ("Implementar a gestão financeira", ["Plano de contas", "Razões e moedas", "Diários", "Caixa e bancos"]),
        ("Implementar contas a receber, crédito, cobrança e assinaturas", ["Contas a receber", "Crédito e cobrança", "Faturamento de assinaturas"]),
        ("Implementar contas a pagar e despesas", ["Contas a pagar", "Gestão de despesas"]),
        ("Gerenciar orçamento", ["Orçamento básico", "Controle orçamentário"]),
        ("Gerenciar ativos fixos", ["Ativos fixos", "Transações de ativos"]),
    ])
C["MB-330"] = dict(
    nome_pt="Consultor funcional de Supply Chain Management", trilha="dynamics", nivel="Associate", status="aposentando", aposenta="2027-02-01",
    resumo="Produtos, estoque, compras, armazém, transporte e planejamento mestre no Dynamics 365 Supply Chain Management.",
    publico="Consultores de cadeia de suprimentos que implantam o Dynamics 365 SCM.",
    prereq=None, antes=[], depois=["AB-330"],
    dominios=[
        ("Implementar o gerenciamento de informações de produtos", ["Produtos", "Pré-requisitos", "Preço e custo de estoque"]),
        ("Implementar a gestão de estoque e ativos", ["Atividades de estoque", "Qualidade", "Gestão de ativos"]),
        ("Implementar processos da cadeia de suprimentos", ["Compras e sourcing", "Custo de aquisição", "Vendas e marketing"]),
        ("Implementar armazém e transporte", ["Gestão de armazém", "Processos de armazém", "Transporte", "App móvel"]),
        ("Implementar o planejamento mestre", ["Configuração", "Planos mestres"]),
    ])
C["AB-330"] = dict(
    nome_pt="Consultor de IA para Supply Chain Management", trilha="dynamics", nivel="Associate", status="beta", aposenta=None,
    resumo="A nova certificação de cadeia de suprimentos organizada por processos de ponta a ponta. Chega enquanto a MB-330 se aposenta.",
    publico="Consultores de cadeia de suprimentos que implantam o Dynamics 365 SCM com recursos de IA.",
    prereq=None, antes=["MB-330"], depois=["AB-100"],
    dominios=[
        ("Implementar o processo design to retire", ["Estratégia de produto", "Introdução de produtos", "Produtos ativos"]),
        ("Implementar o processo forecast to plan", ["Estratégia de negócio", "Planejamento de vendas e operações"]),
        ("Implementar o processo inventory to deliver", ["Armazém", "Níveis de estoque", "Entrada e saída de mercadorias"]),
        ("Implementar o processo order to cash", ["Políticas de venda", "Pedidos de venda", "Clientes"]),
        ("Implementar o processo plan to produce", ["Estratégia de produção", "Planejamento e execução da produção"]),
        ("Implementar o processo source to pay", ["Estratégia de compras", "Fornecedores", "Contratos", "Aquisição"]),
    ])
C["MB-500"] = dict(
    nome_pt="Desenvolvedor de apps de finanças e operações", trilha="dynamics", nivel="Associate", status="ativa", aposenta=None,
    resumo="Desenvolver em X++ para os apps de finanças e operações do Dynamics 365: arquitetura, código, relatórios, dados e desempenho.",
    publico="Desenvolvedores de ERP que customizam o Dynamics 365 Finance e Supply Chain.",
    prereq=None, antes=[], depois=["AB-100"],
    dominios=[
        ("Planejar a arquitetura e o design da solução", ["Componentes principais", "ALM"]),
        ("Aplicar ferramentas de desenvolvimento", ["Visual Studio", "Controle de versão"]),
        ("Projetar e desenvolver elementos AOT", ["Interface", "Modelo de dados"]),
        ("Desenvolver e testar código", ["X++", "Extensões", "Framework", "Testes"]),
        ("Implementar relatórios", ["Ferramentas de relatório", "Relatórios do Dynamics 365"]),
        ("Integrar e gerenciar dados", ["Padrões de integração", "Gestão de dados", "Power Platform, Microsoft 365 e Azure"]),
        ("Implementar segurança e otimizar desempenho", ["Políticas de segurança", "Otimização"]),
    ])
C["AB-210"] = dict(
    nome_pt="Consultor de IA para Vendas", trilha="dynamics", nivel="Associate", status="ativa", aposenta=None,
    resumo="Configurar o Dynamics 365 Sales com IA: qualificação de leads, pesquisa de oportunidades e agentes de vendas.",
    publico="Consultores de CRM que implantam vendas com IA.",
    prereq=None, antes=[], depois=["AB-100"],
    dominios=[
        ("Configurar o Dynamics 365 Sales para IA", ["Configuração de vendas", "Catálogo de produtos"]),
        ("Otimizar vendas com IA", ["Estratégia de vendas com IA", "Implantação de agentes", "Insights com IA"]),
        ("Qualificar e priorizar leads com IA", ["Geração e nutrição de leads", "Sales Qualification Agent"]),
        ("Desenvolver negócios com pesquisa inteligente", ["Oportunidades", "Sales Research Agent"]),
        ("Estender o Sales", ["Apps de apoio", "Power Platform"]),
    ])
C["AB-250"] = dict(
    nome_pt="Engenheiro de IA para Contact Center", trilha="dynamics", nivel="Associate", status="ativa", aposenta=None,
    resumo="Implantar o Dynamics 365 Contact Center: canais, voz, agentes de IA, roteamento e analytics.",
    publico="Engenheiros que implantam centrais de atendimento omnicanal com IA.",
    prereq=None, antes=["MB-230"], depois=["AB-100"],
    dominios=[
        ("Implantar o Dynamics 365 Contact Center", ["Implementação", "Administração", "Usuários"]),
        ("Implementar canais", ["Chat e canais digitais", "Canal de voz", "Recursos dos canais"]),
        ("Configurar agentes e recursos de IA", ["Agent assist", "Agentes de voz"]),
        ("Configurar a distribuição de trabalho", ["Filas", "Roteamento unificado"]),
        ("Configurar a experiência do representante", ["Perfis de experiência", "Produtividade", "Base de conhecimento"]),
        ("Gerenciar analytics", ["Experiência do supervisor", "Relatórios"]),
    ])

# ============================ IA PARA NEGÓCIOS ============================
C["AB-730"] = dict(
    nome_pt="Profissional de negócios em IA", trilha="negocios", nivel="Business", status="ativa", aposenta=None,
    resumo="Usar o Microsoft 365 Copilot e agentes no trabalho: prompts, conteúdo, reuniões e resultados de negócio.",
    publico="Qualquer profissional que quer comprovar produtividade com IA no dia a dia. Não é técnica.",
    prereq=None, antes=[], depois=["AB-731"],
    dominios=[
        ("Entender os fundamentos de IA generativa", ["IA generativa no Microsoft 365", "IA responsável e proteção de dados"]),
        ("Gerenciar prompts e chats no Microsoft 365 Copilot", ["Prompts", "Chats"]),
        ("Gerenciar conteúdo e colaboração com o Copilot", ["Criação e análise de conteúdo", "Reuniões e colaboração"]),
        ("Gerar resultados com agentes", ["Agentes prontos do Copilot", "Copilot Cowork"]),
    ])
C["AB-731"] = dict(
    nome_pt="Líder de transformação com IA", trilha="negocios", nivel="Business", status="ativa", aposenta=None,
    resumo="Valor de negócio da IA generativa, Copilot e Foundry, e estratégia de adoção responsável.",
    publico="Gestores, líderes e tomadores de decisão que conduzem a adoção de IA na empresa.",
    prereq=None, antes=["AB-730"], depois=["AB-100"],
    dominios=[
        ("Identificar o valor de negócio da IA generativa", ["Conceitos de IA generativa", "Benefícios e capacidades"]),
        ("Identificar oportunidades nos apps e serviços de IA da Microsoft", ["Microsoft Copilot", "Foundry Tools"]),
        ("Definir a estratégia de implementação e adoção", ["IA responsável", "Adoção na organização"]),
    ])
C["AB-100"] = dict(
    nome_pt="Arquiteto de soluções empresariais de IA agêntica", trilha="negocios", nivel="Expert", status="ativa", aposenta=None,
    resumo="Planejar, projetar e implantar soluções de negócio com IA e agentes, incluindo custos, ALM e governança.",
    publico="Arquitetos de soluções de Dynamics 365, Power Platform e IA que lideram projetos agênticos.",
    prereq="Ter uma certificação Associate da lista oficial (por exemplo AB-400, AB-410, AB-620, AB-210, MB-230, MB-310, MB-800 ou AI-103).",
    antes=["AB-410", "AB-620", "AB-210", "MB-310"], depois=[],
    dominios=[
        ("Planejar soluções de negócio com IA", ["Requisitos", "Estratégia de IA", "Custos e benefícios"]),
        ("Projetar soluções de negócio com IA", ["IA e agentes", "Extensibilidade", "Agentes e apps prontos"]),
        ("Implantar soluções de negócio com IA", ["Monitoramento e ajuste", "Testes", "ALM", "IA responsável e governança"]),
    ])
