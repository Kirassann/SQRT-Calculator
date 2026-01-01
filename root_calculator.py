
from math import copysign, isclose
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

Window.size = (480, 760)

KV = '''
<RootCalc>:
    orientation: 'vertical'
    padding: dp(20)
    spacing: dp(16)
    canvas.before:
        Color:
            rgba: (0.06, 0.08, 0.12, 1) # темный фон
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        size_hint_y: None
        height: dp(120)
        canvas.before:
            Color:
                rgba: (0.15, 0.54, 0.86, 1)
            RoundedRectangle:
                pos: self.x, self.y
                size: self.width, self.height
                radius: [18,]
        padding: dp(14)
        spacing: dp(12)
        Label:
            text: "Калькулятор корней"
            color: 1,1,1,1
            font_size: '20sp'
            bold: True
            halign: 'left'
            valign: 'middle'
            text_size: self.size

    GridLayout:
        cols:1
        size_hint_y: None
        height: dp(220)
        spacing: dp(10)

        BoxLayout:
            size_hint_y: None
            height: dp(56)
            spacing: dp(8)
            TextInput:
                id: number_input
                hint_text: "Число (напр. 27 или -8)"
                multiline: False
                input_filter: None
                font_size: '18sp'
                padding: [12,12]
            TextInput:
                id: degree_input
                hint_text: "Степень n (напр. 3)"
                multiline: False
                input_filter: 'int'
                font_size: '18sp'
                padding: [12,12]

        BoxLayout:
            size_hint_y: None
            height: dp(56)
            spacing: dp(8)
            Button:
                id: calc_btn
                text: "Вычислить"
                font_size: '18sp'
                on_release: root.on_calculate()
                background_normal: ''
                background_color: (0.2, 0.6, 0.95, 1)
            Button:
                text: "Очистить"
                font_size: '18sp'
                on_release: root.on_clear()
                background_normal: ''
                background_color: (0.2, 0.2, 0.25, 1)

        Label:
            id: hint
            text: root.hint_text
            color: 1,1,1,0.8
            size_hint_y: None
            height: dp(28)
            font_size: '13sp'
            halign: 'left'
            valign: 'middle'
            text_size: self.size

    RelativeLayout:
        size_hint_y: 1
        canvas.before:
            Color:
                rgba: (0.06, 0.08, 0.12, 1)
            Rectangle:
                pos: self.pos
                size: self.size

        BoxLayout:
            id: result_card
            size_hint: (0.92, None)
            height: dp(180)
            pos_hint: {"center_x": 0.5, "center_y": 0.6}
            orientation: 'vertical'
            padding: dp(14)
            spacing: dp(10)
            canvas.before:
                Color:
                    rgba: (0.06, 0.12, 0.22, 0.98)
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [16,]
                Color:
                    rgba: (1,1,1,0.04)
                Rectangle:
                    pos: self.x, self.y + self.height - dp(2)
                    size: self.width, dp(1)

            Label:
                text: "Результат"
                color: 1,1,1,0.9
                font_size: '16sp'
                size_hint_y: None
                height: dp(28)
            Label:
                id: result_label
                text: root.result_text
                color: 0.95, 0.95, 0.95, 1
                font_size: '30sp'
                bold: True
                halign: 'center'
                valign: 'middle'
                text_size: self.size
            Label:
                id: info_label
                text: root.info_text
                color: 1,1,1,0.7
                font_size: '13sp'
                halign: 'center'
                valign: 'middle'
                text_size: self.size
'''

class RootCalc(BoxLayout):
    result_text = StringProperty("—")
    info_text = StringProperty("Введите число и степень, затем нажмите «Вычислить»")
    hint_text = StringProperty("Поддерживается вещественный корень. Для отрицательных чисел допускается нечётная степень.")

    def on_clear(self):
        self.ids.number_input.text = ""
        self.ids.degree_input.text = ""
        self.result_text = "—"
        self.info_text = "Очищено"
        # Легкая анимация очистки
        anim = Animation(opacity=0.2, d=0.12) + Animation(opacity=1, d=0.12)
        anim.start(self.ids.result_card)

    def on_calculate(self):
        btn = self.ids.calc_btn
        press = Animation(scale=0.98, d=0.06) + Animation(scale=1.0, d=0.12)
        press = Animation(opacity=0.85, d=0.06) + Animation(opacity=1.0, d=0.12)
        press.start(btn)

        num_text = self.ids.number_input.text.strip()
        deg_text = self.ids.degree_input.text.strip()
        if not num_text or not deg_text:
            self._show_error("Введите и число, и степень n.")
            return

        try:
            x = float(num_text)
        except ValueError:
            self._show_error("Неверный формат числа.")
            return

        try:
            n = int(deg_text)
        except ValueError:
            self._show_error("Степень n должна быть целым числом.")
            return

        if n == 0:
            self._show_error("Степень n не может быть 0.")
            return
        try:
            root = self._nth_root(x, n)
        except ValueError as e:
            self._show_error(str(e))
            return
        if isclose(root, round(root), rel_tol=1e-12):
            disp = str(int(round(root)))
        else:
            disp = f"{root:.10g}" 

        self.result_text = disp
        self.info_text = f"{n}-ый корень из {x} ≈ {disp}"
        card = self.ids.result_card
        card.y -= 16
        anim = Animation(y=card.y + 16, d=0.28, t='out_back') # выезд
        anim &= Animation(opacity=1.0, d=0.28)
        anim.start(card)
        lbl = self.ids.result_label
        a = Animation(color=(1,1,1,0.0), d=0.12) + Animation(color=(1,1,1,1), d=0.28)
        a.start(lbl)

    def _show_error(self, message):
        self.result_text = "—"
        self.info_text = "Ошибка: " + message
        card = self.ids.result_card
        anim = Animation(x=card.x - 10, d=0.03) + Animation(x=card.x + 10, d=0.03)
        anim += Animation(x=card.x, d=0.03)
        anim.start(card)

    def _nth_root(self, x: float, n: int) -> float:
        if x >= 0:
            return x ** (1.0 / n)
        else:
            if n % 2 == 1:
                # отрицательный корень для нечётной степени
                return - (abs(x) ** (1.0 / n))
            else:
                raise ValueError("Чётная степень от отрицательного числа даёт комплексное значение (не поддерживается).")

class RootApp(App):
    def build(self):
        self.title = "RootCalculator — Kivy"
        Builder.load_string(KV)
        return RootCalc()

if __name__ == '__main__':
    RootApp().run()
