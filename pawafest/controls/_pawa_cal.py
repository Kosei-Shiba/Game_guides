import flet as ft
import numpy as np

class PawaCal(ft.Column):
    _is_internettou = False
    _is_hard = False
    def __init__(self):
        button_width = 200
        button_height = 50
        self.labels = ["筋力", "敏捷", "技術", "変化球", "精神"]
        self.text = self.inputs
        self.multipliers = self.create_multipliers()
        self.internettou_button = ft.ElevatedButton(text='員多亜熱闘', width=button_width, height=button_height, on_click=self.internettou)
        self.hard_button = ft.ElevatedButton(text='達人', width=button_width, height=button_height, on_click=self.hard)
        self.result_table = self.create_result_table()
        self.reset_button = ft.ElevatedButton(text='Reset',icon=ft.icons.DELETE, width=button_width, height=button_height, on_click=self.reset)
        
        super().__init__([self.text, self.multipliers, self.internettou_button, self.hard_button, self.result_table, self.reset_button], expand=False)
    
    @property
    def inputs(self):
        self.offense = ['1B','2B','3B','HR','犠打','犠飛','盗塁']
        self.defense = ['St.','直球','変化','SO','フライ','ゴロ','併殺']
        self.runs = ['RD','失点']
        
        return ft.Column(
            controls=[
                ft.Row([self.parameter_container(parameter) for parameter in self.offense]),
                ft.Row([self.parameter_container(parameter) for parameter in self.defense]),
                ft.Row([self.parameter_container(parameter) for parameter in self.runs]),
            ]
        )
    
    def parameter_container(self, parameter):
        return ft.Container(
            content=self.input_value(parameter),
            border=ft.border.all(1, ft.colors.BLUE_800),
            width = 150,
            height = 50,
            padding=5,
            margin=5
        )
    
    def input_value(self, parameter):
        initial_value = ft.Text(value="0")
        
        def increment(e):
            current_value = int(initial_value.value)
            initial_value.value = str(current_value + 1)
            self.update()
            self.calculate(None)
        
        def decrement(e):
            current_value = int(initial_value.value)
            initial_value.value = str(max(0, current_value - 1)) 
            self.update()
            self.calculate(None)
        
        return ft.Row(
            [
                ft.Text(value=parameter),
                ft.IconButton(icon=ft.icons.REMOVE, on_click=decrement),
                initial_value,
                ft.IconButton(icon=ft.icons.ADD, on_click=increment),
            ]
        )
    
    # マネージャー倍率
    def create_multipliers(self):
        multipliers = ["1", "1.2", "1.3", "1.6"]

        self.multipliers_box = [ft.Dropdown(width=150, height=50,
                                        options=[ft.dropdown.Option(value) for value in multipliers],
                                        value="1", on_change=self.calculate,
                                        label=lab) for lab in self.labels]
        
        return ft.Column(
            controls=[
                ft.Row(controls=[*self.multipliers_box])
            ]
        )
    
    # 員多亜熱闘
    def internettou(self,e):
        self._is_internettou = not self._is_internettou
        self.internettou_button.style = ft.ButtonStyle(
            bgcolor=ft.colors.RED_700 if self._is_internettou else None,
            color=ft.colors.WHITE70 if self._is_internettou else None
        )
        self.internettou_button.update()
        self.calculate(None)

    # Hard
    def hard(self,e):
        self._is_hard = not self._is_hard
        self.hard_button.style = ft.ButtonStyle(
            bgcolor=ft.colors.RED_700 if self._is_hard else None,
            color=ft.colors.WHITE70 if self._is_hard else None
        )
        self.hard_button.update()
        self.calculate(None)
    
    # 経験点出力
    def create_result_table(self):
        font_size = 30
        column_width = 105
        self.result_cells = [ft.Text(value="0", text_align="center",size=font_size) for _ in self.labels]
        
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Container(ft.Text(label, color=ft.colors.WHITE, size=font_size), width=column_width)) 
                for label in self.labels],
            rows=[
                ft.DataRow(cells=[ft.DataCell(cell) for cell in self.result_cells])
            ],
            border=ft.border.all(1, ft.colors.GREY_400),
            horizontal_lines=ft.border.BorderSide(1, ft.colors.GREY_400),
            vertical_lines=ft.border.BorderSide(1, ft.colors.GREY_400),
            heading_row_color=ft.colors.GREEN_700,
            data_row_color=ft.colors.GREEN_100,
        )
    
    
    def calculate(self, e):
        parameter_values = {}
        for row in self.text.controls:
            for container in row.controls:
                row_content = container.content
                parameter = row_content.controls[0].value
                value = int(row_content.controls[2].value)
                parameter_values[parameter] = value
        
        sh = parameter_values[self.offense[0]]
        dh = parameter_values[self.offense[1]]
        th = parameter_values[self.offense[2]]
        hr = parameter_values[self.offense[3]]
        sab = parameter_values[self.offense[4]]
        saf = parameter_values[self.offense[5]]
        stb = parameter_values[self.offense[6]]
        st = parameter_values[self.defense[0]]
        fb = parameter_values[self.defense[1]]
        bb = parameter_values[self.defense[2]]
        so = parameter_values[self.defense[3]]
        fo = parameter_values[self.defense[4]]
        go = parameter_values[self.defense[5]]
        dp = parameter_values[self.defense[6]]
        rd = parameter_values[self.runs[0]]
        run = parameter_values[self.runs[1]]

        power = 3*sh + 7*dh + 8*th + 10*hr + 0*sab + 3*saf + 2*stb + 3*st + 7*fb + 3*bb + 5*so + 4*fo + 2*go + 3*dp
        agile = 3*sh + 8*dh + 10*th + 0*hr + 4*sab + 5*saf + 8*stb + 1*st + 2*fb + 1*bb + 1*so + 5*fo + 2*go + 10*dp
        tech = 4*sh + 5*dh + 5*th + 5*hr + 4*sab + 3*saf + 2*stb + 1*st + 3*fb + 1*bb + 5*so + 4*fo + 6*go + 10*dp
        braking = 0*sh + 0*dh + 0*th + 0*hr + 0*sab + 0*saf + 0*stb + 3*st + 0*fb + 3*bb + 5*so + 2*fo + 4*go + 5*dp
        spilit = 2*sh + 5*dh + 8*th + 9*hr + 5*sab + 9*saf + 0*stb + 3*st + 5*fb + 3*bb + 9*so + 6*fo + 8*go + 10*dp

        points = [power, agile, tech, braking, spilit]
        points = np.array(points)*(1+rd*0.1)*((100-run*6)/100)
        if self._is_internettou:
            points = 1.3*points
        else:
            pass
        if self._is_hard:
            points = 1.2*points
        else:
            pass
        multipliers = [float(dropdown.value) for dropdown in self.multipliers_box]
        results = [int(p * m) for p, m in zip(points, multipliers)]
        
        # 結果を表示
        for i, result in enumerate(results):
            self.result_cells[i].value = str(result)
        self.update()    
    
    # リセットボタン
    def reset(self, e):
        # 行動点をリセット
        for row in self.text.controls:
            for container in row.controls:
                row_content = container.content
                row_content.controls[2].value = "0"
        # 倍率をリセット
        for dropdown in self.multipliers_box:
            dropdown.value = "1"  
        # 結果をリセット
        for cell in self.result_cells:
            cell.value = "0"  
        
        self.update()
