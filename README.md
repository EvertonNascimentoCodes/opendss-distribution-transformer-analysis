# OpenDSS Distribution Transformer Analysis

Ferramenta desenvolvida em Python para automação de estudos de fluxo de potência em alimentadores de redes de distribuição, utilizando o **OpenDSS** por meio da biblioteca **PyDSSInterface**.

O projeto tem como foco a análise detalhada dos transformadores de distribuição, permitindo registrar e organizar diversas grandezas elétricas obtidas a partir das simulações.

## Funcionalidades

O projeto permite realizar o cálculo de fluxo de potência e coletar informações relacionadas aos transformadores, incluindo:

* Tensão por fase nos enrolamentos;
* Tensão em p.u.;
* Corrente por fase;
* Potência aparente (VA);
* Potência ativa (W);
* Potência total por enrolamento;
* Potência nominal dos transformadores;
* Corrente nominal e corrente de emergência;
* Quantidade de enrolamentos;
* Tensões primária, secundária e terciária;
* Identificação das barras associadas aos enrolamentos;
* Condição operativa do transformador;
* Identificação de inversão de fluxo de potência;
* Registro das grandezas para diferentes horários de simulação.

## Atenção para o correto preenchimento dos seguintes parãmetros

## Parâmetro Caminho do arquivo DSS que contém todos os elementos dos alimentador a ser estudado ##
dss_file = pathlib.Path(r"D:\Projetos_Python\Sobrecarga\2_TAP2_1_REG_Aumento\01_REG_CTG_Carg_Leve.dss")

## Parâmetros necessários para fluxo de potência ##
loadmult=float(1.00)
param_mode=str("daily")
param_step_size=float(1)
param_qtde_pontos_curva_carga=int(24)
param_voltagebases=str("[0.220 0.380 0.440 13.800]")
param_tolerance=float(0.0001)
param_maxiter=int(1000)
param_maxcontroliter=int(500)

Caso desejar colocar alguma geração distribuida e/ou carga adicional e/ou até mesmo demais elementos adicionar nos arquivos DSS antes de rodar este script

## Tecnologias utilizadas

* **Python 3.13**
* **OpenDSS**
* **PyDSSInterface**
* **Pandas**
* **NumPy**

Bibliotecas nativas do Python, como `os`, `math` e `pathlib`, também são utilizadas no projeto.

## Objetivo

O objetivo do projeto é facilitar a automação e a análise de estudos de fluxo de potência em redes de distribuição, permitindo obter informações detalhadas dos transformadores e estruturar os resultados para análises posteriores.

O projeto pode ser utilizado como base para estudos relacionados a:

* Carregamento de transformadores;
* Análise de tensão;
* Fluxo de potência em redes de distribuição;
* Geração distribuída;
* Inversão de fluxo;
* Avaliação das condições operativas dos equipamentos;
* Processamento e análise de resultados de simulações elétricas.

## Status do projeto

🚧 **Em desenvolvimento**

Novas funcionalidades e melhorias serão adicionadas ao projeto ao longo do desenvolvimento.

## Licença

Este projeto é disponibilizado sob licença própria.

O uso não comercial é permitido, desde que seja mantida a atribuição ao autor.

O uso comercial, redistribuição comercial ou incorporação do código em produtos ou serviços comerciais está sujeito às condições estabelecidas na licença do projeto.

Consulte o arquivo `LICENSE` para obter os termos completos.

## Autor

**Everton Nascimento**

Electrical Engineer | Energy Systems | Physics & Engineering Education | Technology Solutions & Data Analytics

---

*Projeto desenvolvido para automação e apoio à análise de sistemas elétricos de distribuição.*

