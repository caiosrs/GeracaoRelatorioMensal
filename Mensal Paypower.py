import tkinter as tk
from tkinter import ttk
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import pyautogui
import time

def validate_month(P):
    if P.isdigit():
        if 0 < int(P) <= 12:
            return True
    return False

def get_selected_date():
    month = month_var.get().zfill(2)
    year = year_var.get()
    cpf_value = cpf_entry.get()
    senha_value = senha_entry.get()
    empresa_num = empresa_num_var.get()  
    filial_num = filial_num_var.get() 
    data_competencia = f"{month}-{year}"
    print("Data selecionada:", data_competencia)
    chrome(data_competencia, empresa_num, filial_num, cpf_value, senha_value)
    root.destroy()

def chrome(data_competencia, empresa_num, filial_num, cpf_value, senha_value):
    
    driver = webdriver.Chrome()

    url = "https://dpcontrole.informatecservicos.com.br/Acesso/Acesso.aspx?ReturnUrl=%2fAdministrador%2fHome.aspx"
    driver.get(url)

    # LOGIN DPCONTROLE
    cpf_dpcontrole = driver.find_element(By.ID, 'txtCPF')
    cpf_dpcontrole.send_keys(cpf_value)

    senha_dpcontrole = driver.find_element(By.ID, 'txtSenha')
    senha_dpcontrole.send_keys(senha_value)
    btn_entrar = driver.find_element(By.NAME, 'btnEntrar')

    btn_entrar.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'lnkPaypower')))

    # ACESSANDO PAYPOWER

    lkn_paypower = driver.find_element(By.ID,'lnkPaypower')
    lkn_paypower.click()
    time.sleep(2)

    #ESCOLHENDO A EMPRESA/FILIAL

    pyautogui.press('tab')
    pyautogui.write(empresa_num)
    pyautogui.press('enter')
    if filial_num is None:
        pass
    else:
        pyautogui.write(filial_num)
    
    pyautogui.press('enter')
    time.sleep(2)

    def acessar_ultima_guia_aberta():
        ultima_guia = driver.window_handles[-1]
        driver.switch_to.window(ultima_guia)
        driver.execute_script("window.location.href = 'https://www.paypower.com.br/folha/sistema/relatorios/fichaconsolidada/filtro.asp'")
        
        # FUNÇÕES

    nome_arquivo_mensal = "Mensal"
    nome_arquivo_rescisaoc = "Rescisão Complementar"
    nome_arquivo_adiantamento13 = "Adiantamento de 13º Salário"
    nome_arquivo_13salario = "13º Salário"
    nome_arquivo_plr = "Participação nos Lucros"

    def aceitar_popup_se_existir():
        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            popup = Alert(driver)
            popup.accept()
            return True
        except TimeoutException:
            return False

    def acessar_guia_com_prefixo(url_prefixo):
        # Itera sobre as janelas
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            # Verifica se o URL da guia atual começa com o prefixo desejado
            if driver.current_url.startswith(url_prefixo):
                return True
        return False

    def imprimir_relatorio_pdf(nome_arquivo):
        # Configura opções do Chrome para habilitar a impressão em modo kiosk (tela cheia)
        chrome_options = Options()
        chrome_options.add_argument("--kiosk-printing")

        pyautogui.hotkey('ctrl','p')
        time.sleep(3)
        #WebDriverWait(driver, 5).until(EC.url_to_be("https://www.paypower.com.br/folha/sistema/relatorios/fichaconsolidada/filtro.asp"))

        #pyautogui.click(x=1032, y=647)
        pyautogui.press('enter')
        time.sleep(2)

        pyautogui.write(nome_arquivo)
        pyautogui.press('enter')

        time.sleep(2)

    def pos_preenchimento(nome_arquivo):    
        if aceitar_popup_se_existir():
            return
        else:
            url_prefixo = 'https://www.paypower.com.br/folha/util/showrelatorio.asp'
            if acessar_guia_com_prefixo(url_prefixo):
                imprimir_relatorio_pdf(nome_arquivo)
            else:
                print("Erro ao acessar o relatório.")

    # PREENCHENDO DADOS |Mensal

    def relatorio_mensal_geral(data_competencia):
        acessar_ultima_guia_aberta()
        preencher_competencia = driver.find_element(By.ID, 'COMPETENCIA')
        preencher_competencia.send_keys(data_competencia)

        dropdown_rotina = driver.find_element(By.ID, 'CODROTINA')
        select_rotina = Select(dropdown_rotina)
        select_rotina.select_by_visible_text('Mensal')

        #CLICK VALUE='S'
        rBtn_centro_custo = driver.find_element(By.XPATH, '//*[@id="AGRUPARCCUSTOS"]')
        rBtn_centro_custo.click()

        #CLICK VALUE='S'
        rBtn_filial = driver.find_element(By.XPATH, '//*[@id="AGRUPARFILIALS"]')
        rBtn_filial.click()
        rBtn_filial.send_keys(Keys.ENTER)

        nome_arquivo = f"{data_competencia}_{nome_arquivo_mensal}_Geral"
        pos_preenchimento(nome_arquivo)

    def relatorio_mensal_centro_custo(data_competencia):
        acessar_ultima_guia_aberta()
        preencher_competencia = driver.find_element(By.ID, 'COMPETENCIA')
        preencher_competencia.send_keys(data_competencia)

        dropdown_rotina = driver.find_element(By.ID, 'CODROTINA')
        select_rotina = Select(dropdown_rotina)
        select_rotina.select_by_visible_text('Mensal')

        #CLICK VALUE='N'
        rBtn_filial = driver.find_element(By.XPATH, '//*[@id="AGRUPARFILIALN"]')
        rBtn_filial.click()
        rBtn_filial.send_keys(Keys.ENTER)

        nome_arquivo = f"{data_competencia}_{nome_arquivo_mensal}_CC"
        pos_preenchimento(nome_arquivo)

    def relatorio_mensal_filial(data_competencia):
        acessar_ultima_guia_aberta()
        preencher_competencia = driver.find_element(By.ID, 'COMPETENCIA')
        preencher_competencia.send_keys(data_competencia)

        dropdown_rotina = driver.find_element(By.ID, 'CODROTINA')
        select_rotina = Select(dropdown_rotina)
        select_rotina.select_by_visible_text('Mensal')

        #CLICK VALUE='N'
        rBtn_centro_custo = driver.find_element(By.XPATH, '//*[@id="AGRUPARCCUSTON"]')
        rBtn_centro_custo.click()

        #CLICK VALUE='S'
        rBtn_filial = driver.find_element(By.XPATH, '//*[@id="AGRUPARFILIALS"]')
        rBtn_filial.click()
        rBtn_filial.send_keys(Keys.ENTER)

        nome_arquivo = f"{data_competencia}_{nome_arquivo_mensal}_Filial"
        pos_preenchimento(nome_arquivo)

    def relatorio_mensal_vazio(data_competencia):
        acessar_ultima_guia_aberta()
        preencher_competencia = driver.find_element(By.ID, 'COMPETENCIA')
        preencher_competencia.send_keys(data_competencia)

        dropdown_rotina = driver.find_element(By.ID, 'CODROTINA')
        select_rotina = Select(dropdown_rotina)
        select_rotina.select_by_visible_text('Mensal')

        #CLICK VALUE='N'
        rBtn_centro_custo = driver.find_element(By.XPATH, '//*[@id="AGRUPARCCUSTON"]')
        rBtn_centro_custo.click()

        #CLICK VALUE='N'
        rBtn_filial = driver.find_element(By.XPATH, '//*[@id="AGRUPARFILIALN"]')
        rBtn_filial.click()
        rBtn_filial.send_keys(Keys.ENTER)

        nome_arquivo = f"{data_competencia}_{nome_arquivo_mensal}_Vazio"
        pos_preenchimento(nome_arquivo)

    time.sleep(3)
    relatorio_mensal_geral(data_competencia)
    time.sleep(3)
    relatorio_mensal_centro_custo(data_competencia)
    time.sleep(3)
    relatorio_mensal_filial(data_competencia)
    time.sleep(3)
    relatorio_mensal_vazio(data_competencia)

    def relatorio_rescisao_complementar_geral(data_competencia):
        acessar_ultima_guia_aberta()
        preencher_competencia = driver.find_element(By.ID, 'COMPETENCIA')
        preencher_competencia.send_keys(data_competencia)

        dropdown_rotina = driver.find_element(By.ID, 'CODROTINA')
        select_rotina = Select(dropdown_rotina)
        select_rotina.select_by_visible_text('Rescisão Complementar')

        #CLICK VALUE='S'
        rBtn_centro_custo = driver.find_element(By.XPATH, '//*[@id="AGRUPARCCUSTOS"]')
        rBtn_centro_custo.click()

        #CLICK VALUE='S'
        rBtn_filial = driver.find_element(By.XPATH, '//*[@id="AGRUPARFILIALS"]')
        rBtn_filial.click()
        rBtn_filial.send_keys(Keys.ENTER)

        nome_arquivo = f"{data_competencia}_{nome_arquivo_rescisaoc}_Geral"
        pos_preenchimento(nome_arquivo)

    def relatorio_rescisao_complementar_centro_custo(data_competencia):
        acessar_ultima_guia_aberta()
        preencher_competencia = driver.find_element(By.ID, 'COMPETENCIA')
        preencher_competencia.send_keys(data_competencia)

        dropdown_rotina = driver.find_element(By.ID, 'CODROTINA')
        select_rotina = Select(dropdown_rotina)
        select_rotina.select_by_visible_text('Rescisão Complementar')

        #CLICK VALUE='N'
        rBtn_filial = driver.find_element(By.XPATH, '//*[@id="AGRUPARFILIALN"]')
        rBtn_filial.click()
        rBtn_filial.send_keys(Keys.ENTER)

        nome_arquivo = f"{data_competencia}_{nome_arquivo_rescisaoc}_CC"
        pos_preenchimento(nome_arquivo)

    def relatorio_rescisao_complementar_filial(data_competencia):
        acessar_ultima_guia_aberta()
        preencher_competencia = driver.find_element(By.ID, 'COMPETENCIA')
        preencher_competencia.send_keys(data_competencia)

        dropdown_rotina = driver.find_element(By.ID, 'CODROTINA')
        select_rotina = Select(dropdown_rotina)
        select_rotina.select_by_visible_text('Rescisão Complementar')

        #CLICK VALUE='N'
        rBtn_centro_custo = driver.find_element(By.XPATH, '//*[@id="AGRUPARCCUSTON"]')
        rBtn_centro_custo.click()

        #CLICK VALUE='S'
        rBtn_filial = driver.find_element(By.XPATH, '//*[@id="AGRUPARFILIALS"]')
        rBtn_filial.click()
        rBtn_filial.send_keys(Keys.ENTER)

        nome_arquivo = f"{data_competencia}_{nome_arquivo_rescisaoc}_Filial"
        pos_preenchimento(nome_arquivo)

    def relatorio_rescisao_complementar_vazio(data_competencia):
        acessar_ultima_guia_aberta()
        preencher_competencia = driver.find_element(By.ID, 'COMPETENCIA')
        preencher_competencia.send_keys(data_competencia)

        dropdown_rotina = driver.find_element(By.ID, 'CODROTINA')
        select_rotina = Select(dropdown_rotina)
        select_rotina.select_by_visible_text('Rescisão Complementar')

        #CLICK VALUE='N'
        rBtn_centro_custo = driver.find_element(By.XPATH, '//*[@id="AGRUPARCCUSTON"]')
        rBtn_centro_custo.click()

        #CLICK VALUE='N'
        rBtn_filial = driver.find_element(By.XPATH, '//*[@id="AGRUPARFILIALN"]')
        rBtn_filial.click()
        rBtn_filial.send_keys(Keys.ENTER)

        nome_arquivo = f"{data_competencia}_{nome_arquivo_rescisaoc}_Vazio"
        pos_preenchimento(nome_arquivo)

    relatorio_rescisao_complementar_geral(data_competencia)
    relatorio_rescisao_complementar_centro_custo(data_competencia)
    relatorio_rescisao_complementar_filial(data_competencia)
    relatorio_rescisao_complementar_vazio(data_competencia)

    # PREENCHENDO DADOS |Adiantamento de 13º Salário

    def relatorio_adiamento13_geral(data_competencia):
        acessar_ultima_guia_aberta()
        preencher_competencia = driver.find_element(By.ID, 'COMPETENCIA')
        preencher_competencia.send_keys(data_competencia)

        dropdown_rotina = driver.find_element(By.ID, 'CODROTINA')
        select_rotina = Select(dropdown_rotina)
        select_rotina.select_by_visible_text('Adiantamento de 13º Salário')

        #CLICK VALUE='S'
        rBtn_centro_custo = driver.find_element(By.XPATH, '//*[@id="AGRUPARCCUSTOS"]')
        rBtn_centro_custo.click()

        #CLICK VALUE='S'
        rBtn_filial = driver.find_element(By.XPATH, '//*[@id="AGRUPARFILIALS"]')
        rBtn_filial.click()
        rBtn_filial.send_keys(Keys.ENTER)

        nome_arquivo = f"{data_competencia}_{nome_arquivo_adiantamento13}_Geral"
        pos_preenchimento(nome_arquivo)

    def relatorio_adiamento13_centro_custo(data_competencia):
        acessar_ultima_guia_aberta()
        preencher_competencia = driver.find_element(By.ID, 'COMPETENCIA')
        preencher_competencia.send_keys(data_competencia)

        dropdown_rotina = driver.find_element(By.ID, 'CODROTINA')
        select_rotina = Select(dropdown_rotina)
        select_rotina.select_by_visible_text('Adiantamento de 13º Salário')

        #CLICK VALUE='N'
        rBtn_filial = driver.find_element(By.XPATH, '//*[@id="AGRUPARFILIALN"]')
        rBtn_filial.click()
        rBtn_filial.send_keys(Keys.ENTER)

        nome_arquivo = f"{data_competencia}_{nome_arquivo_adiantamento13}_CC"
        pos_preenchimento(nome_arquivo)

    def relatorio_adiamento13_filial(data_competencia):
        acessar_ultima_guia_aberta()
        preencher_competencia = driver.find_element(By.ID, 'COMPETENCIA')
        preencher_competencia.send_keys(data_competencia)

        dropdown_rotina = driver.find_element(By.ID, 'CODROTINA')
        select_rotina = Select(dropdown_rotina)
        select_rotina.select_by_visible_text('Adiantamento de 13º Salário')

        #CLICK VALUE='N'
        rBtn_centro_custo = driver.find_element(By.XPATH, '//*[@id="AGRUPARCCUSTON"]')
        rBtn_centro_custo.click()

        #CLICK VALUE='S'
        rBtn_filial = driver.find_element(By.XPATH, '//*[@id="AGRUPARFILIALS"]')
        rBtn_filial.click()
        rBtn_filial.send_keys(Keys.ENTER)

        nome_arquivo = f"{data_competencia}_{nome_arquivo_adiantamento13}_Filial"
        pos_preenchimento(nome_arquivo)

    def relatorio_adiamento13_vazio(data_competencia):
        acessar_ultima_guia_aberta()
        preencher_competencia = driver.find_element(By.ID, 'COMPETENCIA')
        preencher_competencia.send_keys(data_competencia)

        dropdown_rotina = driver.find_element(By.ID, 'CODROTINA')
        select_rotina = Select(dropdown_rotina)
        select_rotina.select_by_visible_text('Adiantamento de 13º Salário')

        #CLICK VALUE='N'
        rBtn_centro_custo = driver.find_element(By.XPATH, '//*[@id="AGRUPARCCUSTON"]')
        rBtn_centro_custo.click()

        #CLICK VALUE='N'
        rBtn_filial = driver.find_element(By.XPATH, '//*[@id="AGRUPARFILIALN"]')
        rBtn_filial.click()
        rBtn_filial.send_keys(Keys.ENTER)

        nome_arquivo = f"{data_competencia}_{nome_arquivo_adiantamento13}_Vazio"
        pos_preenchimento(nome_arquivo)

    relatorio_adiamento13_geral(data_competencia)
    relatorio_adiamento13_centro_custo(data_competencia)
    relatorio_adiamento13_filial(data_competencia)
    relatorio_adiamento13_vazio(data_competencia)

    def relatorio_13salario_geral(data_competencia):
        acessar_ultima_guia_aberta()
        preencher_competencia = driver.find_element(By.ID, 'COMPETENCIA')
        preencher_competencia.send_keys(data_competencia)

        dropdown_rotina = driver.find_element(By.ID, 'CODROTINA')
        select_rotina = Select(dropdown_rotina)
        select_rotina.select_by_visible_text('13º Salário')

        #CLICK VALUE='S'
        rBtn_centro_custo = driver.find_element(By.XPATH, '//*[@id="AGRUPARCCUSTOS"]')
        rBtn_centro_custo.click()

        #CLICK VALUE='S'
        rBtn_filial = driver.find_element(By.XPATH, '//*[@id="AGRUPARFILIALS"]')
        rBtn_filial.click()
        rBtn_filial.send_keys(Keys.ENTER)

        nome_arquivo = f"{data_competencia}_{nome_arquivo_13salario}_Geral"
        pos_preenchimento(nome_arquivo)

    def relatorio_13salario_centro_custo(data_competencia):
        acessar_ultima_guia_aberta()
        preencher_competencia = driver.find_element(By.ID, 'COMPETENCIA')
        preencher_competencia.send_keys(data_competencia)

        dropdown_rotina = driver.find_element(By.ID, 'CODROTINA')
        select_rotina = Select(dropdown_rotina)
        select_rotina.select_by_visible_text('13º Salário')

        #CLICK VALUE='N'
        rBtn_filial = driver.find_element(By.XPATH, '//*[@id="AGRUPARFILIALN"]')
        rBtn_filial.click()
        rBtn_filial.send_keys(Keys.ENTER)

        nome_arquivo = f"{data_competencia}_{nome_arquivo_13salario}_CC"
        pos_preenchimento(nome_arquivo)

    def relatorio_13salario_filial(data_competencia):
        acessar_ultima_guia_aberta()
        preencher_competencia = driver.find_element(By.ID, 'COMPETENCIA')
        preencher_competencia.send_keys(data_competencia)

        dropdown_rotina = driver.find_element(By.ID, 'CODROTINA')
        select_rotina = Select(dropdown_rotina)
        select_rotina.select_by_visible_text('13º Salário')

        #CLICK VALUE='N'
        rBtn_centro_custo = driver.find_element(By.XPATH, '//*[@id="AGRUPARCCUSTON"]')
        rBtn_centro_custo.click()

        #CLICK VALUE='S'
        rBtn_filial = driver.find_element(By.XPATH, '//*[@id="AGRUPARFILIALS"]')
        rBtn_filial.click()
        rBtn_filial.send_keys(Keys.ENTER)

        nome_arquivo = f"{data_competencia}_{nome_arquivo_13salario}_Filial"
        pos_preenchimento(nome_arquivo)

    def relatorio_13salario_vazio(data_competencia):
        acessar_ultima_guia_aberta()
        preencher_competencia = driver.find_element(By.ID, 'COMPETENCIA')
        preencher_competencia.send_keys(data_competencia)

        dropdown_rotina = driver.find_element(By.ID, 'CODROTINA')
        select_rotina = Select(dropdown_rotina)
        select_rotina.select_by_visible_text('13º Salário')

        #CLICK VALUE='N'
        rBtn_centro_custo = driver.find_element(By.XPATH, '//*[@id="AGRUPARCCUSTON"]')
        rBtn_centro_custo.click()

        #CLICK VALUE='N'
        rBtn_filial = driver.find_element(By.XPATH, '//*[@id="AGRUPARFILIALN"]')
        rBtn_filial.click()
        rBtn_filial.send_keys(Keys.ENTER)

        nome_arquivo = f"{data_competencia}_{nome_arquivo_13salario}_Vazio"
        pos_preenchimento(nome_arquivo)

    relatorio_13salario_geral(data_competencia)
    relatorio_13salario_centro_custo(data_competencia)
    relatorio_13salario_filial(data_competencia)
    relatorio_13salario_vazio(data_competencia)

    def relatorio_plr_geral(data_competencia):
        acessar_ultima_guia_aberta()
        preencher_competencia = driver.find_element(By.ID, 'COMPETENCIA')
        preencher_competencia.send_keys(data_competencia)

        dropdown_rotina = driver.find_element(By.ID, 'CODROTINA')
        select_rotina = Select(dropdown_rotina)
        select_rotina.select_by_visible_text('Participação nos Lucros')

        #CLICK VALUE='S'
        rBtn_centro_custo = driver.find_element(By.XPATH, '//*[@id="AGRUPARCCUSTOS"]')
        rBtn_centro_custo.click()

        #CLICK VALUE='S'
        rBtn_filial = driver.find_element(By.XPATH, '//*[@id="AGRUPARFILIALS"]')
        rBtn_filial.click()
        rBtn_filial.send_keys(Keys.ENTER)

        nome_arquivo = f"{data_competencia}_{nome_arquivo_plr}_Geral"
        pos_preenchimento(nome_arquivo)

    def relatorio_plr_centro_custo(data_competencia):
        acessar_ultima_guia_aberta()
        preencher_competencia = driver.find_element(By.ID, 'COMPETENCIA')
        preencher_competencia.send_keys(data_competencia)

        dropdown_rotina = driver.find_element(By.ID, 'CODROTINA')
        select_rotina = Select(dropdown_rotina)
        select_rotina.select_by_visible_text('Participação nos Lucros')

        #CLICK VALUE='N'
        rBtn_filial = driver.find_element(By.XPATH, '//*[@id="AGRUPARFILIALN"]')
        rBtn_filial.click()
        rBtn_filial.send_keys(Keys.ENTER)

        nome_arquivo = f"{data_competencia}_{nome_arquivo_plr}_CC"
        pos_preenchimento(nome_arquivo)

    def relatorio_plr_filial(data_competencia):
        acessar_ultima_guia_aberta()
        preencher_competencia = driver.find_element(By.ID, 'COMPETENCIA')
        preencher_competencia.send_keys(data_competencia)

        dropdown_rotina = driver.find_element(By.ID, 'CODROTINA')
        select_rotina = Select(dropdown_rotina)
        select_rotina.select_by_visible_text('Participação nos Lucros')

        #CLICK VALUE='N'
        rBtn_centro_custo = driver.find_element(By.XPATH, '//*[@id="AGRUPARCCUSTON"]')
        rBtn_centro_custo.click()

        #CLICK VALUE='S'
        rBtn_filial = driver.find_element(By.XPATH, '//*[@id="AGRUPARFILIALS"]')
        rBtn_filial.click()
        rBtn_filial.send_keys(Keys.ENTER)

        nome_arquivo = f"{data_competencia}_{nome_arquivo_plr}_Filial"
        pos_preenchimento(nome_arquivo)

    def relatorio_plr_vazio(data_competencia):
        acessar_ultima_guia_aberta()
        preencher_competencia = driver.find_element(By.ID, 'COMPETENCIA')
        preencher_competencia.send_keys(data_competencia)

        dropdown_rotina = driver.find_element(By.ID, 'CODROTINA')
        select_rotina = Select(dropdown_rotina)
        select_rotina.select_by_visible_text('Participação nos Lucros')

        #CLICK VALUE='N'
        rBtn_centro_custo = driver.find_element(By.XPATH, '//*[@id="AGRUPARCCUSTON"]')
        rBtn_centro_custo.click()

        #CLICK VALUE='N'
        rBtn_filial = driver.find_element(By.XPATH, '//*[@id="AGRUPARFILIALN"]')
        rBtn_filial.click()
        rBtn_filial.send_keys(Keys.ENTER)

        nome_arquivo = f"{data_competencia}_{nome_arquivo_plr}_Vazio"
        pos_preenchimento(nome_arquivo)

    relatorio_plr_geral(data_competencia)
    relatorio_plr_centro_custo(data_competencia)
    relatorio_plr_filial(data_competencia)
    relatorio_plr_vazio(data_competencia)

    driver.quit()

