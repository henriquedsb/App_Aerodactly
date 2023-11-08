import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.optimize import curve_fit, fsolve
import pandas as pd
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
    
    # Método para calcular e plotar as curvas de tração disponível e requerida
    def curvas_tracao_disponivel_requerida(self):
        # Definição dos parâmetros iniciais
        W = float(self.peso_aeronave.get()) # Peso da aeronave (N)
        ro = 1.225  # Densidade do ar para uma altitude (kg/m^3)
        v = [8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]  # Velocidades da aeronave (m/s)
        S = float(self.asa_area_aeronave.get()) # Área da asa (m^2)
        AR = float(self.asa_alongamento_aeronave .get())  # Alongamento da asa
        Cd0 = float(self.coef_arrasto_parasita.get()) # Coeficiente de arrasto parasita
        e0 = float(self.coef_arrasto_induzido.get())  # Coeficiente de arrasto induzido - varia entre 0.95 e 1 (asa ideal)

        # Listas para armazenar os resultados
        lista_Tr = []
        lista_D0 = []
        lista_Di = []
        lista_Td = [35.525, 33.910, 32.013, 29.845, 27.414, 24.727, 21.790, 18.608, 15.185, 11.526, 7.635, 3.515]  # Tração disponível (N)
        
        # Loop para calcular os coeficientes e forças para cada velocidade
        for velocidade in v:
            Cl = (2 * W) / (ro * (velocidade ** 2) * S)  # Coeficiente de sustentação requerido
            Cd = Cd0 + (Cl**2) / (np.pi * e0 * AR)  # Coeficiente de arrasto total (Cd = Cd0 + (Cl^2) / (pi * e0 * AR))
            Tr = W / (Cl / Cd)  # Tração requerida
            D0 = (1 / 2) * ro * (velocidade ** 2) * S * Cd0  # Força de arrasto parasita
            Di = (1 / 2) * ro * (velocidade ** 2) * S * (Cd0 * (Cl ** 2))  # Força de arrasto induzida
            
            # Adiciona os resultados às listas
            lista_Tr.append(Tr)
            lista_D0.append(D0)
            lista_Di.append(Di)

        # Cria um DataFrame para armazenar os dados
        dados = {
            'v(m/s)': v,
            'Td(N) APC 13"x4"': lista_Td,
            'D0(N)': lista_D0,
            'Di(N)': lista_Di,
            'Tr(N)': lista_Tr
        }
        df = pd.DataFrame(dados)
        #print(df)  # Imprime o DataFrame com os dados

        # Ajusta curvas aos dados usando a função curve_fit do SciPy
        self.params1, params_covariance1 = curve_fit(self.func1, v, lista_Td)
        #print("Parâmetros da curva 1:", self.params1)

        self.params2, params_covariance2 = curve_fit(self.func2, v, lista_Tr)
        #print("Parâmetros da curva 2:", self.params2)

        # Calcula os pontos de interseção das curvas ajustadas
        intersecao_pontos = []
        for x_guess in np.linspace(min(v + v), max(v + v), num=100):
            try:
                x_intersecao, y_intersecao = fsolve(self.equacoes, [x_guess, self.func1(x_guess, *self.params1)])
                intersecao_pontos.append((x_intersecao, y_intersecao))
            except:
                pass

        # Determina as velocidades mínima e máxima de interseção
        v_min = min(ponto[0] for ponto in intersecao_pontos)
        v_max = max(ponto[0] for ponto in intersecao_pontos)
        resultado_tracao = (f'Velocidade mínima: {v_min:.3f} m/s\n'
                            f'Velocidade máxima: {v_max:.3f} m/s\n')

        # Plota os gráficos
        figura = plt.figure(figsize=(8, 6))
        plt.plot(v, lista_Td, label='Tração Disponível')
        plt.plot(v, lista_Tr, label='Tração Requisitada')
        plt.plot(v, lista_D0, label='Força de Arrasto Parasita')
        plt.plot(v, lista_Di, label='Força de Arrasto Induzida')
        plt.title('Tração Disponível e Requisitada')
        plt.xlabel('Velocidade (m/s)')
        plt.ylabel('Tração (N)')
        plt.legend()

        canvas = FigureCanvasTkAgg(figura, master=self.frame_grafico)
        canvas.get_tk_widget().pack()
        canvas.draw()

        self.texto_resultado_curvas.set(resultado_tracao)

    # Função para ajuste de curva (exponencial)
    def func1(self, x, a, b, c):
        return a * np.exp(b * x) + c

    # Função para ajuste de curva (polinomial de segundo grau)
    def func2(self, x, d, e, f):
        return d * x**2 + e * x + f

    # Equações para encontrar os pontos de interseção
    def equacoes(self, vars):
        x, y = vars
        eq1 = self.func1(x, *self.params1) - y
        eq2 = self.func2(x, *self.params2) - y
        return [eq1, eq2]