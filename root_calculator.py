from math import copysign, isclose
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.metrics import sp

Window.size = (480, 760)

KV = '''
<RootCalc>:
    orientation: 'vertical'
    padding: 0
    spacing: 0
    canvas.before:
        Color:
            rgba: (0.02, 0.02, 0.05, 1)  # Deep dark background
        Rectangle:
            pos: self.pos
            size: self.size
        # Scanline effect
        Color:
            rgba: (0, 1, 0.8, 0.02)
        Rectangle:
            pos: self.x, self.y
            size: self.width, dp(2)
        Rectangle:
            pos: self.x, self.y + dp(200)
            size: self.width, dp(2)
        Rectangle:
            pos: self.x, self.y + dp(400)
            size: self.width, dp(2)

    # Top terminal-style header
    BoxLayout:
        size_hint_y: None
        height: dp(70)
        padding: [dp(20), dp(16), dp(20), dp(16)]
        canvas.before:
            Color:
                rgba: (0.05, 0.05, 0.12, 1)
            Rectangle:
                pos: self.pos
                size: self.size
            # Neon top border
            Color:
                rgba: (0, 1, 0.6, 0.8)
            Rectangle:
                pos: self.x, self.y + self.height - dp(2)
                size: self.width, dp(2)
            # Bottom glow
            Color:
                rgba: (0, 1, 0.6, 0.3)
            Rectangle:
                pos: self.x, self.y + self.height - dp(4)
                size: self.width, dp(4)
        
        BoxLayout:
            orientation: 'horizontal'
            spacing: dp(12)
            
            Label:
                text: "█"
                color: (0, 1, 0.6, 1)
                font_size: '24sp'
                size_hint_x: None
                width: dp(30)
            
            BoxLayout:
                orientation: 'vertical'
                spacing: dp(2)
                Label:
                    text: "ROOT_CALC.EXE"
                    color: (0, 1, 0.6, 1)
                    font_size: '18sp'
                    bold: True
                    halign: 'left'
                    valign: 'bottom'
                    text_size: self.size
                    font_name: 'RobotoMono-Regular'
                Label:
                    text: "made by kirassan,tgc:@kirassan_jojosan"
                    color: (0, 0.8, 0.5, 0.6)
                    font_size: '11sp'
                    halign: 'left'
                    valign: 'top'
                    text_size: self.size
                    font_name: 'RobotoMono-Regular'

    # Main content area
    BoxLayout:
        orientation: 'vertical'
        padding: [dp(20), dp(24), dp(20), dp(20)]
        spacing: dp(20)

        # Input section
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: dp(200)
            spacing: dp(16)
            
            # Title with glitch effect
            Label:
                text: "> QUANTUM_ROOT_EXTRACTION"
                color: (0, 1, 0.8, 0.9)
                font_size: '15sp'
                size_hint_y: None
                height: dp(28)
                halign: 'left'
                valign: 'middle'
                text_size: self.size
                font_name: 'RobotoMono-Regular'
                canvas.before:
                    Color:
                        rgba: (0, 1, 0.8, 0.1)
                    Rectangle:
                        pos: self.x - dp(4), self.y
                        size: dp(4), self.height

            # Input fields with hacker styling
            BoxLayout:
                size_hint_y: None
                height: dp(54)
                spacing: dp(12)
                
                BoxLayout:
                    orientation: 'vertical'
                    spacing: dp(4)
                    
                    Label:
                        text: "[ VALUE ]"
                        color: (0.4, 0.9, 1, 0.7)
                        font_size: '11sp'
                        size_hint_y: None
                        height: dp(16)
                        halign: 'left'
                        valign: 'middle'
                        text_size: self.size
                        font_name: 'RobotoMono-Regular'
                    
                    TextInput:
                        id: number_input
                        hint_text: "enter number..."
                        multiline: False
                        input_filter: None
                        font_size: '16sp'
                        padding: [12, 8]
                        background_normal: ''
                        background_color: (0.08, 0.12, 0.18, 0.9)
                        foreground_color: (0, 1, 0.7, 1)
                        hint_text_color: (0, 1, 0.7, 0.4)
                        cursor_color: (0, 1, 0.7, 1)
                        font_name: 'RobotoMono-Regular'
                        canvas.before:
                            Color:
                                rgba: (0, 1, 0.7, 0.3)
                            Line:
                                rectangle: (self.x, self.y, self.width, self.height)
                                width: 1.2
                
                BoxLayout:
                    orientation: 'vertical'
                    spacing: dp(4)
                    size_hint_x: 0.4
                    
                    Label:
                        text: "[ DEGREE ]"
                        color: (0.4, 0.9, 1, 0.7)
                        font_size: '11sp'
                        size_hint_y: None
                        height: dp(16)
                        halign: 'left'
                        valign: 'middle'
                        text_size: self.size
                        font_name: 'RobotoMono-Regular'
                    
                    TextInput:
                        id: degree_input
                        hint_text: "n"
                        multiline: False
                        input_filter: 'int'
                        font_size: '16sp'
                        padding: [12, 8]
                        background_normal: ''
                        background_color: (0.08, 0.12, 0.18, 0.9)
                        foreground_color: (0, 1, 0.7, 1)
                        hint_text_color: (0, 1, 0.7, 0.4)
                        cursor_color: (0, 1, 0.7, 1)
                        font_name: 'RobotoMono-Regular'
                        canvas.before:
                            Color:
                                rgba: (0, 1, 0.7, 0.3)
                            Line:
                                rectangle: (self.x, self.y, self.width, self.height)
                                width: 1.2

            # Buttons with cyberpunk style
            BoxLayout:
                size_hint_y: None
                height: dp(52)
                spacing: dp(12)
                
                Button:
                    id: calc_btn
                    text: "[ EXECUTE ]"
                    font_size: '16sp'
                    on_release: root.on_calculate()
                    background_normal: ''
                    background_color: (0, 0, 0, 0)
                    color: (0, 1, 0.6, 1)
                    bold: True
                    font_name: 'RobotoMono-Regular'
                    canvas.before:
                        Color:
                            rgba: (0, 1, 0.6, 0.15)
                        Rectangle:
                            pos: self.pos
                            size: self.size
                        Color:
                            rgba: (0, 1, 0.6, 0.7)
                        Line:
                            rectangle: (self.x, self.y, self.width, self.height)
                            width: 1.8
                        # Glow effect
                        Color:
                            rgba: (0, 1, 0.6, 0.3)
                        Line:
                            rectangle: (self.x - 2, self.y - 2, self.width + 4, self.height + 4)
                            width: 2
                
                Button:
                    text: "[ CLEAR ]"
                    font_size: '16sp'
                    on_release: root.on_clear()
                    background_normal: ''
                    background_color: (0, 0, 0, 0)
                    color: (1, 0.3, 0.4, 1)
                    bold: True
                    font_name: 'RobotoMono-Regular'
                    size_hint_x: 0.5
                    canvas.before:
                        Color:
                            rgba: (1, 0.2, 0.3, 0.12)
                        Rectangle:
                            pos: self.pos
                            size: self.size
                        Color:
                            rgba: (1, 0.2, 0.3, 0.6)
                        Line:
                            rectangle: (self.x, self.y, self.width, self.height)
                            width: 1.5

            # Hint text
            Label:
                id: hint
                text: root.hint_text
                color: (0.3, 0.8, 0.9, 0.6)
                size_hint_y: None
                height: dp(36)
                font_size: '11sp'
                halign: 'left'
                valign: 'middle'
                text_size: self.size
                font_name: 'RobotoMono-Regular'

        # Result display - Matrix style
        RelativeLayout:
            size_hint_y: 1

            BoxLayout:
                id: result_card
                size_hint: (1, None)
                height: dp(260)
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                orientation: 'vertical'
                padding: 0
                spacing: 0
                canvas.before:
                    # Main card background
                    Color:
                        rgba: (0.03, 0.06, 0.12, 0.95)
                    Rectangle:
                        pos: self.pos
                        size: self.size
                    # Neon border
                    Color:
                        rgba: (0, 1, 0.8, 0.5)
                    Line:
                        rectangle: (self.x, self.y, self.width, self.height)
                        width: 2
                    # Outer glow
                    Color:
                        rgba: (0, 1, 0.8, 0.2)
                    Line:
                        rectangle: (self.x - 3, self.y - 3, self.width + 6, self.height + 6)
                        width: 3
                    # Corner brackets
                    Color:
                        rgba: (0, 1, 0.8, 0.8)
                    Line:
                        points: [self.x, self.y + dp(20), self.x, self.y, self.x + dp(20), self.y]
                        width: 2.5
                    Line:
                        points: [self.right - dp(20), self.y, self.right, self.y, self.right, self.y + dp(20)]
                        width: 2.5
                    Line:
                        points: [self.x, self.top - dp(20), self.x, self.top, self.x + dp(20), self.top]
                        width: 2.5
                    Line:
                        points: [self.right - dp(20), self.top, self.right, self.top, self.right, self.top - dp(20)]
                        width: 2.5

                # Header bar
                BoxLayout:
                    size_hint_y: None
                    height: dp(50)
                    padding: [dp(16), dp(12)]
                    canvas.before:
                        Color:
                            rgba: (0, 1, 0.8, 0.08)
                        Rectangle:
                            pos: self.pos
                            size: self.size
                        Color:
                            rgba: (0, 1, 0.8, 0.3)
                        Rectangle:
                            pos: self.x, self.y
                            size: self.width, dp(1)
                    
                    Label:
                        text: ">>> OUTPUT_STREAM"
                        color: (0, 1, 0.8, 0.8)
                        font_size: '13sp'
                        halign: 'left'
                        valign: 'middle'
                        text_size: self.size
                        font_name: 'RobotoMono-Regular'
                    
                    Label:
                        id: status_led
                        text: "●"
                        color: (0, 1, 0.5, 1)
                        font_size: '20sp'
                        size_hint_x: None
                        width: dp(30)

                # Result area
                BoxLayout:
                    orientation: 'vertical'
                    padding: [dp(20), dp(16)]
                    spacing: dp(12)
                    
                    Label:
                        text: "[ RESULT ]"
                        color: (0.5, 0.9, 1, 0.6)
                        font_size: '12sp'
                        size_hint_y: None
                        height: dp(20)
                        halign: 'center'
                        valign: 'middle'
                        text_size: self.size
                        font_name: 'RobotoMono-Regular'
                    
                    Label:
                        id: result_label
                        text: root.result_text
                        color: (0, 1, 0.7, 1)
                        font_size: '42sp'
                        bold: True
                        halign: 'center'
                        valign: 'middle'
                        text_size: self.size
                        font_name: 'RobotoMono-Regular'
                        canvas.before:
                            Color:
                                rgba: (0, 1, 0.7, 0.15)
                            Rectangle:
                                pos: self.center_x - dp(100), self.center_y - dp(2)
                                size: dp(200), dp(4)
                    
                    BoxLayout:
                        size_hint_y: None
                        height: dp(60)
                        padding: [dp(12), 0]
                        canvas.before:
                            Color:
                                rgba: (0, 1, 0.8, 0.05)
                            Rectangle:
                                pos: self.pos
                                size: self.size
                        
                        Label:
                            id: info_label
                            text: root.info_text
                            color: (0.4, 0.9, 1, 0.8)
                            font_size: '12sp'
                            halign: 'center'
                            valign: 'middle'
                            text_size: self.size
                            font_name: 'RobotoMono-Regular'

    # Bottom status bar
    BoxLayout:
        size_hint_y: None
        height: dp(32)
        padding: [dp(16), 0]
        canvas.before:
            Color:
                rgba: (0.05, 0.05, 0.12, 1)
            Rectangle:
                pos: self.pos
                size: self.size
            Color:
                rgba: (0, 1, 0.6, 0.5)
            Rectangle:
                pos: self.x, self.top - dp(1)
                size: self.width, dp(1)
        
        Label:
            text: "STATUS: READY"
            color: (0, 1, 0.6, 0.7)
            font_size: '10sp'
            halign: 'left'
            valign: 'middle'
            text_size: self.size
            font_name: 'RobotoMono-Regular'
        
        Label:
            text: "UPTIME: ∞"
            color: (0, 1, 0.6, 0.5)
            font_size: '10sp'
            halign: 'right'
            valign: 'middle'
            text_size: self.size
            font_name: 'RobotoMono-Regular'
'''

