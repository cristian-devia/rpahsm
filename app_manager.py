
from login import LoginManager

class AppManager:
    def __init__(self):
        self.login_manager = LoginManager()

    def ejecutar_automatizacion(self, username, password, campaign, hsm_name, has_parameters, params_count, message, entries_parametros, is_hsm, is_auto_managed, awaiting_input):
        parametros = [entry.get() for entry in entries_parametros]
        
        if not isinstance(parametros, list):
            parametros = list(parametros)
        
        url = "https://cari.ai/app"
        driver = self.login_manager.login(url, username, password, campaign, hsm_name, params_count, message, parametros, is_hsm, is_auto_managed, awaiting_input)
        
        if driver:
            print("Automatización completada con éxito.")
