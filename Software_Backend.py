import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import sys

class Backend():

    def calcular_atmosfera(self):
        try:
            altitude = float(self.entrada_altitude.get())
            resultado = self.display_resultados(altitude)
            self.texto_resultado.set(resultado)
            self.plotar_graficos(altitude/ 1000)
        except ValueError as e:
            self.texto_resultado.set(str(e))

    def obter_parametros_atmosfera(self, altitude):

        # Constantes para a Atmosfera Padrão Internacional
        self.T0 = 288.15  # Temperatura ao nível do mar em Kelvin
        self.P0 = 101325  # Pressão ao nível do mar em Pa
        self.R_ar = 287.05   # Constante específica para o ar seco em J/(kg*K)
        self.g = 9.80665  # Aceleração devido à gravidade em m/s^2
        self.d = 1.225 # densidade ao nivel do mar (kg/m³)

        if altitude < 0:
            raise ValueError("Altitude não pode ser negativa")

        if 0 <= altitude <= 11000:
            a = -0.0065
            temperatura = 288.16 + a*(altitude)
            pressao =  self.P0 * ((temperatura / 288.16) ** (-(self.g) / (self.R_ar * a)))
            densidade =  self.d * ((temperatura / 288.16) ** -((self.g / (self.R_ar * a))+1))
        
        elif 11000 < altitude <= 25000:
            temperatura = 216.66
            pressao =  22633.063267781792 * (np.exp(-((self.g * (altitude - 11000)) / (self.R_ar * temperatura))))
            densidade = 0.36392992704843696 * (np.exp(-((self.g * (altitude - 11000)) / (self.R_ar * temperatura))))

        elif 25000 < altitude <= 47000:
            a = 0.003
            temperatura = 216.66 + a * (altitude - 25000)
            pressao =  2488.9284998637704 * ((temperatura / 216.66) ** (-(self.g)/ (self.R_ar * a)))
            densidade =  0.040020900249662594 * ((temperatura / 216.66) ** -((self.g / (self.R_ar * a))+1))

        elif 47000 < altitude <= 53000:
            temperatura = 282.66
            pressao = 120.47006704567295 * (np.exp(-((self.g * (altitude - 11000)) / (self.R_ar * temperatura))))
            densidade = 0.0014848000352386834 * (np.exp(-((self.g * (altitude - 11000)) / (self.R_ar * temperatura))))

        elif 53000 < altitude <= 79000:
            a = -0.0045
            temperatura = 282.66 + a * (altitude - 53000)
            pressao =  0.7520835925686842 * ((temperatura / 282.66) ** (-(self.g) / (self.R_ar * a)))
            densidade =  9.269470600734819e-06 * ((temperatura / 282.66) ** -((self.g / (self.R_ar * a))+1))

        elif 79000 < altitude <= 90000:
            temperatura = 165.66
            pressao =  0.01301937861177987 * (np.exp(-((self.g * (altitude - 11000)) / (self.R_ar * temperatura))))
            densidade =  2.737951630479538e-07 * (np.exp(-((self.g * (altitude - 11000)) / (self.R_ar * temperatura))))

        elif 90000 < altitude <= 105000:
            a = 0.004
            temperatura = 165.66 + a * (altitude - 90000)
            pressao =  1.0941946323031164e-09 * ((temperatura / 165.66) ** (-(self.g) / (self.R_ar * a)))
            densidade =  2.3010714004934494e-14* ((temperatura / 165.66) ** -((self.g / (self.R_ar * a))+1))

        else:
            raise ValueError('A altitude está além dos limites da atmosfera padrão')

        return altitude, temperatura, pressao, densidade

    def display_resultados(self, altitude):
        altitude, temperatura, pressao, densidade = self.obter_parametros_atmosfera(altitude)
    
        def formatar_com_notacao_cientifica(valor, limite=1e-3, casas_decimais=4):
            if abs(valor) < limite:
                return f'{valor:_.{casas_decimais}e}'
            return f'{valor:_.{casas_decimais}f}'
        
        return (
            f'Na altitude de {altitude:_.2f} metros:\n'
            f'Temperatura: {temperatura:_.2f} K\n'
            f'Pressão: {formatar_com_notacao_cientifica(pressao)} Pa\n'
            f'Densidade: {formatar_com_notacao_cientifica(densidade)} kg/m³'
        ).replace('.',',').replace('_','.')
    
    def pegar_informacoes(self):
        lista_altitude = list(range(105001))
        lista_temperaturas = []
        lista_pressoes = []
        lista_densidades = []

        for altitude in lista_altitude:
            altitude, temperatura, pressao, densidade = self.obter_parametros_atmosfera(altitude)
            lista_temperaturas.append(temperatura)
            lista_pressoes.append(pressao)
            lista_densidades.append(densidade)

         # Convertendo altitudes para quilômetros
        lista_altitude_km = [alt / 1000 for alt in lista_altitude]
        lista_pressoes_kPa = [pressao / 1000 for pressao in lista_pressoes]

        return lista_altitude_km, lista_temperaturas, lista_pressoes_kPa, lista_densidades


    def plotar_graficos(self, altitude_usuario_km):
        lista_altitude_km, lista_temperaturas, lista_pressoes_kPa, lista_densidades = self.pegar_informacoes()

        indice_usuario = int(altitude_usuario_km * 1000)

        figura, eixos = plt.subplots(1, 3, figsize=(15/2, 5/2))

        titulo_figura = f'Perfil Atmosférico a {altitude_usuario_km:.2f} km'
        figura.suptitle(titulo_figura, fontsize=16)

        eixos[0].plot(lista_temperaturas, lista_altitude_km)
        eixos[0].plot(lista_temperaturas[indice_usuario], altitude_usuario_km, marker='o', color='red', markersize=8)
        eixos[0].set_xlabel('Temperatura (K)')
        eixos[0].set_ylabel('Altitude (km)')
        eixos[0].set_title('Temperatura vs Altitude')

        eixos[1].plot(lista_pressoes_kPa, lista_altitude_km)
        eixos[1].plot(lista_pressoes_kPa[indice_usuario], altitude_usuario_km, marker='o', color='red', markersize=8)
        eixos[1].set_xlabel('Pressão (kPa)')
        eixos[1].set_ylabel('Altitude (km)')
        eixos[1].set_title('Pressão vs Altitude')
        #eixos[1].ticklabel_format(axis='x', style='sci', scilimits=(0,0))  # Notação científica para os valores de pressão
        eixos[1].yaxis.get_major_formatter().set_useOffset(False)  # Desativa o uso de offset nos eixos y

        eixos[2].plot(lista_densidades, lista_altitude_km)
        eixos[2].plot(lista_densidades[indice_usuario], altitude_usuario_km, marker='o', color='red', markersize=8)
        eixos[2].set_xlabel('Densidade (kg/m³)')
        eixos[2].set_ylabel('Altitude (km)')
        eixos[2].set_title('Densidade vs Altitude')
        #eixos[2].ticklabel_format(axis='x', style='sci', scilimits=(0,0))  # Notação científica para os valores de densidade
        eixos[2].yaxis.get_major_formatter().set_useOffset(False)  # Desativa o uso de offset nos eixos y

        for ax in eixos:
            ax.grid()

        figura.tight_layout()

        canvas = FigureCanvasTkAgg(figura, master=self)
        #canvas.get_tk_widget().grid(column=0, row=4, padx=10, pady=10, sticky='w')
        canvas.get_tk_widget().pack()
        canvas.draw()


    def obter_caminho_recurso(caminho_relativo):
        try:
            # Obter caminho absoluto para recursos
            caminho_base = sys._MEIPASS
        except Exception:
            caminho_base = os.path.abspath(".")

        return os.path.join(caminho_base, caminho_relativo)
    