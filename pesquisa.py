from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
import kivy
from kivy.graphics import Color
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivy.core.window import Window
from datetime import datetime

# Definir a cor de fundo da janela para um tom mais suave (quase branco)
Window.clearcolor = (0.95, 0.95, 0.95, 1)

# Dados simulados para pessoas
# Em um aplicativo real, isso viria de uma base de dados na web
MOCK_PEOPLE_DATA = {
    "João Silva": {
        "cpf": "123.456.789-00",
        "rg": "MG-12.345.678",
        "mandados": "Nenhum",
        "jusbrasil": "Nenhum processo encontrado."
    },
    "Maria Souza": {
        "cpf": "987.654.321-01",
        "rg": "SP-98.765.432",
        "mandados": "Mandado de citação em aberto (Processo 1234/2023)",
        "jusbrasil": "Processo Civil 5678/2022 (Vara de Família)."
    },
    "Carlos Pereira": {
        "cpf": "111.222.333-44",
        "rg": "RJ-11.223.344",
        "mandados": "Nenhum",
        "jusbrasil": "Nenhum processo encontrado."
    }
}

# Dados simulados para veículos
# Em um aplicativo real, isso viria de uma base de dados do Detran
MOCK_VEHICLE_DATA = {
    "AAA1234": {
        "placa": "AAA1234",
        "marca": "Chevrolet",
        "modelo": "Onix",
        "ano_modelo": "2020/2021",
        "cor": "Branco",
        "cidade_estado": "Belo Horizonte/MG",
        "chassi": "ABCDE",
        "status": "OK" # OK, Roubo/Furto, Alerta
    },
    "BRA2R22": { # Exemplo de Mercosul
        "placa": "BRA2R22",
        "marca": "Ford",
        "modelo": "Ka",
        "ano_modelo": "2018/2019",
        "cor": "Vermelho",
        "cidade_estado": "São Paulo/SP",
        "chassi": "FGHIJ",
        "status": "Roubo/Furto"
    },
    "XYZ9876": {
        "placa": "XYZ9876",
        "marca": "Volkswagen",
        "modelo": "Virtus",
        "ano_modelo": "2022/2023",
        "cor": "Prata",
        "cidade_estado": "Rio de Janeiro/RJ",
        "chassi": "KLMNO",
        "status": "Alerta"
    }
}

# Dados simulados para mandados
MOCK_MANDATES_DATA = [
    {"mandado_id": "M001", "nome": "Fernando Souza", "crime": "Furto Qualificado", "status": "Ativo"},
    {"mandado_id": "M002", "nome": "Juliana Costa", "crime": "Estelionato", "status": "Ativo"},
]

# Dados simulados para procurados
MOCK_WANTED_DATA = [
    {"nome": "Roberto Carlos", "motivo": "Homicídio", "status": "Foragido"},
    {"nome": "Ana Paula", "motivo": "Tráfico de Drogas", "status": "Foragida"},
]

# Dados simulados para desaparecidos
MOCK_MISSING_DATA = [
    {"nome": "Pedro Henrique", "data_desaparecimento": "10/05/2023", "local": "Curitiba/PR"},
    {"nome": "Camila Oliveira", "data_desaparecimento": "22/01/2024", "local": "Fortaleza/CE"},
]


