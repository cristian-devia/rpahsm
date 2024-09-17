# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

class LoginManager:
    def __init__(self):
        self.driver = None

    def slow_type(self, element, text, delay=0.1):
        for character in text:
            try:
                element.send_keys(character)
                time.sleep(delay)
            except Exception as e:
                print(f"Error enviando el carácter '{character}': {e}")

    def login(self, url, username, password, campaign, hsm_name, params_count, message, parametros, is_hsm, is_auto_managed, awaiting_input):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--ignore-ssl-errors')
            options.add_argument('--allow-insecure-localhost')
            options.add_argument('--disable-web-security')
            options.add_argument('--allow-running-insecure-content')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')

            service = Service(executable_path='C:\\Users\\crideves\\Documents\\chromedriver.exe')
            self.driver = webdriver.Chrome(service=service, options=options)
            
            self.driver.get(url)
            print("Navegador abierto y URL cargada.")

            username_field = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="username"]')))
            self.slow_type(username_field, username)
            print("Nombre de usuario ingresado.")

            password_field = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="passerw"]')))
            self.slow_type(password_field, password)
            print("Contraseña ingresada.")

            password_field.send_keys(Keys.RETURN)

            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="SelectEnterprise_select_enterprise_id"]')))
            print("Página de selección de campaña cargada.")

            company_dropdown = self.driver.find_element(By.XPATH, '//*[@id="SelectEnterprise_select_enterprise_id"]')
            company_dropdown.click()
            company_dropdown.send_keys(Keys.TAB)

            current_selected_option = None
            while True:
                selected_option = self.driver.execute_script("return arguments[0].options[arguments[0].selectedIndex].text;", company_dropdown)
                print(f"Opción seleccionada: {selected_option}")

                if selected_option.strip() == campaign:
                    break

                if selected_option != current_selected_option:
                    current_selected_option = selected_option
                    company_dropdown.send_keys(Keys.ARROW_DOWN)
                    time.sleep(0.5)

            ingresar_button = self.driver.find_element(By.XPATH, '//*[@id="doLogin_button"]')
            ingresar_button.click()
            print("Botón de ingresar clickeado.")

            time.sleep(4)
            print("Esperando 4 segundos antes de redirigir...")

            hsm_config_url = "https://cari.ai/campaign/hsmConfigGupshup"
            self.driver.execute_script(f"window.open('{hsm_config_url}', '_blank');")
            print("Redirigiendo a la página de Configurar HSM Gupshup en una nueva pestaña.")

            self.driver.switch_to.window(self.driver.window_handles[-1])
            print("Cambio de enfoque a la nueva pestaña.")

            WebDriverWait(self.driver, 30).until(EC.url_contains("hsmConfigGupshup"))
            print("Redirección exitosa.")

            new_button = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="new__button"]/i[2]')))
            new_button.click()
            print("Botón '+' clickeado.")

            time.sleep(5)

            nombre_field = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="HSMConfigGupshup_name"]')))
            self.slow_type(nombre_field, hsm_name)

            element_name_field = self.driver.find_element(By.XPATH, '//*[@id="HSMConfigGupshup_elementName"]')
            self.slow_type(element_name_field, hsm_name)

            categoria_field = self.driver.find_element(By.XPATH, '//*[@id="select2-HSMConfigGupshup_whatsapp_category_new-container"]')
            categoria_field.click()
            categoria_options = self.driver.find_elements(By.XPATH, '//*[@id="select2-HSMConfigGupshup_whatsapp_category_new-results"]/li')
            for option in categoria_options:
                if option.text == "MARKETING":
                    option.click()
                    break

            idioma_field = self.driver.find_element(By.XPATH, '//*[@id="select2-HSMConfigGupshup_language-container"]')
            idioma_field.click()
            idioma_options = self.driver.find_elements(By.XPATH, '//*[@id="select2-HSMConfigGupshup_language-results"]/li')
            for option in idioma_options:
                if option.text == "Español Neutro":
                    option.click()
                    break

            is_hsm_field = self.driver.find_element(By.XPATH, '//*[@id="select2-HSMConfigGupshup_is_hsm-container"]')
            is_hsm_field.click()
            is_hsm_options = self.driver.find_elements(By.XPATH, '//*[@id="select2-HSMConfigGupshup_is_hsm-results"]/li')
            for option in is_hsm_options:
                if option.text == ("Si" if is_hsm else "No"):
                    option.click()
                    break

            auto_managed_field = self.driver.find_element(By.XPATH, '//*[@id="select2-HSMConfigGupshup_is_auto_managed-container"]')
            auto_managed_field.click()
            auto_managed_options = self.driver.find_elements(By.XPATH, '//*[@id="select2-HSMConfigGupshup_is_auto_managed-results"]/li')
            for option in auto_managed_options:
                if option.text == ("Si" if is_auto_managed else "No"):
                    option.click()
                    break

            awaiting_input_field = self.driver.find_element(By.XPATH, '//*[@id="select2-HSMConfigGupshup_awaitingInput-container"]')
            awaiting_input_field.click()
            awaiting_input_options = self.driver.find_elements(By.XPATH, '//*[@id="select2-HSMConfigGupshup_awaitingInput-results"]/li')
            for option in awaiting_input_options:
                if option.text == ("Si" if awaiting_input else "No"):
                    option.click()
                    break

            parametros_field = self.driver.find_element(By.XPATH, '//*[@id="HSMConfigGupshup_param_count"]')
            self.slow_type(parametros_field, str(params_count))

            add_param_button = self.driver.find_element(By.XPATH, '//*[@id="HSMConfigGupshup_fields_cfg_inputtable"]/tfoot/tr/td/a[1]/div')
            for _ in range(params_count - 1):
                add_param_button.click()
                time.sleep(1)

            if not isinstance(parametros, list):
                raise ValueError("La variable 'parametros' debe ser una lista.")

            for index, param in enumerate(parametros, 1):
                try:
                    param_xpath = f'//*[@id="HSMConfigGupshup_fields_cfg_inputtable_field_{index}"]'
                    print(f"Buscando el campo de parámetro con XPath: {param_xpath}")
                    
                    param_name_field = WebDriverWait(self.driver, 20).until(
                        EC.visibility_of_element_located((By.XPATH, param_xpath))
                    )
                    
                    print(f"Llenando el parámetro en el índice {index} con el valor: {param}")
                    self.slow_type(param_name_field, param)
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"Error llenando el parámetro en el índice {index}: {e}")

            body_field = self.driver.find_element(By.XPATH, '//*[@id="HSMConfigGupshup_form"]/div[18]/div[1]/div[2]/div')
            self.slow_type(body_field, message)
            
            example_field = self.driver.find_element(By.XPATH, '//*[@id="HSMConfigGupshup_form"]/div[19]/div[1]/div[2]/div' )
            self.slow_type(example_field, message)

            vigencia_field = self.driver.find_element(By.XPATH, '//*[@id="HSMConfigGupshup_validity"]')
            self.slow_type(vigencia_field, "24")

            print("Formulario llenado.")

            try:
                save_button = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="save__button"]/i[2]'))
                )
                save_button.click()
                print("Botón de guardar clickeado.")
            except Exception as e:
                print(f"Error al hacer clic en el botón de guardar: {e}")

            return self.driver

        except Exception as e:
            print(f"Ocurrió un error en el login: {e}")
            if self.driver:
                self.driver.quit()
            return None
