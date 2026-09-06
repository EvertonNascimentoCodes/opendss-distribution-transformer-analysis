import py_dss_interface
import pathlib
import os
import math
import pandas as pd


## Caminho do arquivo DSS que contém todos os elementos dos alimentador a ser estudado ##
dss_file = pathlib.Path(r"D:\Projetos_Python\Sobrecarga\2_TAP2_1_REG_Aumento\01_REG_CTG_Carg_Leve.dss")

## Coloca o apelido na biblioteca py_dss_interface como DSS ##
dss=py_dss_interface.DSS()

## Parâmetros necessários para fluxo de potência ##
loadmult=float(1.00)
param_mode=str("daily")
param_step_size=float(1)
param_qtde_pontos_curva_carga=int(24)
param_voltagebases=str("[0.220 0.380 0.440 13.800]")
param_tolerance=float(0.0001)
param_maxiter=int(1000)
param_maxcontroliter=int(500)

## Realiza o carregamento do arquivo DSS apontado e cria as redes ##
dss.text(f"compile [{dss_file}]")

## Verifica se carregou o arquivo e identificou o nome do alimentador para dar andamento a análise##
if dss_file.exists()==True:
    print(f"Arquivo carregado é do alimentador {dss.circuit.name}.")
    transformadores_qtd=int(dss.transformers.count)
    print(f"O alimentador {dss.circuit.name} possui {transformadores_qtd} transformadores.")
    
    #### Atribui zero inicialmente para a contagem de transformadores ####
    cont_transformadores=int(0)
    
    #### Atribui zero inicialmente para a contagem da quantidade de pontos da simulação e calcula a quantidade de horas total ####
    conta_hora_tr=float(0)
    total_hora_tr=float(param_step_size*param_qtde_pontos_curva_carga)
    
    #### Cria Lista Vazia ####
    dados_tabela_tr=[]
    
    #### Calcula o fluxo de potência para cada ponto da curva de carga ####
    while (conta_hora_tr<(total_hora_tr- 1e-9)):
    ##while (conta_hora_tr<1):
        dss.text(f"Set loadmult={loadmult}")
        dss.text(f"Set mode={param_mode}")
        dss.text(f"Set stepsize={param_step_size}")
        dss.text(f"Set number=1")
        dss.text(f"Set hour={conta_hora_tr*param_step_size}")
        dss.text(f"Set Voltagebases={param_voltagebases}")
        dss.text(f"Calc Voltagebases")
        dss.text(f"Set tolerance = 0.0001")
        dss.text(f"Set maxiter=100")
        dss.text(f"Set maxcontroliter = 50")
        dss.text(f"Solve")
        
        #### Zera a contagem de transformadores ####
        cont_transformadores=int(0)
        
        #### Ativa o primeiro transformador da lista em memória dos transformadores do alimentador ####
        dss.transformers.first()
        
        
        #### Registra a hora que será pego os valores ####
        hora_tr=(conta_hora_tr*param_step_size)
        print(f"{hora_tr}")
        
        #############################################################################################################
        #### A partir deste ponto depois pode ser criada a função do transformador e só realizado a chamada aqui ####
        #############################################################################################################
        while (cont_transformadores<transformadores_qtd):
            #### Registra o nome do transformador ####
            transformador_id=(dss.transformers.name)
            print(f"{transformador_id}")
            
            #### Registra a potência nominal do transformador e as correntes normais e emergenciais ####
            dss.transformers.wdg = 1
            kVA_nom_tr=(dss.transformers.kva)
            #print(f"{kVA_nom_tr}")
            corrente_nom_tr=(dss.cktelement.norm_amps)
            #print(f"{corrente_nom_tr}")
            corrente_emerg_tr=(dss.cktelement.emerg_amps)
            #print(f"{corrente_emerg_tr}")
            
            #### Registra a quantidade de enrolamentos do transformador ####
            qtde_enrolamentos_tr=(dss.transformers.num_windings)
            #print(f"{qtde_enrolamentos_tr}")
            
            #### Registra a tensão nominal primária, secundária e terciária se houver ####
            dss.transformers.wdg = 1
            kv_primario = dss.transformers.kv
            #print(f"{kv_primario}")
            dss.transformers.wdg = 2
            kv_secundario = dss.transformers.kv
            #print(f"{kv_secundario}")
            if qtde_enrolamentos_tr==3:
                dss.transformers.wdg = 3
                kv_terciario = dss.transformers.kv
                #print(f"{kv_terciario}")
            else:
                kv_terciario =0
            
            #### Ativa novamente a referência de propriedades para o enrolamento primário ####
            dss.transformers.wdg = 1
            
            #### Registra a quantidade de fases do transformador ####
            phases_tr=(dss.cktelement.num_phases)
            #print(f"{phases_tr}")
            
            #### Registra qual é a barra de conexão do primário do transformador ####
            barra_primaria_tr=(dss.cktelement.bus_names[0])
            #print(f"{barra_primaria_tr}")
            
            #### Registra qual é a barra de conexão do secundário do transformador ####
            barra_secundaria_tr=(dss.cktelement.bus_names[1])
            #print(f"{barra_secundaria_tr}")
            
            #### Registra qual é a barra de conexão do terciário do transformador ####
            if qtde_enrolamentos_tr==3:
                barra_terciaria_tr=(dss.cktelement.bus_names[2])
                #print(f"{barra_terciaria_tr}")
            else:
                barra_terciaria_tr=0
            
            #### Registra o resultado das principais grandezas elétricas calculadas e sequência dos nós para saber sequência das fases ####
            V_voltages_tr=(dss.cktelement.voltages_mag_ang)
            #print(f"{V_voltages_tr}")
            nodes_phases_tr=(dss.cktelement.node_order)
            #print(f"{nodes_phases_tr}")
            correntes_tr=(dss.cktelement.currents_mag_ang)
            #print(f"{correntes_tr}")
            potencias_tr=(dss.cktelement.powers)
            #print(f"{potencias_tr}")
            ####################################
            #### Transformadores trifásicos ####
            ####################################
            if phases_tr==3 and nodes_phases_tr[0]==1 and nodes_phases_tr[1]==2 and nodes_phases_tr[2]==3:
                #### Dados do Primário ####
                V_fase_A_pri= V_voltages_tr[0]
                V_fase_B_pri= V_voltages_tr[2]
                V_fase_C_pri= V_voltages_tr[4]
                Vpu_fase_A_pri=V_fase_A_pri/((kv_primario*1000)/math.sqrt(3))
                Vpu_fase_B_pri=V_fase_B_pri/((kv_primario*1000)/math.sqrt(3))
                Vpu_fase_C_pri=V_fase_C_pri/((kv_primario*1000)/math.sqrt(3))
                Amps_fase_A_pri= correntes_tr[0]
                Amps_fase_B_pri= correntes_tr[2]
                Amps_fase_C_pri= correntes_tr[4]
                VA_fase_A_pri=V_fase_A_pri*Amps_fase_A_pri
                VA_fase_B_pri=V_fase_B_pri*Amps_fase_B_pri
                VA_fase_C_pri=V_fase_C_pri*Amps_fase_C_pri
                VA_tot_tr_pri=VA_fase_A_pri+VA_fase_B_pri+VA_fase_C_pri
                W_fase_A_pri=potencias_tr[0]*1000
                W_fase_B_pri=potencias_tr[2]*1000
                W_fase_C_pri=potencias_tr[4]*1000
                W_tot_tr_pri=W_fase_A_pri+W_fase_B_pri+W_fase_C_pri
                if VA_tot_tr_pri>kVA_nom_tr*1000 and  VA_tot_tr_pri<1.3*kVA_nom_tr*1000:
                    cond_ope_tr=str('Sobrecarga - Dentro do limite térmico')
                    #print(f"{cond_ope_tr}")
                elif VA_tot_tr_pri>1.3*kVA_nom_tr*1000:
                    cond_ope_tr=str('Sobrecarga - Acima do limite térmico')
                    #print(f"{cond_ope_tr}")
                else:
                    cond_ope_tr=str('Normal - Abaixo da potência nominal')
                    #print(f"{cond_ope_tr}")
                #### Dados do Secundário ####
                V_fase_A_sec= V_voltages_tr[8]
                V_fase_B_sec= V_voltages_tr[10]
                V_fase_C_sec= V_voltages_tr[12]
                Vpu_fase_A_sec=V_fase_A_sec/((kv_secundario*1000)/math.sqrt(3))
                Vpu_fase_B_sec=V_fase_B_sec/((kv_secundario*1000)/math.sqrt(3))
                Vpu_fase_C_sec=V_fase_C_sec/((kv_secundario*1000)/math.sqrt(3))
                Amps_fase_A_sec= correntes_tr[8]
                Amps_fase_B_sec= correntes_tr[10]
                Amps_fase_C_sec= correntes_tr[12]
                VA_fase_A_sec=V_fase_A_sec*Amps_fase_A_sec
                VA_fase_B_sec=V_fase_B_sec*Amps_fase_B_sec
                VA_fase_C_sec=V_fase_C_sec*Amps_fase_C_sec
                VA_tot_tr_sec=VA_fase_A_sec+VA_fase_B_sec+VA_fase_C_sec
                #### OpenDSS entende que o que entra no terminal é positivo e o que sai do terminal é negativo, por isso multipiquei por -1 para não confundir com inversão do fluxo de potência ####
                W_fase_A_sec=potencias_tr[8]*1000*(-1)
                W_fase_B_sec=potencias_tr[10]*1000*(-1)
                W_fase_C_sec=potencias_tr[12]*1000*(-1)
                W_tot_tr_sec=W_fase_A_sec+W_fase_B_sec+W_fase_C_sec
                if qtde_enrolamentos_tr==3:
                    #### Dados do Terciário ####
                    V_fase_A_ter= V_voltages_tr[16]
                    V_fase_B_ter= V_voltages_tr[18]
                    V_fase_C_ter= V_voltages_tr[20]
                    Vpu_fase_A_ter=V_fase_A_ter/((kv_terciario*1000)/math.sqrt(3))
                    Vpu_fase_B_ter=V_fase_B_ter/((kv_terciario*1000)/math.sqrt(3))
                    Vpu_fase_C_ter=V_fase_C_ter/((kv_terciario*1000)/math.sqrt(3))
                    Amps_fase_A_ter= correntes_tr[16]
                    Amps_fase_B_ter= correntes_tr[18]
                    Amps_fase_C_ter= correntes_tr[20]
                    VA_fase_A_ter=V_fase_A_ter*Amps_fase_A_ter
                    VA_fase_B_ter=V_fase_B_ter*Amps_fase_B_ter
                    VA_fase_C_ter=V_fase_C_ter*Amps_fase_C_ter
                    VA_tot_tr_ter=VA_fase_A_ter+VA_fase_B_ter+VA_fase_C_ter
                    #### OpenDSS entende que o que entra no terminal é positivo e o que sai do terminal é negativo, por isso multipiquei por -1 para não confundir com inversão do fluxo de potência ####
                    W_fase_A_ter=potencias_tr[16]*1000*(-1)
                    W_fase_B_ter=potencias_tr[18]*1000*(-1)
                    W_fase_C_ter=potencias_tr[20]*1000*(-1)
                    W_tot_tr_ter=W_fase_A_ter+W_fase_B_ter+W_fase_C_ter
                else:
                    V_fase_A_ter=0
                    V_fase_B_ter=0
                    V_fase_C_ter=0
                    Vpu_fase_A_ter=0
                    Vpu_fase_B_ter=0
                    Vpu_fase_C_ter=0
                    Amps_fase_A_ter=0
                    Amps_fase_B_ter=0
                    Amps_fase_C_ter=0
                    VA_fase_A_ter=0
                    VA_fase_B_ter=0
                    VA_fase_C_ter=0
                    VA_tot_tr_ter=0
                    W_fase_A_ter=0
                    W_fase_B_ter=0
                    W_fase_C_ter=0
                    W_tot_tr_ter=0
            
            ####################################
            #### Transformadores Bifásicos #####
            ####################################
            if phases_tr==2:
                ##################################################
                ####Bifásicos ligados nas Fases AB no primário####
                ##################################################
                if nodes_phases_tr[0]==1 and nodes_phases_tr[1]==2:
                    V_fase_A_pri= V_voltages_tr[0]
                    V_fase_B_pri= V_voltages_tr[2]
                    V_fase_C_pri= 0
                    Vpu_fase_A_pri=V_fase_A_pri/((kv_primario*1000)/math.sqrt(3))
                    Vpu_fase_B_pri=V_fase_B_pri/((kv_primario*1000)/math.sqrt(3))
                    Vpu_fase_C_pri=0
                    Amps_fase_A_pri= correntes_tr[0]
                    Amps_fase_B_pri= correntes_tr[2]
                    Amps_fase_C_pri= 0
                    VA_fase_A_pri=V_fase_A_pri*Amps_fase_A_pri
                    VA_fase_B_pri=V_fase_B_pri*Amps_fase_B_pri
                    VA_fase_C_pri=0
                    VA_tot_tr_pri=VA_fase_A_pri+VA_fase_B_pri+VA_fase_C_pri
                    W_fase_A_pri=potencias_tr[0]*1000
                    W_fase_B_pri=potencias_tr[2]*1000
                    W_fase_C_pri=0
                    W_tot_tr_pri=W_fase_A_pri+W_fase_B_pri+W_fase_C_pri
                    if VA_tot_tr_pri>kVA_nom_tr*1000 and  VA_tot_tr_pri<1.3*kVA_nom_tr*1000:
                        cond_ope_tr=str('Sobrecarga - Dentro do limite térmico')
                        #print(f"{cond_ope_tr}")
                    elif VA_tot_tr_pri>1.3*kVA_nom_tr*1000:
                        cond_ope_tr=str('Sobrecarga - Acima do limite térmico')
                        #print(f"{cond_ope_tr}")
                    else:
                        cond_ope_tr=str('Normal - Abaixo da potência nominal')
                        #print(f"{cond_ope_tr}")
                        
                ##################################################
                ####Bifásicos ligados nas Fases BC no primário####
                ##################################################
                if nodes_phases_tr[0]==2 and nodes_phases_tr[1]==3:
                    V_fase_A_pri= 0
                    V_fase_B_pri= V_voltages_tr[0]
                    V_fase_C_pri= V_voltages_tr[2]
                    Vpu_fase_A_pri=0
                    Vpu_fase_B_pri=V_fase_B_pri/((kv_primario*1000)/math.sqrt(3))
                    Vpu_fase_C_pri=V_fase_C_pri/((kv_primario*1000)/math.sqrt(3))
                    Amps_fase_A_pri= 0
                    Amps_fase_B_pri= correntes_tr[0]
                    Amps_fase_C_pri= correntes_tr[2]
                    VA_fase_A_pri=0
                    VA_fase_B_pri=V_fase_B_pri*Amps_fase_B_pri
                    VA_fase_C_pri=V_fase_C_pri*Amps_fase_C_pri
                    VA_tot_tr_pri=VA_fase_A_pri+VA_fase_B_pri+VA_fase_C_pri
                    W_fase_A_pri=0
                    W_fase_B_pri=potencias_tr[0]*1000
                    W_fase_C_pri=potencias_tr[2]*1000
                    W_tot_tr_pri=W_fase_A_pri+W_fase_B_pri+W_fase_C_pri
                    if VA_tot_tr_pri>kVA_nom_tr*1000 and  VA_tot_tr_pri<1.3*kVA_nom_tr*1000:
                        cond_ope_tr=str('Sobrecarga - Dentro do limite térmico')
                        #print(f"{cond_ope_tr}")
                    elif VA_tot_tr_pri>1.3*kVA_nom_tr*1000:
                        cond_ope_tr=str('Sobrecarga - Acima do limite térmico')
                        #print(f"{cond_ope_tr}")
                    else:
                        cond_ope_tr=str('Normal - Abaixo da potência nominal')
                        #print(f"{cond_ope_tr}")
                        
                ##################################################
                ####Bifásicos ligados nas Fases CA no primário####
                ##################################################
                if nodes_phases_tr[0]==3 and nodes_phases_tr[1]==1:
                    V_fase_A_pri= V_voltages_tr[2]
                    V_fase_B_pri= 0
                    V_fase_C_pri= V_voltages_tr[0]
                    Vpu_fase_A_pri=V_fase_A_pri/((kv_primario*1000)/math.sqrt(3))
                    Vpu_fase_B_pri=0
                    Vpu_fase_C_pri=V_fase_C_pri/((kv_primario*1000)/math.sqrt(3))
                    Amps_fase_A_pri= correntes_tr[2]
                    Amps_fase_B_pri= 0
                    Amps_fase_C_pri= correntes_tr[0]
                    VA_fase_A_pri=V_fase_A_pri*Amps_fase_A_pri
                    VA_fase_B_pri=0
                    VA_fase_C_pri=V_fase_C_pri*Amps_fase_C_pri
                    VA_tot_tr_pri=VA_fase_A_pri+VA_fase_B_pri+VA_fase_C_pri
                    W_fase_A_pri=potencias_tr[2]*1000
                    W_fase_B_pri=0
                    W_fase_C_pri=potencias_tr[0]*1000
                    W_tot_tr_pri=W_fase_A_pri+W_fase_B_pri+W_fase_C_pri
                    if VA_tot_tr_pri>kVA_nom_tr*1000 and  VA_tot_tr_pri<1.3*kVA_nom_tr*1000:
                        cond_ope_tr=str('Sobrecarga - Dentro do limite térmico')
                        #print(f"{cond_ope_tr}")
                    elif VA_tot_tr_pri>1.3*kVA_nom_tr*1000:
                        cond_ope_tr=str('Sobrecarga - Acima do limite térmico')
                        #print(f"{cond_ope_tr}")
                    else:
                        cond_ope_tr=str('Normal - Abaixo da potência nominal')
                        #print(f"{cond_ope_tr}")
                
                ####################################################
                ####Bifásicos Ligados nas Fases AB no Secundário####
                ####################################################
                if nodes_phases_tr[3]==1 and nodes_phases_tr[4]==2:
                    V_fase_A_sec= V_voltages_tr[6]
                    V_fase_B_sec= V_voltages_tr[8]
                    V_fase_C_sec= 0
                    Vpu_fase_A_sec=V_fase_A_sec/(kv_secundario*1000)
                    Vpu_fase_B_sec=V_fase_B_sec/(kv_secundario*1000)
                    Vpu_fase_C_sec=0
                    Amps_fase_A_sec= correntes_tr[6]
                    Amps_fase_B_sec= correntes_tr[8]
                    Amps_fase_C_sec= 0
                    VA_fase_A_sec=V_fase_A_sec*Amps_fase_A_sec
                    VA_fase_B_sec=V_fase_B_sec*Amps_fase_B_sec
                    VA_fase_C_sec=0
                    VA_tot_tr_sec=VA_fase_A_sec+VA_fase_B_sec+VA_fase_C_sec
                    #### OpenDSS entende que o que entra no terminal é positivo e o que sai do terminal é negativo, por isso multipiquei por -1 para não confundir com inversão do fluxo de potência ####
                    W_fase_A_sec=potencias_tr[6]*1000*(-1)
                    W_fase_B_sec=potencias_tr[8]*1000*(-1)
                    W_fase_C_sec=0
                    W_tot_tr_sec=W_fase_A_sec+W_fase_B_sec+W_fase_C_sec
                    
                    #### Dados do Terciário####
                    V_fase_A_ter= 0
                    V_fase_B_ter= 0
                    V_fase_C_ter= 0
                    Vpu_fase_A_ter=0
                    Vpu_fase_B_ter=0
                    Vpu_fase_C_ter=0
                    Amps_fase_A_ter= 0
                    Amps_fase_B_ter= 0
                    Amps_fase_C_ter= 0
                    VA_fase_A_ter=0
                    VA_fase_B_ter=0
                    VA_fase_C_ter=0
                    VA_tot_tr_ter=0
                    #### OpenDSS entende que o que entra no terminal é positivo e o que sai do terminal é negativo, por isso multipiquei por -1 para não confundir com inversão do fluxo de potência ####
                    W_fase_A_ter=0
                    W_fase_B_ter=0
                    W_fase_C_ter=0
                    W_tot_tr_ter=0
                    
                ####################################################
                ####Bifásicos Ligados nas Fases BC no Secundário####
                ####################################################
                if nodes_phases_tr[3]==2 and nodes_phases_tr[4]==3:
                    V_fase_A_sec= V_voltages_tr[6]
                    V_fase_B_sec= 0
                    V_fase_C_sec= V_voltages_tr[8]
                    Vpu_fase_A_sec=V_fase_A_sec/(kv_secundario*1000)
                    Vpu_fase_B_sec=0
                    Vpu_fase_C_sec=V_fase_C_sec/(kv_secundario*1000)
                    Amps_fase_A_sec= correntes_tr[6]
                    Amps_fase_B_sec= 0
                    Amps_fase_C_sec= correntes_tr[8]
                    VA_fase_A_sec=V_fase_A_sec*Amps_fase_A_sec
                    VA_fase_B_sec=0
                    VA_fase_C_sec=V_fase_C_sec*Amps_fase_C_sec
                    VA_tot_tr_sec=VA_fase_A_sec+VA_fase_B_sec+VA_fase_C_sec
                    #### OpenDSS entende que o que entra no terminal é positivo e o que sai do terminal é negativo, por isso multipiquei por -1 para não confundir com inversão do fluxo de potência ####
                    W_fase_A_sec=potencias_tr[6]*1000*(-1)
                    W_fase_B_sec=0
                    W_fase_C_sec=potencias_tr[8]*1000*(-1)
                    W_tot_tr_sec=W_fase_A_sec+W_fase_B_sec+W_fase_C_sec
                    
                    #### Dados do Terciário####
                    V_fase_A_ter= 0
                    V_fase_B_ter= 0
                    V_fase_C_ter= 0
                    Vpu_fase_A_ter=0
                    Vpu_fase_B_ter=0
                    Vpu_fase_C_ter=0
                    Amps_fase_A_ter= 0
                    Amps_fase_B_ter= 0
                    Amps_fase_C_ter= 0
                    VA_fase_A_ter=0
                    VA_fase_B_ter=0
                    VA_fase_C_ter=0
                    VA_tot_tr_ter=0
                    #### OpenDSS entende que o que entra no terminal é positivo e o que sai do terminal é negativo, por isso multipiquei por -1 para não confundir com inversão do fluxo de potência ####
                    W_fase_A_ter=0
                    W_fase_B_ter=0
                    W_fase_C_ter=0
                    W_tot_tr_ter=0
                
                ####################################################
                ####Bifásicos Ligados nas Fases CA no Secundário####
                ####################################################
                if nodes_phases_tr[3]==3 and nodes_phases_tr[4]==1:
                    V_fase_A_sec= V_voltages_tr[8]
                    V_fase_B_sec= 0
                    V_fase_C_sec= V_voltages_tr[6]
                    Vpu_fase_A_sec=V_fase_A_sec/(kv_secundario*1000)
                    Vpu_fase_B_sec=0
                    Vpu_fase_C_sec=V_fase_C_sec/(kv_secundario*1000)
                    Amps_fase_A_sec= correntes_tr[8]
                    Amps_fase_B_sec= 0
                    Amps_fase_C_sec= correntes_tr[6]
                    VA_fase_A_sec=V_fase_A_sec*Amps_fase_A_sec
                    VA_fase_B_sec=0
                    VA_fase_C_sec=V_fase_C_sec*Amps_fase_C_sec
                    VA_tot_tr_sec=VA_fase_A_sec+VA_fase_B_sec+VA_fase_C_sec
                    #### OpenDSS entende que o que entra no terminal é positivo e o que sai do terminal é negativo, por isso multipiquei por -1 para não confundir com inversão do fluxo de potência ####
                    W_fase_A_sec=potencias_tr[8]*1000*(-1)
                    W_fase_B_sec=0
                    W_fase_C_sec=potencias_tr[6]*1000*(-1)
                    W_tot_tr_sec=W_fase_A_sec+W_fase_B_sec+W_fase_C_sec
                    
                    #### Dados do Terciário####
                    V_fase_A_ter= 0
                    V_fase_B_ter= 0
                    V_fase_C_ter= 0
                    Vpu_fase_A_ter=0
                    Vpu_fase_B_ter=0
                    Vpu_fase_C_ter=0
                    Amps_fase_A_ter= 0
                    Amps_fase_B_ter= 0
                    Amps_fase_C_ter= 0
                    VA_fase_A_ter=0
                    VA_fase_B_ter=0
                    VA_fase_C_ter=0
                    VA_tot_tr_ter=0
                    #### OpenDSS entende que o que entra no terminal é positivo e o que sai do terminal é negativo, por isso multipiquei por -1 para não confundir com inversão do fluxo de potência ####
                    W_fase_A_ter=0
                    W_fase_B_ter=0
                    W_fase_C_ter=0
                    W_tot_tr_ter=0
                    
            ################################################################        
            #### Transformadores Monofásicos Ligados Fase A NO PRIMÁRIO ####
            ################################################################
            if phases_tr==1 and nodes_phases_tr[0]==1:
                #### Dados do Primário ####
                V_fase_A_pri= V_voltages_tr[0]
                V_fase_B_pri= 0
                V_fase_C_pri= 0
                Vpu_fase_A_pri=V_fase_A_pri/(kv_primario*1000)
                Vpu_fase_B_pri=0
                Vpu_fase_C_pri=0
                Amps_fase_A_pri= correntes_tr[0]
                Amps_fase_B_pri= 0
                Amps_fase_C_pri= 0
                VA_fase_A_pri=V_fase_A_pri*Amps_fase_A_pri
                VA_fase_B_pri=0
                VA_fase_C_pri=0
                VA_tot_tr_pri=VA_fase_A_pri+VA_fase_B_pri+VA_fase_C_pri
                W_fase_A_pri=potencias_tr[0]*1000
                W_fase_B_pri=0
                W_fase_C_pri=0
                W_tot_tr_pri=W_fase_A_pri+W_fase_B_pri+W_fase_C_pri
                if VA_tot_tr_pri>kVA_nom_tr*1000 and  VA_tot_tr_pri<1.3*kVA_nom_tr*1000:
                    cond_ope_tr=str('Sobrecarga - Dentro do limite térmico')
                    #print(f"{cond_ope_tr}")
                elif VA_tot_tr_pri>1.3*kVA_nom_tr*1000:
                    cond_ope_tr=str('Sobrecarga - Acima do limite térmico')
                    #print(f"{cond_ope_tr}")
                else:
                    cond_ope_tr=str('Normal - Abaixo da potência nominal')
                    #print(f"{cond_ope_tr}")
            
            ################################################################        
            #### Transformadores Monofásicos Ligados Fase B NO PRIMÁRIO ####
            ################################################################
            if phases_tr==1 and nodes_phases_tr[0]==2:
                #### Dados do Primário ####
                V_fase_A_pri=0 
                V_fase_B_pri=V_voltages_tr[0]
                V_fase_C_pri=0
                Vpu_fase_A_pri=0
                Vpu_fase_B_pri=V_fase_B_pri/(kv_primario*1000)
                Vpu_fase_C_pri=0
                Amps_fase_A_pri= 0
                Amps_fase_B_pri= correntes_tr[0]
                Amps_fase_C_pri= 0
                VA_fase_A_pri=0
                VA_fase_B_pri=V_fase_B_pri*Amps_fase_B_pri
                VA_fase_C_pri=0
                VA_tot_tr_pri=VA_fase_A_pri+VA_fase_B_pri+VA_fase_C_pri
                W_fase_A_pri=0
                W_fase_B_pri=potencias_tr[0]*1000
                W_fase_C_pri=0
                W_tot_tr_pri=W_fase_A_pri+W_fase_B_pri+W_fase_C_pri
                if VA_tot_tr_pri>kVA_nom_tr*1000 and  VA_tot_tr_pri<1.3*kVA_nom_tr*1000:
                    cond_ope_tr=str('Sobrecarga - Dentro do limite térmico')
                    #print(f"{cond_ope_tr}")
                elif VA_tot_tr_pri>1.3*kVA_nom_tr*1000:
                    cond_ope_tr=str('Sobrecarga - Acima do limite térmico')
                    #print(f"{cond_ope_tr}")
                else:
                    cond_ope_tr=str('Normal - Abaixo da potência nominal')
                    #print(f"{cond_ope_tr}")

            ################################################################        
            #### Transformadores Monofásicos Ligados Fase C NO PRIMÁRIO ####
            ################################################################
            if phases_tr==1 and nodes_phases_tr[0]==3:
                #### Dados do Primário ####
                V_fase_A_pri=0 
                V_fase_B_pri=0
                V_fase_C_pri=V_voltages_tr[0]
                Vpu_fase_A_pri=0
                Vpu_fase_B_pri=0
                Vpu_fase_C_pri=V_fase_C_pri/(kv_primario*1000)
                Amps_fase_A_pri= 0
                Amps_fase_B_pri= 0
                Amps_fase_C_pri= correntes_tr[0]
                VA_fase_A_pri=0
                VA_fase_B_pri=0
                VA_fase_C_pri=V_fase_C_pri*Amps_fase_C_pri
                VA_tot_tr_pri=VA_fase_A_pri+VA_fase_B_pri+VA_fase_C_pri
                W_fase_A_pri=0
                W_fase_B_pri=0
                W_fase_C_pri=potencias_tr[0]*1000
                W_tot_tr_pri=W_fase_A_pri+W_fase_B_pri+W_fase_C_pri
                if VA_tot_tr_pri>kVA_nom_tr*1000 and  VA_tot_tr_pri<1.3*kVA_nom_tr*1000:
                    cond_ope_tr=str('Sobrecarga - Dentro do limite térmico')
                    #print(f"{cond_ope_tr}")
                elif VA_tot_tr_pri>1.3*kVA_nom_tr*1000:
                    cond_ope_tr=str('Sobrecarga - Acima do limite térmico')
                    #print(f"{cond_ope_tr}")
                else:
                    cond_ope_tr=str('Normal - Abaixo da potência nominal')
                    #print(f"{cond_ope_tr}")
            
            ################################################################        
            #### Transformadores Monofásicos Ligados Fase A NO SECUNDÁRIO ##
            ################################################################
            if phases_tr==1 and nodes_phases_tr[2]==1:
                V_fase_A_sec= V_voltages_tr[4]
                V_fase_B_sec= 0
                V_fase_C_sec= 0
                Vpu_fase_A_sec=V_fase_A_sec/(kv_secundario*1000)
                Vpu_fase_B_sec=0
                Vpu_fase_C_sec=0
                Amps_fase_A_sec= correntes_tr[4]
                Amps_fase_B_sec= 0
                Amps_fase_C_sec= 0
                VA_fase_A_sec=V_fase_A_sec*Amps_fase_A_sec
                VA_fase_B_sec=0
                VA_fase_C_sec=0
                VA_tot_tr_sec=VA_fase_A_sec+VA_fase_B_sec+VA_fase_C_sec
                #### OpenDSS entende que o que entra no terminal é positivo e o que sai do terminal é negativo, por isso multipiquei por -1 para não confundir com inversão do fluxo de potência ####
                W_fase_A_sec=potencias_tr[4]*1000*(-1)
                W_fase_B_sec=0
                W_fase_C_sec=0
                W_tot_tr_sec=W_fase_A_sec+W_fase_B_sec+W_fase_C_sec
                    
            ################################################################        
            #### Transformadores Monofásicos Ligados Fase B NO SECUNDÁRIO ##
            ################################################################
            if phases_tr==1 and nodes_phases_tr[2]==2:
                V_fase_A_sec= 0
                V_fase_B_sec= V_voltages_tr[4]
                V_fase_C_sec= 0
                Vpu_fase_A_sec=0
                Vpu_fase_B_sec=V_fase_B_sec/(kv_secundario*1000)
                Vpu_fase_C_sec=0
                Amps_fase_A_sec= 0
                Amps_fase_B_sec= correntes_tr[4]
                Amps_fase_C_sec= 0
                VA_fase_A_sec=0
                VA_fase_B_sec=V_fase_B_sec*Amps_fase_B_sec
                VA_fase_C_sec=0
                VA_tot_tr_sec=VA_fase_A_sec+VA_fase_B_sec+VA_fase_C_sec
                #### OpenDSS entende que o que entra no terminal é positivo e o que sai do terminal é negativo, por isso multipiquei por -1 para não confundir com inversão do fluxo de potência ####
                W_fase_A_sec=0
                W_fase_B_sec=potencias_tr[4]*1000*(-1)
                W_fase_C_sec=0
                W_tot_tr_sec=W_fase_A_sec+W_fase_B_sec+W_fase_C_sec
                
            ################################################################        
            #### Transformadores Monofásicos Ligados Fase C NO SECUNDÁRIO ##
            ################################################################
            if phases_tr==1 and nodes_phases_tr[2]==3:
                V_fase_A_sec= 0
                V_fase_B_sec= 0
                V_fase_C_sec= V_voltages_tr[4]
                Vpu_fase_A_sec=0
                Vpu_fase_B_sec=0
                Vpu_fase_C_sec=V_fase_C_sec/(kv_secundario*1000)
                Amps_fase_A_sec= 0
                Amps_fase_B_sec= 0
                Amps_fase_C_sec= correntes_tr[4]
                VA_fase_A_sec=0
                VA_fase_B_sec=0
                VA_fase_C_sec=V_fase_C_sec*Amps_fase_C_sec
                VA_tot_tr_sec=VA_fase_A_sec+VA_fase_B_sec+VA_fase_C_sec
                #### OpenDSS entende que o que entra no terminal é positivo e o que sai do terminal é negativo, por isso multipiquei por -1 para não confundir com inversão do fluxo de potência ####
                W_fase_A_sec=0
                W_fase_B_sec=0
                W_fase_C_sec=potencias_tr[4]*1000*(-1)
                W_tot_tr_sec=W_fase_A_sec+W_fase_B_sec+W_fase_C_sec           
            
            #################################################        
            #### Transformadores Monofásicos A TRÊS FIOS ####
            #################################################
            if qtde_enrolamentos_tr==3 and phases_tr==1:
                ###############################################################################        
                #### Transformadores Monofásicos A TRÊS FIOS Ligados Fase AB NO LADO DE BT ####
                ###############################################################################
                if nodes_phases_tr[2]==1 and nodes_phases_tr[5]==2:
                    V_fase_A_sec= V_voltages_tr[4]
                    V_fase_B_sec= 0
                    V_fase_C_sec= 0
                    Vpu_fase_A_sec=V_fase_A_sec/(kv_secundario*1000)
                    Vpu_fase_B_sec=0
                    Vpu_fase_C_sec=0
                    Amps_fase_A_sec= correntes_tr[4]
                    Amps_fase_B_sec= 0
                    Amps_fase_C_sec= 0
                    VA_fase_A_sec=V_fase_A_sec*Amps_fase_A_sec
                    VA_fase_B_sec=0
                    VA_fase_C_sec=0
                    VA_tot_tr_sec=VA_fase_A_sec+VA_fase_B_sec+VA_fase_C_sec
                    #### OpenDSS entende que o que entra no terminal é positivo e o que sai do terminal é negativo, por isso multipiquei por -1 para não confundir com inversão do fluxo de potência ####
                    W_fase_A_sec=potencias_tr[4]*1000*(-1)
                    W_fase_B_sec=0
                    W_fase_C_sec=0
                    W_tot_tr_sec=W_fase_A_sec+W_fase_B_sec+W_fase_C_sec
                    
                    #### Dados do Terciário####
                    V_fase_A_ter= 0
                    V_fase_B_ter= V_voltages_tr[10]
                    V_fase_C_ter= 0
                    Vpu_fase_A_ter=0
                    Vpu_fase_B_ter=V_fase_B_ter/(kv_secundario*1000)
                    Vpu_fase_C_ter=0
                    Amps_fase_A_ter= 0
                    Amps_fase_B_ter= correntes_tr[10]
                    Amps_fase_C_ter= 0
                    VA_fase_A_ter=0
                    VA_fase_B_ter=V_fase_B_ter*Amps_fase_B_ter
                    VA_fase_C_ter=0
                    VA_tot_tr_ter=VA_fase_A_ter+VA_fase_B_ter+VA_fase_C_ter
                    #### OpenDSS entende que o que entra no terminal é positivo e o que sai do terminal é negativo, por isso multipiquei por -1 para não confundir com inversão do fluxo de potência ####
                    W_fase_A_ter=0
                    W_fase_B_ter=potencias_tr[10]*1000*(-1)
                    W_fase_C_ter=0
                    W_tot_tr_ter=W_fase_A_ter+W_fase_B_ter+W_fase_C_ter
                    
                ###############################################################################        
                #### Transformadores Monofásicos A TRÊS FIOS Ligados Fase BC NO LADO DE BT ####
                ###############################################################################
                if nodes_phases_tr[2]==2 and nodes_phases_tr[5]==3:
                    V_fase_A_sec= 0
                    V_fase_B_sec= V_voltages_tr[4]
                    V_fase_C_sec= 0
                    Vpu_fase_A_sec=0
                    Vpu_fase_B_sec=V_fase_B_sec/(kv_secundario*1000)
                    Vpu_fase_C_sec=0
                    Amps_fase_A_sec= 0
                    Amps_fase_B_sec= correntes_tr[4]
                    Amps_fase_C_sec= 0
                    VA_fase_A_sec=0
                    VA_fase_B_sec=V_fase_B_sec*Amps_fase_B_sec
                    VA_fase_C_sec=0
                    VA_tot_tr_sec=VA_fase_A_sec+VA_fase_B_sec+VA_fase_C_sec
                    #### OpenDSS entende que o que entra no terminal é positivo e o que sai do terminal é negativo, por isso multipiquei por -1 para não confundir com inversão do fluxo de potência ####
                    W_fase_A_sec=0
                    W_fase_B_sec=potencias_tr[4]*1000*(-1)
                    W_fase_C_sec=0
                    W_tot_tr_sec=W_fase_A_sec+W_fase_B_sec+W_fase_C_sec
                    
                    #### Dados do Terciário####
                    V_fase_A_ter= 0
                    V_fase_B_ter= 0
                    V_fase_C_ter= V_voltages_tr[10]
                    Vpu_fase_A_ter=0
                    Vpu_fase_B_ter=0
                    Vpu_fase_C_ter=V_fase_C_ter/(kv_secundario*1000)
                    Amps_fase_A_ter= 0
                    Amps_fase_B_ter= 0
                    Amps_fase_C_ter= correntes_tr[10]
                    VA_fase_A_ter=0
                    VA_fase_B_ter=0
                    VA_fase_C_ter=V_fase_C_ter*Amps_fase_C_ter
                    VA_tot_tr_ter=VA_fase_A_ter+VA_fase_B_ter+VA_fase_C_ter
                    #### OpenDSS entende que o que entra no terminal é positivo e o que sai do terminal é negativo, por isso multipiquei por -1 para não confundir com inversão do fluxo de potência ####
                    W_fase_A_ter=0
                    W_fase_B_ter=0
                    W_fase_C_ter=potencias_tr[10]*1000*(-1)
                    W_tot_tr_ter=W_fase_A_ter+W_fase_B_ter+W_fase_C_ter
                    
                ###############################################################################        
                #### Transformadores Monofásicos A TRÊS FIOS Ligados Fase CA NO LADO DE BT ####
                ###############################################################################
                if nodes_phases_tr[2]==3 and nodes_phases_tr[5]==1:
                    V_fase_A_sec= 0
                    V_fase_B_sec= 0
                    V_fase_C_sec= V_voltages_tr[4]
                    Vpu_fase_A_sec=0
                    Vpu_fase_B_sec=0
                    Vpu_fase_C_sec=V_fase_C_sec/(kv_secundario*1000)
                    Amps_fase_A_sec= 0
                    Amps_fase_B_sec= 0
                    Amps_fase_C_sec= correntes_tr[4]
                    VA_fase_A_sec=0
                    VA_fase_B_sec=0
                    VA_fase_C_sec=V_fase_C_sec*Amps_fase_C_sec
                    VA_tot_tr_sec=VA_fase_A_sec+VA_fase_B_sec+VA_fase_C_sec
                    #### OpenDSS entende que o que entra no terminal é positivo e o que sai do terminal é negativo, por isso multipiquei por -1 para não confundir com inversão do fluxo de potência ####
                    W_fase_A_sec=0
                    W_fase_B_sec=0
                    W_fase_C_sec=potencias_tr[4]*1000*(-1)
                    W_tot_tr_sec=W_fase_A_sec+W_fase_B_sec+W_fase_C_sec
                    
                    #### Dados do Terciário####
                    V_fase_A_ter= V_voltages_tr[10]
                    V_fase_B_ter= 0
                    V_fase_C_ter= 0
                    Vpu_fase_A_ter=V_fase_A_ter/(kv_secundario*1000)
                    Vpu_fase_B_ter=0
                    Vpu_fase_C_ter=0
                    Amps_fase_A_ter= correntes_tr[10]
                    Amps_fase_B_ter= 0
                    Amps_fase_C_ter= 0
                    VA_fase_A_ter=V_fase_A_ter*Amps_fase_A_ter
                    VA_fase_B_ter=0
                    VA_fase_C_ter=0
                    VA_tot_tr_ter=VA_fase_A_ter+VA_fase_B_ter+VA_fase_C_ter
                    #### OpenDSS entende que o que entra no terminal é positivo e o que sai do terminal é negativo, por isso multipiquei por -1 para não confundir com inversão do fluxo de potência ####
                    W_fase_A_ter=potencias_tr[10]*1000*(-1)
                    W_fase_B_ter=0
                    W_fase_C_ter=0
                    W_tot_tr_ter=W_fase_A_ter+W_fase_B_ter+W_fase_C_ter
            else:
                V_fase_A_ter=0
                V_fase_B_ter=0
                V_fase_C_ter=0
                Vpu_fase_A_ter=0
                Vpu_fase_B_ter=0
                Vpu_fase_C_ter=0
                Amps_fase_A_ter=0
                Amps_fase_B_ter=0
                Amps_fase_C_ter=0
                VA_fase_A_ter=0
                VA_fase_B_ter=0
                VA_fase_C_ter=0
                VA_tot_tr_ter=0
                W_fase_A_ter=0
                W_fase_B_ter=0
                W_fase_C_ter=0
                W_tot_tr_ter=0
            
            #### Cria o dicionário da linha atual para acrescentar na lista dados_tabela_tr ####
            linha_atual_tr={
                "hora_tr": hora_tr,
                "transformador_id": transformador_id,
                "kVA_nom_tr": kVA_nom_tr,
                "corrente_nom_tr": corrente_nom_tr,
                "corrente_emerg_tr": corrente_emerg_tr,
                "qtde_enrolamentos_tr": qtde_enrolamentos_tr,
                "kv_primario": kv_primario,
                "kv_secundario": kv_secundario,
                "kv_terciario": kv_terciario,
                "phases_tr": phases_tr,
                "barra_primaria_tr": barra_primaria_tr,
                "barra_secundaria_tr": barra_secundaria_tr,
                "barra_terciaria_tr": barra_terciaria_tr,
                "V_fase_A_pri": V_fase_A_pri,
                "V_fase_B_pri": V_fase_B_pri,
                "V_fase_C_pri": V_fase_C_pri,
                "Vpu_fase_A_pri": Vpu_fase_A_pri,
                "Vpu_fase_B_pri": Vpu_fase_B_pri,
                "Vpu_fase_C_pri": Vpu_fase_C_pri,
                "Amps_fase_A_pri": Amps_fase_A_pri,
                "Amps_fase_B_pri": Amps_fase_B_pri,
                "Amps_fase_C_pri": Amps_fase_C_pri,
                "VA_fase_A_pri": VA_fase_A_pri,
                "VA_fase_B_pri": VA_fase_B_pri,
                "VA_fase_C_pri": VA_fase_C_pri,
                "VA_tot_tr_pri": VA_tot_tr_pri,
                "W_fase_A_pri": W_fase_A_pri,
                "W_fase_B_pri": W_fase_B_pri,
                "W_fase_C_pri": W_fase_C_pri,
                "W_tot_tr_pri": W_tot_tr_pri,
                "V_fase_A_sec": V_fase_A_sec,
                "V_fase_B_sec": V_fase_B_sec,
                "V_fase_C_sec": V_fase_C_sec,
                "Vpu_fase_A_sec": Vpu_fase_A_sec,
                "Vpu_fase_B_sec": Vpu_fase_B_sec,
                "Vpu_fase_C_sec": Vpu_fase_C_sec,
                "Amps_fase_A_sec": Amps_fase_A_sec,
                "Amps_fase_B_sec": Amps_fase_B_sec,
                "Amps_fase_C_sec": Amps_fase_C_sec,
                "VA_fase_A_sec": VA_fase_A_sec,
                "VA_fase_B_sec": VA_fase_B_sec,
                "VA_fase_C_sec": VA_fase_C_sec,
                "VA_tot_tr_sec": VA_tot_tr_sec,
                "W_fase_A_sec": W_fase_A_sec,
                "W_fase_B_sec": W_fase_B_sec,
                "W_fase_C_sec": W_fase_C_sec,
                "W_tot_tr_sec": W_tot_tr_sec,
                "V_fase_A_ter": V_fase_A_ter,
                "V_fase_B_ter": V_fase_B_ter,
                "V_fase_C_ter": V_fase_C_ter,
                "Vpu_fase_A_ter": Vpu_fase_A_ter,
                "Vpu_fase_B_ter": Vpu_fase_B_ter,
                "Vpu_fase_C_ter": Vpu_fase_C_ter,
                "Amps_fase_A_ter": Amps_fase_A_ter,
                "Amps_fase_B_ter": Amps_fase_B_ter,
                "Amps_fase_C_ter": Amps_fase_C_ter,
                "VA_fase_A_ter": VA_fase_A_ter,
                "VA_fase_B_ter": VA_fase_B_ter,
                "VA_fase_C_ter": VA_fase_C_ter,
                "VA_tot_tr_ter": VA_tot_tr_ter,
                "W_fase_A_ter": W_fase_A_ter,
                "W_fase_B_ter": W_fase_B_ter,
                "W_fase_C_ter": W_fase_C_ter,
                "W_tot_tr_ter": W_tot_tr_ter,
                "cond_ope_tr": cond_ope_tr,
            }
            #### Acrescenta os dados da linha atual como dicionário na lista  linha_atual_tr, então  linha_atual_tr será uma lista de dicionários ####
            dados_tabela_tr.append( linha_atual_tr)
            ##print(f"{dados_tabela_tr}")
            
            ####Passa para o próximo transformador e conta####
            cont_transformadores=cont_transformadores+1
            dss.transformers.next()
            
        ####Passa para a próxima hora e roda novamente para todos os transforamdores####                    
        conta_hora_tr=conta_hora_tr+param_step_size
else:
    print("Arquivo dss da rede não encontrado!")

df = pd.DataFrame(dados_tabela_tr)
df.to_csv(
    f"dados_tabela_tr{dss.circuit.name}.csv",
    sep=";",          # separador ponto e vírgula
    decimal=",",      # separador decimal vírgula
    index=False,
    encoding="utf-8-sig"
)
print("FINALIZADO!")