class RootCalc(BoxLayout):
    result_text = StringProperty("—")
    info_text = StringProperty(">>> AWAITING INPUT...")
    hint_text = StringProperty("> Supports real roots | Odd degrees allow negative values")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self._blink_led, 1.2)

    def _blink_led(self, dt):
        """LED blinking animation"""
        led = self.ids.get('status_led')
        if led:
            anim = Animation(opacity=0.3, duration=0.6) + Animation(opacity=1.0, duration=0.6)
            anim.start(led)

    def on_clear(self):
        self.ids.number_input.text = ""
        self.ids.degree_input.text = ""
        self.result_text = "—"
        self.info_text = ">>> MEMORY CLEARED"
        
        # Glitch effect on clear
        card = self.ids.result_card
        anim = Animation(x=card.x - 5, duration=0.05)
        anim += Animation(x=card.x + 5, duration=0.05)
        anim += Animation(x=card.x, duration=0.05)
        anim &= Animation(opacity=0.5, duration=0.15) + Animation(opacity=1.0, duration=0.1)
        anim.start(card)

    def on_calculate(self):
        btn = self.ids.calc_btn
        # Button press effect with glow
        press = Animation(opacity=0.6, duration=0.08) + Animation(opacity=1.0, duration=0.15)
        press.start(btn)

        num_text = self.ids.number_input.text.strip()
        deg_text = self.ids.degree_input.text.strip()
        
        if not num_text or not deg_text:
            self._show_error("ERROR: INCOMPLETE INPUT DETECTED")
            return

        try:
            x = float(num_text)
        except ValueError:
            self._show_error("ERROR: INVALID NUMBER FORMAT")
            return

        try:
            n = int(deg_text)
        except ValueError:
            self._show_error("ERROR: DEGREE MUST BE INTEGER")
            return

        if n == 0:
            self._show_error("ERROR: ZERO DEGREE NOT PERMITTED")
            return
            
        try:
            root = self._nth_root(x, n)
        except ValueError as e:
            self._show_error(f"ERROR: {str(e).upper()}")
            return
            
        if isclose(root, round(root), rel_tol=1e-12):
            disp = str(int(round(root)))
        else:
            disp = f"{root:.10g}"

        self.result_text = disp
        self.info_text = f">>> nth_root({x}, {n}) = {disp}"
        
        # Sci-fi reveal animation
        card = self.ids.result_card
        lbl = self.ids.result_label
        
        # Card animation - slide up with scale
        card.opacity = 0
        card.y -= 30
        anim = Animation(y=card.y + 30, opacity=1.0, duration=0.4, t='out_cubic')
        anim.start(card)
        
        # Text typing effect
        original_text = self.result_text
        self.result_text = ""
        
        def update_text(dt, index=[0]):
            if index[0] < len(original_text):
                self.result_text += original_text[index[0]]
                index[0] += 1
            else:
                # Pulse effect when complete (use numeric sp() values)
                pulse = Animation(font_size=sp(48), duration=0.15) + Animation(font_size=sp(42), duration=0.15)
                pulse.start(lbl)
                
        Clock.schedule_interval(lambda dt: update_text(dt), 0.05)

    def _show_error(self, message):
        self.result_text = "⚠"
        self.info_text = message
        
        # Error shake with red flash
        card = self.ids.result_card
        result_label = self.ids.result_label
        
        # Shake animation
        anim = Animation(x=card.x - 8, duration=0.05)
        anim += Animation(x=card.x + 8, duration=0.05)
        anim += Animation(x=card.x - 8, duration=0.05)
        anim += Animation(x=card.x + 8, duration=0.05)
        anim += Animation(x=card.x, duration=0.05)
        anim.start(card)
        
        # Color flash
        original_color = result_label.color
        result_label.color = (1, 0.2, 0.3, 1)
        Clock.schedule_once(lambda dt: setattr(result_label, 'color', (0, 1, 0.7, 1)), 0.3)

    def _nth_root(self, x: float, n: int) -> float:
        if x >= 0:
            return x ** (1.0 / n)
        else:
            if n % 2 == 1:
                return - (abs(x) ** (1.0 / n))
            else:
                raise ValueError("Even degree of negative number yields complex value")

class RootApp(App):
    def build(self):
        self.title = "Quantum Root Calculator - Hacker Edition"
        Builder.load_string(KV)
        return RootCalc()

if __name__ == '__main__':
    RootApp().run()