class BaseScreen(Screen):
    """
    Classe base para todas as telas do aplicativo, incluindo o menu suspenso.
    """
    menu_open = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(self._build_header())
        self.add_widget(self._build_menu_drawer())

    def _build_header(self):
        """Constrói o cabeçalho com o botão de menu."""
        header_layout = BoxLayout(
            size_hint=(1, 0.1),
            pos_hint={'top': 1},
            orientation='horizontal',
            padding=10,
            spacing=10
        )
        # Título do aplicativo
        header_layout.add_widget(Label(
            text="Consulta Pública",
            size_hint_x=0.8,
            font_size='20sp',
            bold=True,
            color=(0.1, 0.1, 0.1, 1)
        ))
        # Botão para abrir o menu
        menu_button = Button(
            text="☰", # Ícone de hambúrguer
            size_hint_x=0.2,
            font_size='24sp',
            background_normal='',
            background_color=(0.2, 0.6, 0.8, 1),
            color=(1, 1, 1, 1),
            on_release=self.toggle_menu,
            font_name='Roboto' # Usar uma fonte padrão
        )
        header_layout.add_widget(menu_button)
        return header_layout

    def _build_menu_drawer(self):
        """Constrói o layout do menu suspenso."""
        # O menu será um FloatLayout que aparece sobre outras coisas
        self.menu_drawer = FloatLayout(
            size_hint=(0.7, 0.9), # Largura de 70% da tela, altura de 90%
            pos_hint={'right': 1, 'top': 0.9}, # Fixado à direita
            opacity=0,
            disabled=True # Inicia desabilitado para não interceptar toques
        )

        menu_background = BoxLayout
        orientation='vertical',
        size_hint=(1, 1),
        padding=20,
        spacing=15,
        background_color=(0.1, 0.1, 0.1, 0.9), # Fundo escuro semitransparente
        with self.canvas:
            kivy.graphics.Color(0.1, 0.1, 0.1, 0.9),
            kivy.graphics.Rectangle(pos=self.menu_drawer.pos, size=self.menu_drawer.size)
            
        
        
        self.menu_drawer.add_widget(menu_background)

        # Botões do menu
        menu_options = [
            ("Voltar ao Início", lambda x: self.go_to_screen("main_menu")),
            ("Perfil", lambda x: self.go_to_screen("profile")),
            ("Ajuda", lambda x: self.go_to_screen("help")),
            ("Sair", lambda x: App.get_running_app().stop())
        ]

        for text, callback in menu_options:
            btn = Button(
                text=text,
                size_hint_y=None,
                height=Window.height * 0.08,
                background_normal='',
                background_color=(0.2, 0.6, 0.8, 1),
                color=(1, 1, 1, 1),
                font_size='18sp',
                on_release=callback
            )
            menu_background.add_widget(btn)

        # Botão para fechar o menu
        close_button = Button(
            text="Fechar",
            size_hint_y=None,
            height=Window.height * 0.08,
            background_normal='',
            background_color=(0.8, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size='18sp',
            on_release=self.toggle_menu
        )
        menu_background.add_widget(close_button)

        # Usar um BoxLayout vazio para empurrar os botões para cima
        menu_background.add_widget(BoxLayout())

        return self.menu_drawer

    def toggle_menu(self, instance=None):
        """Alterna a visibilidade do menu suspenso."""
        self.menu_open = not self.menu_open
        if self.menu_open:
            self.menu_drawer.opacity = 1
            self.menu_drawer.disabled = False
        else:
            self.menu_drawer.opacity = 0
            self.menu_drawer.disabled = True

    def go_to_screen(self, screen_name):
        """Navega para outra tela e fecha o menu."""
        self.manager.current = screen_name
        self.toggle_menu() # Fecha o menu após a navegação


class MainMenuScreen(BaseScreen):
    """
    Tela do menu principal do aplicativo.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'main_menu'

        layout = BoxLayout(
            orientation='vertical',
            padding=30,
            spacing=20,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.9, 0.8)
        )

        title = Label(
            text="Menu Principal",
            font_size='28sp',
            bold=True,
            color=(0.1, 0.1, 0.1, 1),
            size_hint_y=None,
            height=50
        )
        layout.add_widget(title)

        # Botões para as opções de consulta
        buttons_data = [
            ("Consultar Pessoa", "person_search"),
            ("Consultar Veículo", "vehicle_search"),
            ("Mandados de Prisão", "mandates_search"),
            ("Pessoas Procuradas", "wanted_search"),
            ("Pessoas Desaparecidas", "missing_search"),
        ]

        for text, screen_name in buttons_data:
            btn = Button(
                text=text,
                size_hint_y=None,
                height=Window.height * 0.1,
                font_size='20sp',
                background_normal='',
                background_color=(0.2, 0.6, 0.8, 1), # Cor primária azul
                color=(1, 1, 1, 1)
            )
            btn.bind(
    on_release=lambda btn_instance, screen=screen_name: (
        setattr(self.manager.transition, "direction", "left" if self.manager.current == "main_menu" else "right"),
        setattr(self.manager, "current", screen)
    )
)
        layout.add_widget(btn)

        def mudar_tela(btn_instance, screen):
            self.manager.transition.direction = "left" if self.manager.current == "main_menu" else "right"
            self.manager.current = screen

        btn.bind(on_release=lambda btn_instance, screen=screen_name: mudar_tela(btn_instance, screen))
        layout.add_widget(btn)


class PersonSearchScreen(BaseScreen):
    """
    Tela para pesquisa de pessoas.
    """
    person_name = StringProperty("")
    search_result_text = StringProperty("Nenhum resultado para exibir.")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'person_search'

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Campo de entrada para o nome completo
        input_layout = BoxLayout(orientation='vertical', size_hint_y=0.2)
        input_layout.add_widget(Label(
            text="Nome Completo:",
            size_hint_y=None,
            height=40,
            color=(0.1, 0.1, 0.1, 1),
            font_size='18sp'
        ))
        self.name_input = TextInput(
            multiline=False,
            font_size='20sp',
            padding=(10, 10, 10, 10),
            size_hint_y=None,
            height=50,
            background_normal='',
            background_color=(1, 1, 1, 1),
            foreground_color=(0.1, 0.1, 0.1, 1),
            hint_text_color=(0.5, 0.5, 0.5, 1)
        )
        input_layout.add_widget(self.name_input)

        search_button = Button(
            text="Pesquisar Pessoa",
            size_hint_y=None,
            height=60,
            font_size='22sp',
            background_normal='',
            background_color=(0.2, 0.6, 0.8, 1),
            color=(1, 1, 1, 1)
        )
        search_button.bind(on_release=self.perform_person_search)
        input_layout.add_widget(search_button)
        main_layout.add_widget(input_layout)

        # Área de resultados (ScrollView para conteúdo longo)
        scroll_view = ScrollView(size_hint=(1, 0.7))
        self.result_label = Label(
            text=self.search_result_text,
            size_hint_y=None,
            height=self.height, # Será ajustado pelo `text_size`
            text_size=(self.width - 20, None), # Largura menos o padding
            valign='top',
            halign='left',
            color=(0.1, 0.1, 0.1, 1),
            font_size='18sp',
            padding=(10, 10)
        )
        self.result_label.bind(texture_size=self._set_label_height)
        scroll_view.add_widget(self.result_label)
        main_layout.add_widget(scroll_view)

        self.add_widget(main_layout)

    def _set_label_height(self, instance, value):
        instance.height = value[1]

    def perform_person_search(self, instance):
        """Executa a pesquisa de pessoa com base no nome inserido."""
        name_to_search = self.name_input.text.strip()
        if not name_to_search:
            self.search_result_text = "Por favor, digite um nome completo para pesquisar."
            self.result_label.text = self.search_result_text
            return

        person_data = MOCK_PEOPLE_DATA.get(name_to_search)
        if person_data:
            self.search_result_text = (
                f"[color=000000][b]Resultado da Consulta:[/b][/color]\n\n"
                f"[color=000000]Nome Completo: [b]{name_to_search}[/b][/color]\n"
                f"[color=000000]CPF: {person_data['cpf']}[/color]\n"
                f"[color=000000]RG: {person_data['rg']}[/color]\n"
                f"[color=000000]Mandados Judiciais e de Captura: {person_data['mandados']}[/color]\n"
                f"[color=000000]Processos no Jus Brasil: {person_data['jusbrasil']}[/color]"
            )
        else:
            self.search_result_text = (
                f"[color=0FF000]Pessoa '[b]{name_to_search}[/b]' não encontrada na base de dados simulada.[/color]\n"
                f"[color=000000]Por favor, tente 'João Silva', 'Maria Souza' ou 'Carlos Pereira'.[/color]"
            )
        self.result_label.text = self.search_result_text


class VehicleSearchScreen(BaseScreen):
    """
    Tela para pesquisa de veículos.
    """
    vehicle_status_text = StringProperty("Status do Veículo")
    vehicle_status_color = ListProperty([0.5, 0.5, 0.5, 1]) # Cinza padrão
    search_result_text = StringProperty("Nenhum resultado para exibir.")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'vehicle_search'

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Logo do veículo
        vehicle_image_placeholder = Image(
            source='https://placehold.co/150x100/A0A0A0/FFFFFF?text=VEÍCULO', # Placeholder de imagem
            size_hint=(1, 0.2),
            allow_stretch=True,
            keep_ratio=True
        )
        main_layout.add_widget(vehicle_image_placeholder)

        # Campo de status do veículo
        self.status_box = BoxLayout
        size_hint_y=None,
        height=60,
        padding=10,
        spacing=10,
        with self.canvas:
            kivy.graphics.Color(*self.vehicle_status_color),
            kivy.graphics.Rectangle(pos=self.pos, size=self.size)
            
        
        self.status_label = Label(
            text=self.vehicle_status_text,
            font_size='20sp',
            bold=True,
            color=(1, 1, 1, 1)
        )
        self.status_box.add_widget(self.status_label)
        main_layout.add_widget(self.status_box)

        # Campos de entrada para as placas
        input_layout = GridLayout(cols=2, size_hint_y=0.2, spacing=10, padding=10)
        input_layout.add_widget(Label(
            text="Placa Padrão (ABC1234):",
            color=(0.1, 0.1, 0.1, 1),
            font_size='16sp'
        ))
        self.plate_standard_input = TextInput(
            multiline=False,
            font_size='20sp',
            padding=(10, 10, 10, 10),
            background_normal='',
            background_color=(1, 1, 1, 1),
            foreground_color=(0.1, 0.1, 0.1, 1),
            hint_text="ABC1234"
        )
        input_layout.add_widget(self.plate_standard_input)

        input_layout.add_widget(Label(
            text="Placa Mercosul (AAA-0B22):",
            color=(0.1, 0.1, 0.1, 1),
            font_size='16sp'
        ))
        self.plate_mercosul_input = TextInput(
            multiline=False,
            font_size='20sp',
            padding=(10, 10, 10, 10),
            background_normal='',
            background_color=(1, 1, 1, 1),
            foreground_color=(0.1, 0.1, 0.1, 1),
            hint_text="AAA-0B22"
        )
        input_layout.add_widget(self.plate_mercosul_input)
        main_layout.add_widget(input_layout)

        search_button = Button(
            text="Pesquisar Veículo",
            size_hint_y=None,
            height=60,
            font_size='22sp',
            background_normal='',
            background_color=(0.2, 0.6, 0.8, 1),
            color=(1, 1, 1, 1)
        )
        search_button.bind(on_release=self.perform_vehicle_search)
        main_layout.add_widget(search_button)

        # Área de resultados
        scroll_view = ScrollView(size_hint=(1, 0.3))
        self.result_label = Label(
            text=self.search_result_text,
            size_hint_y=None,
            height=self.height,
            text_size=(self.width - 20, None),
            valign='top',
            halign='left',
            color=(0.1, 0.1, 0.1, 1),
            font_size='18sp',
            padding=(10, 10)
        )
        self.result_label.bind(texture_size=self._set_label_height)
        scroll_view.add_widget(self.result_label)
        main_layout.add_widget(scroll_view)

        # Caixa de diálogo para consultar outro veículo
        self.another_search_box = BoxLayout(
            size_hint_y=None,
            height=60,
            padding=10,
            spacing=10,
            opacity=0, # Inicia oculta
            disabled=True # Inicia desabilitada
        )
        self.another_search_box.add_widget(Label(
            text="Deseja consultar outro veículo?",
            color=(0.1, 0.1, 0.1, 1),
            font_size='18sp'
        ))
        yes_button = Button(
            text="Sim",
            size_hint_x=0.3,
            background_normal='',
            background_color=(0.4, 0.8, 0.4, 1),
            color=(1, 1, 1, 1),
            on_release=self.clear_vehicle_search
        )
        self.another_search_box.add_widget(yes_button)
        main_layout.add_widget(self.another_search_box)

        self.add_widget(main_layout)

        # Bind para atualizar a cor do status box
        self.bind(vehicle_status_color=self._update_status_box_color)

    def _update_status_box_color(self, instance, value):
        self.status_box.canvas.before.children[1].rgba = value

    def _set_label_height(self, instance, value):
        instance.height = value[1]

    def perform_vehicle_search(self, instance):
        """Executa a pesquisa de veículo com base na placa inserida."""
        plate_to_search = self.plate_standard_input.text.strip().upper() or self.plate_mercosul_input.text.strip().upper()
        if not plate_to_search:
            self.search_result_text = "Por favor, digite a placa do veículo para pesquisar."
            self.result_label.text = self.search_result_text
            self.vehicle_status_text = "Status do Veículo"
            self.vehicle_status_color = [0.5, 0.5, 0.5, 1] # Cinza
            self.another_search_box.opacity = 0
            self.another_search_box.disabled = True
            return

        vehicle_data = MOCK_VEHICLE_DATA.get(plate_to_search)
        current_date = datetime.now().strftime("%d/%m/%Y")

        if vehicle_data:
            if vehicle_data['status'] == "Roubo/Furto" or vehicle_data['status'] == "Alerta":
                self.vehicle_status_text = f"🚨 Queixa de {vehicle_data['status']}! 🚨"
                self.vehicle_status_color = [0.8, 0.2, 0.2, 1] # Vermelho
            else:
                self.vehicle_status_text = "✅ Nenhum registro de Roubo/Furto ou Alerta."
                self.vehicle_status_color = [0.4, 0.8, 0.4, 1] # Verde

            self.search_result_text = (
                f"[color=000000][b]Resultado da Consulta:[/b][/color]\n\n"
                f"[color=000000]Placa: [b]{vehicle_data['placa']}[/b][/color]\n"
                f"[color=000000]Marca: {vehicle_data['marca']}[/color]\n"
                f"[color=000000]Modelo: {vehicle_data['modelo']}[/color]\n"
                f"[color=000000]Ano Modelo: {vehicle_data['ano_modelo']}[/color]\n"
                f"[color=000000]Cor: {vehicle_data['cor']}[/color]\n"
                f"[color=000000]Cidade/Estado: {vehicle_data['cidade_estado']}[/color]\n"
                f"[color=000000]Final do Chassi: {vehicle_data['chassi']}[/color]\n"
                f"[color=000000]Data da Pesquisa: {current_date}[/color]"
            )
        else:
            self.vehicle_status_text = "Status do Veículo"
            self.vehicle_status_color = [0.5, 0.5, 0.5, 1] # Cinza
            self.search_result_text = (
                f"[color=000000]Veículo com placa '[b]{plate_to_search}[/b]' não encontrado na base de dados simulada.[/color]\n"
                f"[color=000000]Por favor, tente 'AAA1234', 'BRA2R22' ou 'XYZ9876'.[/color]"
            )

        self.result_label.text = self.search_result_text
        self.another_search_box.opacity = 1
        self.another_search_box.disabled = False

    def clear_vehicle_search(self, instance):
        """Limpa os campos e resultados da pesquisa de veículo."""
        self.plate_standard_input.text = ""
        self.plate_mercosul_input.text = ""
        self.search_result_text = "Nenhum resultado para exibir."
        self.result_label.text = self.search_result_text
        self.vehicle_status_text = "Status do Veículo"
        self.vehicle_status_color = [0.5, 0.5, 0.5, 1] # Cinza
        self.another_search_box.opacity = 0
        self.another_search_box.disabled = True


class MandatesSearchScreen(BaseScreen):
    """
    Tela para pesquisa de mandados de prisão.
    """
    search_result_text = StringProperty("Nenhum mandado para exibir.")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'mandates_search'

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        title = Label(
            text="Pesquisa de Mandados de Prisão",
            font_size='24sp',
            bold=True,
            color=(0.1, 0.1, 0.1, 1),
            size_hint_y=None,
            height=50
        )
        main_layout.add_widget(title)

        # Entrada para nome para pesquisa de mandado (simulada)
        input_layout = BoxLayout(orientation='vertical', size_hint_y=0.15)
        input_layout.add_widget(Label(
            text="Nome para pesquisa de mandado:",
            color=(0.1, 0.1, 0.1, 1),
            font_size='18sp'
        ))
        self.mandate_name_input = TextInput(
            multiline=False,
            font_size='20sp',
            padding=(10, 10, 10, 10),
            background_normal='',
            background_color=(1, 1, 1, 1),
            foreground_color=(0.1, 0.1, 0.1, 1)
        )
        input_layout.add_widget(self.mandate_name_input)

        search_button = Button(
            text="Pesquisar Mandado",
            size_hint_y=None,
            height=60,
            font_size='22sp',
            background_normal='',
            background_color=(0.2, 0.6, 0.8, 1),
            color=(1, 1, 1, 1)
        )
        search_button.bind(on_release=self.perform_mandate_search)
        input_layout.add_widget(search_button)
        main_layout.add_widget(input_layout)


        # Área de resultados
        scroll_view = ScrollView(size_hint=(1, 0.5))
        self.result_label = Label(
            text=self.search_result_text,
            size_hint_y=None,
            height=self.height,
            text_size=(self.width - 20, None),
            valign='top',
            halign='left',
            color=(0.1, 0.1, 0.1, 1),
            font_size='18sp',
            padding=(10, 10)
        )
        self.result_label.bind(texture_size=self._set_label_height)
        scroll_view.add_widget(self.result_label)
        main_layout.add_widget(scroll_view)

        self.add_widget(main_layout)

    def _set_label_height(self, instance, value):
        instance.height = value[1]

    def perform_mandate_search(self, instance):
        """Pesquisa mandados de prisão (simulado)."""
        name_to_search = self.mandate_name_input.text.strip().lower()
        results = [
            m for m in MOCK_MANDATES_DATA
            if name_to_search in m["nome"].lower()
        ]

        if results:
            self.search_result_text = "[color=000000][b]Mandados Encontrados:[/b][/color]\n\n"
            for m in results:
                self.search_result_text += (
                    f"[color=000000]ID: {m['mandado_id']}\n"
                    f"Nome: {m['nome']}\n"
                    f"Crime: {m['crime']}\n"
                    f"Status: [b]{m['status']}[/b][/color]\n\n"
                )
        else:
            self.search_result_text = (
                f"[color=000000]Nenhum mandado encontrado para '[b]{name_to_search}[/b]'.[/color]\n"
                f"[color=000000]Tente 'Fernando Souza' ou 'Juliana Costa'.[/color]"
            )
        self.result_label.text = self.search_result_text


class WantedSearchScreen(BaseScreen):
    """
    Tela para pesquisa de pessoas procuradas pela justiça.
    """
    search_result_text = StringProperty("Nenhuma pessoa procurada para exibir.")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'wanted_search'

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        title = Label(
            text="Pessoas Procuradas pela Justiça",
            font_size='24sp',
            bold=True,
            color=(0.1, 0.1, 0.1, 1),
            size_hint_y=None,
            height=50
        )
        main_layout.add_widget(title)

        # Entrada para nome para pesquisa de procurados (simulada)
        input_layout = BoxLayout(orientation='vertical', size_hint_y=0.15)
        input_layout.add_widget(Label(
            text="Nome para pesquisa de procurado:",
            color=(0.1, 0.1, 0.1, 1),
            font_size='18sp'
        ))
        self.wanted_name_input = TextInput(
            multiline=False,
            font_size='20sp',
            padding=(10, 10, 10, 10),
            background_normal='',
            background_color=(1, 1, 1, 1),
            foreground_color=(0.1, 0.1, 0.1, 1)
        )
        input_layout.add_widget(self.wanted_name_input)

        search_button = Button(
            text="Pesquisar Procurado",
            size_hint_y=None,
            height=60,
            font_size='22sp',
            background_normal='',
            background_color=(0.2, 0.6, 0.8, 1),
            color=(1, 1, 1, 1)
        )
        search_button.bind(on_release=self.perform_wanted_search)
        input_layout.add_widget(search_button)
        main_layout.add_widget(input_layout)

        # Área de resultados
        scroll_view = ScrollView(size_hint=(1, 0.5))
        self.result_label = Label(
            text=self.search_result_text,
            size_hint_y=None,
            height=self.height,
            text_size=(self.width - 20, None),
            valign='top',
            halign='left',
            color=(0.1, 0.1, 0.1, 1),
            font_size='18sp',
            padding=(10, 10)
        )
        self.result_label.bind(texture_size=self._set_label_height)
        scroll_view.add_widget(self.result_label)
        main_layout.add_widget(scroll_view)

        self.add_widget(main_layout)

    def _set_label_height(self, instance, value):
        instance.height = value[1]

    def perform_wanted_search(self, instance):
        """Pesquisa pessoas procuradas (simulado)."""
        name_to_search = self.wanted_name_input.text.strip().lower()
        results = [
            p for p in MOCK_WANTED_DATA
            if name_to_search in p["nome"].lower()
        ]

        if results:
            self.search_result_text = "[color=000000][b]Pessoas Procuradas Encontradas:[/b][/color]\n\n"
            for p in results:
                self.search_result_text += (
                    f"[color=000000]Nome: {p['nome']}\n"
                    f"Motivo: {p['motivo']}\n"
                    f"Status: [b]{p['status']}[/b][/color]\n\n"
                )
        else:
            self.search_result_text = (
                f"[color=000000]Nenhuma pessoa procurada encontrada para '[b]{name_to_search}[/b]'.[/color]\n"
                f"[color=000000]Tente 'Roberto Carlos' ou 'Ana Paula'.[/color]"
            )
        self.result_label.text = self.search_result_text


class MissingSearchScreen(BaseScreen):
    """
    Tela para pesquisa de pessoas desaparecidas.
    """
    search_result_text = StringProperty("Nenhuma pessoa desaparecida para exibir.")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'missing_search'

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        title = Label(
            text="Pessoas Desaparecidas",
            font_size='24sp',
            bold=True,
            color=(0.1, 0.1, 0.1, 1),
            size_hint_y=None,
            height=50
        )
        main_layout.add_widget(title)

        # Entrada para nome para pesquisa de desaparecidos (simulada)
        input_layout = BoxLayout(orientation='vertical', size_hint_y=0.15)
        input_layout.add_widget(Label(
            text="Nome para pesquisa de desaparecido:",
            color=(0.1, 0.1, 0.1, 1),
            font_size='18sp'
        ))
        self.missing_name_input = TextInput(
            multiline=False,
            font_size='20sp',
            padding=(10, 10, 10, 10),
            background_normal='',
            background_color=(1, 1, 1, 1),
            foreground_color=(0.1, 0.1, 0.1, 1)
        )
        input_layout.add_widget(self.missing_name_input)

        search_button = Button(
            text="Pesquisar Desaparecido",
            size_hint_y=None,
            height=60,
            font_size='22sp',
            background_normal='',
            background_color=(0.2, 0.6, 0.8, 1),
            color=(1, 1, 1, 1)
        )
        search_button.bind(on_release=self.perform_missing_search)
        input_layout.add_widget(search_button)
        main_layout.add_widget(input_layout)

        # Área de resultados
        scroll_view = ScrollView(size_hint=(1, 0.5))
        self.result_label = Label(
            text=self.search_result_text,
            size_hint_y=None,
            height=self.height,
            text_size=(self.width - 20, None),
            valign='top',
            halign='left',
            color=(0.1, 0.1, 0.1, 1),
            font_size='18sp',
            padding=(10, 10)
        )
        self.result_label.bind(texture_size=self._set_label_height)
        scroll_view.add_widget(self.result_label)
        main_layout.add_widget(scroll_view)

        self.add_widget(main_layout)

    def _set_label_height(self, instance, value):
        instance.height = value[1]

    def perform_missing_search(self, instance):
        """Pesquisa pessoas desaparecidas (simulado)."""
        name_to_search = self.missing_name_input.text.strip().lower()
        results = [
            p for p in MOCK_MISSING_DATA
            if name_to_search in p["nome"].lower()
        ]

        if results:
            self.search_result_text = "[color=000000][b]Pessoas Desaparecidas Encontradas:[/b][/color]\n\n"
            for p in results:
                self.search_result_text += (
                    f"[color=000000]Nome: {p['nome']}\n"
                    f"Data Desaparecimento: {p['data_desaparecimento']}\n"
                    f"Local: {p['local']}[/color]\n\n"
                )
        else:
            self.search_result_text = (
                f"[color=000000]Nenhuma pessoa desaparecida encontrada para '[b]{name_to_search}[/b]'.[/color]\n"
                f"[color=000000]Tente 'Pedro Henrique' ou 'Camila Oliveira'.[/color]"
            )
        self.result_label.text = self.search_result_text


class ProfileScreen(BaseScreen):
    """
    Tela de perfil do usuário (placeholder).
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'profile'
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        layout.add_widget(Label(
            text="Perfil do Usuário",
            font_size='28sp',
            bold=True,
            color=(0.1, 0.1, 0.1, 1)
        ))
        layout.add_widget(Label(
            text="Esta é a tela de perfil do usuário. Aqui poderiam estar informações de login ou configurações.",
            halign='center',
            valign='middle',
            text_size=(Window.width - 60, None),
            color=(0.1, 0.1, 0.1, 1),
            font_size='18sp'
        ))
        layout.add_widget(Button(
            text="Voltar ao Menu Principal",
            size_hint_y=None,
            height=60,
            font_size='22sp',
            background_normal='',
            background_color=(0.2, 0.6, 0.8, 1),
            color=(1, 1, 1, 1),
            on_release=lambda x: setattr(self.manager, 'current', 'main_menu')
        ))
        self.add_widget(layout)


class HelpScreen(BaseScreen):
    """
    Tela de ajuda do aplicativo.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'help'
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        layout.add_widget(Label(
            text="Ajuda do Aplicativo",
            font_size='28sp',
            bold=True,
            color=(0.1, 0.1, 0.1, 1)
        ))
        help_text = (
            "Bem-vindo ao aplicativo de Consulta Pública!\n\n"
            "Use o menu principal para selecionar o tipo de consulta desejada:\n"
            "- [b]Consultar Pessoa:[/b] Insira o nome completo para ver dados simulados de CPF, RG, mandados e processos.\n"
            "- [b]Consultar Veículo:[/b] Insira a placa (padrão ou Mercosul) para obter informações simuladas do veículo e seu status de roubo/furto.\n"
            "- [b]Mandados de Prisão:[/b] Pesquise por nomes para encontrar mandados simulados.\n"
            "- [b]Pessoas Procuradas:[/b] Pesquise por nomes para encontrar pessoas procuradas simuladas.\n"
            "- [b]Pessoas Desaparecidas:[/b] Pesquise por nomes para encontrar pessoas desaparecidas simuladas.\n\n"
            "Use o menu '☰' no canto superior direito para:\n"
            "- [b]Voltar ao Início:[/b] Retorna à tela principal e limpa as pesquisas.\n"
            "- [b]Perfil:[/b] Acesse as configurações de perfil (se implementado).\n"
            "- [b]Sair:[/b] Fecha o aplicativo."
        )
        layout.add_widget(Label(
            text=help_text,
            halign='left',
            valign='top',
            text_size=(Window.width - 60, None),
            color=(0.1, 0.1, 0.1, 1),
            font_size='18sp',
            markup=True
        ))
        layout.add_widget(Button(
            text="Voltar ao Menu Principal",
            size_hint_y=None,
            height=60,
            font_size='22sp',
            background_normal='',
            background_color=(0.2, 0.6, 0.8, 1),
            color=(1, 1, 1, 1),
            on_release=lambda x: setattr(self.manager, 'current', 'main_menu')
        ))
        self.add_widget(layout)


class PublicConsultationApp(App):
    """
    Classe principal do aplicativo Kivy.
    """
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(MainMenuScreen())
        self.sm.add_widget(PersonSearchScreen())
        self.sm.add_widget(VehicleSearchScreen())
        self.sm.add_widget(MandatesSearchScreen())
        self.sm.add_widget(WantedSearchScreen())
        self.sm.add_widget(MissingSearchScreen())
        self.sm.add_widget(ProfileScreen())
        self.sm.add_widget(HelpScreen())
        return self.sm


if __name__ == '__main__':

    PublicConsultationApp().run()