root = tk.Tk()
root.title("Relatório Paypower")

# Label central para "LOGIN"
label_login = tk.Label(root, text="LOGIN", font=("Helvetica", 16))
label_login.grid(row=0, column=0, columnspan=2, pady=10)

# Label e campo para CPF
label_cpf = tk.Label(root, text="CPF:")
label_cpf.grid(row=1, column=0, padx=5, pady=5, sticky="e")

cpf_entry = tk.StringVar()
cpf_entry = ttk.Entry(root, width=20, textvariable=cpf_entry)
cpf_entry.grid(row=1, column=1, padx=5, pady=5)

# Label e campo para senha
label_senha = tk.Label(root, text="Senha:")
label_senha.grid(row=2, column=0, padx=5, pady=5, sticky="e")

senha_entry = tk.StringVar()
senha_entry = ttk.Entry(root, show="*", width=20, textvariable=senha_entry)
senha_entry.grid(row=2, column=1, padx=5, pady=5)

label = tk.Label(root, text="Selecione o mês e o ano:")
label.grid(row=3, column=0, columnspan=2, pady=5)

month_var = tk.StringVar()
year_var = tk.StringVar()

validate_month_cmd = root.register(validate_month)

month_entry = ttk.Entry(root, textvariable=month_var, width=4, validate="key")
month_entry.grid(row=4, column=0, padx=5, pady=5)

year_entry = ttk.Entry(root, textvariable=year_var, width=7, validate="key")
year_entry.grid(row=4, column=1, padx=5, pady=5)

label_empresa = tk.Label(root, text="Digite os 4 digitos da EMPRESA")
label_empresa.grid(row=5, column=0, padx=5, pady=5)
empresa_num_var = tk.StringVar()

label_filial = tk.Label(root, text="Digite os 4 digitos da FILIAL")
label_filial.grid(row=5, column=1, padx=5, pady=5)
filial_num_var = tk.StringVar()

empresa_num_entry = ttk.Entry(root, textvariable=empresa_num_var, width=7, validate="key")
empresa_num_entry.grid(row=6, column=0, padx=5, pady=5)

filial_num_entry = ttk.Entry(root, textvariable=filial_num_var, width=7, validate="key")
filial_num_entry.grid(row=6, column=1, padx=5, pady=5)

btn_select = ttk.Button(root, text="Selecionar Data", command=get_selected_date)
btn_select.grid(row=7, column=0, columnspan=2, pady=5)

root.mainloop()