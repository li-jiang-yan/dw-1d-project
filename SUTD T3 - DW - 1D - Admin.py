from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button 
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.image import Image, AsyncImage
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.config import Config
from libdw import pyrebase
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

url = "https://dfirebase-itemlist.firebaseio.com/"
apikey = "AIzaSyCLHh59akyNalglHiidchrLOKsXBU32A9E"

config = {
    "apiKey": apikey,
    "databaseURL": url,
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

root = db.child("/").get()
item_dict = root.val()
# Set application to maximized window
Config.set('graphics', 'window_state', 'maximized')

def list_of_item_objects():
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    root = db.child("/").get()
    item_dict = root.val()
    my_list_of_item_objects = []
    for item in item_dict:
        my_list_of_item_objects.append(Drink(item_dict[item][0], item_dict[item][1], item_dict[item][2]))
    return my_list_of_item_objects

# Create main Admin app that consists of a build method
class Admin(App):
    def build(self):
        sm = ScreenManager()
        
        # Child widgets of sm are Login Screen, Menu Screen
        # Consumer App Management Screen and Purchase History Screen
        '''ls = LoginScreen(name = 'login')
        ms = MenuScreen(name = 'menu')'''
        cams = ConsumerAppManagement(name = 'manage')
        '''phs = PurchaseHistory(name = 'history')'''
        
        for screens in [cams]:
            sm.add_widget(screens)
        
        sm.current = 'manage'
        return sm

'''
# Create Login Screen
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        
        self.layout = FloatLayout()
        
        # Child widgets of the Login Screen are Image and Login Panel
        self.login_img = AsyncImage()
        self.login_panel = BoxLayout()
        self.login_panel.orientation = 'vertical'
        self.login_img.source = 'https://images.mentalfloss.com/sites/default/files/styles/mf_image_16x9/public/549585-istock-909106260.jpg?itok=ds7LqH1N&resize=1100x1100'
        login_img_percent = 0.6
        self.login_img.size_hint = (login_img_percent, 1)
        self.login_img.pos_hint = {'x': 0, 'y': 0}
        self.login_img.allow_stretch = True
        self.login_img.keep_ratio = False
        self.login_panel.size_hint = (1 - login_img_percent, 1)
        self.login_panel.pos_hint = {'x': login_img_percent, 'y': 0}
        
        # Child widgets of Login Panel are Admin Login Label, Username Label,
        # Username Input, Password Label, Password Input, Button Layout,
        # Forget Label, Creators Label
        self.adminlogin_lbl = Label()
        self.username_lbl = Label()
        self.username_inp = TextInput()
        self.password_lbl = Label()
        self.password_inp = TextInput()
        self.btn_layout = BoxLayout()
        self.btn_layout.orientation = 'horizontal'
        self.forget_lbl = Label()
        self.credits_lbl = Label()
        
        # Child widgets of Button Layout are Sign In Button and Quit Button
        self.signin_btn = Button()
        self.quit_btn = Button()
        self.signin_btn.text = 'Sign In'
        self.quit_btn.text = 'Quit App'
        self.signin_btn.bind(on_press = self.login)
        self.quit_btn.bind(on_press = App.get_running_app().stop)
        for btn_widgets in [self.signin_btn,
                            self.quit_btn]:
            self.btn_layout.add_widget(btn_widgets)
        
        # Add text to the child widgets
        self.adminlogin_lbl.text = 'Admin Login'
        self.username_lbl.text = 'Username:'
        self.password_lbl.text = 'Password:'
        self.forget_lbl.text = 'If you have forgotten your password, please contact IT Support.'
        # The creators_group_tag and creators_names are global variables defined
        # in lines XX
        self.credits_lbl.text = creators_group_tag + '\n' + creators_names
        
        # Set multiline of Username and Password Inputs to False
        self.username_inp.multiline = False
        self.password_inp.multiline = False
        
        # Set font size of Label and Button child widgets
        self.adminlogin_lbl.font_size = 24
        self.credits_lbl.font_size = 14
                
        # The font size of text in Username Label, Username Input,
        # Password Label, Password Input, Sign In Button, Quit Button
        # and Forget Label are 18
        for eachWidget in [self.username_lbl,
                           self.username_inp,
                           self.password_lbl,
                           self.password_inp,
                           self.signin_btn,
                           self.quit_btn,
                           self.forget_lbl]:
            eachWidget.font_size = 18
        
        # Set all text in Admin Login Label, Username Label, Password Label,
        # Sign In Button, Quit Button to bold font
        for eachWidget in [self.adminlogin_lbl,
                           self.username_lbl,
                           self.password_lbl,
                           self.signin_btn,
                           self.quit_btn]:
            eachWidget.bold = True
        
        # Mask the characters entered into Password Input
        self.password_inp.password = True
        
        # Set the sizes and positions of Admin Login Label, Username Label,
        # Username Input, Password Lael, Password Input, Sign In Button,
        # Quit Button, Forget Label, Credits Label
        
        for login_panel_child in [self.adminlogin_lbl,
                                  self.username_lbl,
                                  self.username_inp,
                                  self.password_lbl,
                                  self.password_inp,
                                  self.btn_layout,
                                  self.forget_lbl,
                                  self.credits_lbl]:
            login_panel_child.pos_hint = {'x': 0.025}
            login_panel_child.size_hint[0] = 0.95
                
        for login_panel_child in [self.adminlogin_lbl,
                                  self.username_lbl,
                                  self.username_inp,
                                  self.password_lbl,
                                  self.password_inp,
                                  Label(),
                                  self.btn_layout,
                                  self.forget_lbl,
                                  self.credits_lbl]:
            self.login_panel.add_widget(login_panel_child)

        for LoginScreenLayout_child in [self.login_img,
                                        self.login_panel]:
            self.layout.add_widget(LoginScreenLayout_child)

        self.add_widget(self.layout)
        
    def login(self, value):
        # If correct username and password are given
        if (self.username_inp.text, self.password_inp.text) == ('Admin', 'Password'):
            self.manager.current = 'menu'
        
        # If incorrect username and password are given
        else:
            login_popup = myPopUp()
            login_popup.set_message('Incorrect username/password. Please try again later.')
            login_popup.set_dismiss_message('Dismiss')
            login_popup.set_size(0.9, 0.2)
            login_popup.set_title('Incorrect Password')
            login_popup.getPopUp()
        
        # Empty username and password fields
        self.username_inp.text = ''
        self.password_inp.text = ''

# Create Menu Screen
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        
        self.layout = BoxLayout()
        self.layout.orientation = 'vertical'
        
        # Child widgets of the Menu Screen are Welcome Message, Back to Login
        # Page Button, Menu Sublayout and Credits Label
        self.welcome_msg = Label()
        self.to_ls_btn = Button()
        self.menu_sublayout = BoxLayout()
        self.menu_sublayout.orientation = 'horizontal'
        self.credits_lbl = Label()
        
        # Child widgets of Menu Sublayout are Menu Ssublayout 1 and Menu
        # Ssublayout 2
        self.menu_ssublayout1 = BoxLayout()
        self.menu_ssublayout2 = BoxLayout()
        self.menu_ssublayout1.orientation = 'vertical'
        self.menu_ssublayout2.orientation = 'vertical'
        for menu_ssublayout in [self.menu_ssublayout1,
                                self.menu_ssublayout2]:
            self.menu_sublayout.add_widget(menu_ssublayout)
        
        # Child widgets of Menu Ssublayout 1 are XXX and Menu Management Button
        self.to_cams_btn = Button()
        self.to_cams_btn.text = 'Menu Management'
        self.to_cams_btn.bind(on_press = self.change_to_cams)
        for mssl1_child in [self.to_cams_btn]:
            self.menu_ssublayout1.add_widget(mssl1_child)
        
        # Child widgets of Menu Ssublayout 2 are XXX and Purchase History Button
        self.to_phs_btn = Button()
        self.to_phs_btn.text = 'Purchase History'
        self.to_phs_btn.bind(on_press = self.change_to_phs)
        for mssl2_child in [self.to_phs_btn]:
            self.menu_ssublayout2.add_widget(mssl2_child)
        
        # Add text to the Label and Button child widgets
        self.welcome_msg.text = 'Welcome back, ' + 'User' + '!'
        self.to_ls_btn.text = 'Back to Login Page'
        # The creators_group_tag and creators_names are global variables defined
        # in lines XX
        self.credits_lbl.text = creators_group_tag + ' - ' + creators_names
        
        # Set font size of Label and Button child widgets
        # The font size of text in Welcome Message, Back to Login Page Button
        # are 18
        for menu_child in [self.welcome_msg,
                           self.to_ls_btn]:
            menu_child.font_size = 18
        self.credits_lbl.font_size = 16
        
        # Set widget size of Welcome Message, Back to Login Page Button, 
        # Menu Sublayout and Credits Label
        self.welcome_msg.size_hint = (1, 0.1)
        self.to_ls_btn.size_hint = (1, 0.1)
        self.menu_sublayout.size_hint = (1, 0.7)
        self.credits_lbl.size_hint = (1, 0.1)
        
        # Set the callback functions for the Buttons
        self.to_ls_btn.bind(on_press = self.change_to_login)
        
        for menu_child in [self.welcome_msg,
                           self.to_ls_btn,
                           self.menu_sublayout,
                           self.credits_lbl]:
            self.layout.add_widget(menu_child)
        
        self.add_widget(self.layout)
    
    def change_to_login(self, value):
        self.manager.current = 'login'
        
    def change_to_cams(self, value):
        self.manager.current = 'manage'
    
    def change_to_phs(self, value):
        self.manager.current = 'history'
'''
# Create Consumer App Management Screen
class ConsumerAppManagement(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.layout = BoxLayout()
        self.layout.orientation = 'vertical'
        # Child widgets of Consumer App Management Layout
        # are title, Inner Layout, Back to Menu Button
        # and Credits Label
        self.title_lbl = Label()
        self.title_lbl.text = 'Consumer App Management Screen'
        self.title_lbl.size_hint[1] = 0.05
        self.cams_inner_layout = BoxLayout()
        self.cams_inner_layout.orientation = 'horizontal'
        '''self.to_ms_btn = Button()
        self.to_ms_btn.size_hint[1] = 0.05
        self.to_ms_btn.text = 'Back to Menu Page'
        self.to_ms_btn.bind(on_press = self.change_to_ms)'''
        self.credits_lbl = Label()
        self.credits_lbl.text = creators_group_tag + ' - ' + creators_names
        self.credits_lbl.size_hint[1] = 0.05
        # Child widgets of Inner Layout are Add Drink Panel
        # and Preview Panel
        self.add_drink_panel = BoxLayout()
        self.add_drink_panel.orientation = 'vertical'
        self.preview_panel = BoxLayout()
        self.preview_panel.orientation = 'vertical'
        # Child widgets of Add Drink Panel are 
        # New Drink Label, Drink Reference Label,
        # Drink Reference Input, Drink Name Label,
        # Drink Name, Drink Price Label,
        # Drink Price, Drink Picture Label,
        # Drink Picture URL,
        # Submit Drink
        self.new_drink_lbl = Label()
        self.new_drink_ref_lbl = Label()
        self.new_drink_ref_inp = TextInput()
        self.new_drink_name_lbl = Label()
        self.new_drink_name_inp = TextInput()
        self.new_drink_price_lbl = Label()
        self.new_drink_price_inp = TextInput()
        self.new_drink_url_lbl = Label()
        self.new_drink_url_inp = TextInput()
        self.new_drink_submit_btn = Button()
        self.new_drink_lbl.text = 'Add New Drink'
        self.new_drink_ref_lbl.text = 'New Drink Reference:'
        self.new_drink_name_lbl.text = 'New Drink Name:'
        self.new_drink_price_lbl.text = 'New Drink Unit Price:'
        self.new_drink_url_lbl.text = 'URL to New Drink Image:'
        self.new_drink_submit_btn.text = 'Upload'
        self.new_drink_submit_btn.bind(on_press = self.upload_drink)
        for add_drink_panel_child in [self.new_drink_lbl,
                                      self.new_drink_ref_lbl,
                                      self.new_drink_ref_inp,
                                      self.new_drink_name_lbl,
                                      self.new_drink_name_inp,
                                      self.new_drink_price_lbl,
                                      self.new_drink_price_inp,
                                      self.new_drink_url_lbl,
                                      self.new_drink_url_inp,
                                      self.new_drink_submit_btn]:
            self.add_drink_panel.add_widget(add_drink_panel_child)
        for label_child in [self.title_lbl,
                            self.new_drink_lbl,
                            self.new_drink_ref_lbl,
                            self.new_drink_name_lbl,
                            self.new_drink_price_lbl,
                            self.new_drink_url_lbl,
                            self.new_drink_submit_btn,
                            self.credits_lbl]:
            label_child.bold = True
        self.title_lbl.font_size = 24
        self.new_drink_lbl.font_size = 22
        for label_child in [self.new_drink_ref_lbl,
                            self.new_drink_ref_inp,
                            self.new_drink_name_lbl,
                            self.new_drink_name_inp,
                            self.new_drink_price_lbl,
                            self.new_drink_price_inp,
                            self.new_drink_url_lbl,
                            self.new_drink_url_inp,
                            self.new_drink_submit_btn]:
            label_child.font_size = 20
        self.credits_lbl.font_size = 14
        self.my_list_of_item_objects = list_of_item_objects()
        # Child widgets of Order Screen are
        # Drinks Scroll Layout, Checkout Button,
        # Back to Menu Button
        self.item_scroll = ScrollView()
        self.item_scroll.size_hint = (1, None)
        self.item_scroll.size = (Window.width, Window.height)
        # Child widget of Drinks Scroll Layout
        # is Order Item Layout
        self.order_item_layout = BoxLayout()
        self.order_item_layout.orientation = 'vertical'
        self.order_item_layout.spacing = 10
        self.order_item_layout.size_hint_y = None
        # Child widget of Order Item Layout
        # are the Object Panels
        for index in range(len(self.my_list_of_item_objects)):
            item_object_panel = (self.my_list_of_item_objects[index]).to_drink_menu()
            item_object_panel.size_hint_y = None
            item_object_panel.height = 125
            self.order_item_layout.add_widget(item_object_panel)
        self.item_scroll.add_widget(self.order_item_layout)
        for os_children in [self.item_scroll]:
            self.preview_panel.add_widget(os_children)
        for cams_inner_child in [self.add_drink_panel]:
            self.cams_inner_layout.add_widget(cams_inner_child)
        # Child widgets of Preview Panel are
        # Preview Label, Drink Previews
        for cams_child in [self.title_lbl,
                           self.cams_inner_layout,
                           self.credits_lbl]:
            self.layout.add_widget(cams_child)
        self.add_widget(self.layout)
    '''
    def change_to_ms(self, value):
        self.manager.current = 'menu'
    '''
    def upload_drink(self, value):
        if not(self.new_drink_ref_inp.text in drink_dict):
            if self.new_drink_ref_inp.text != '':
                # is_valid_num is a function defined in lines XX
                if is_valid_num(self.new_drink_price_inp.text):
                    db.child(self.new_drink_ref_inp.text).set([self.new_drink_name_inp.text,
                            float(self.new_drink_price_inp.text),
                            self.new_drink_url_inp.text])
                    self.new_drink_ref_inp.text = ''
                    self.new_drink_name_inp.text = ''
                    self.new_drink_price_inp.text = ''
                    self.new_drink_url_inp.text = ''
                    self.my_list_of_item_objects = list_of_item_objects()
                    
                else:
                    # The myPopUp class is a class defined at lines XX
                    upload_drink_popup_3 = myPopUp()
                    upload_drink_popup_3.set_message('Invalid drink price. Please provide only numeric inputs (decimal points up to 2 d.p. allowed.)')
                    upload_drink_popup_3.set_dismiss_message('Dismiss')
                    upload_drink_popup_3.set_size(1, 0.2)
                    upload_drink_popup_3.set_title('Drink Price Invalid')
                    upload_drink_popup_3.getPopUp()
            else:
                # The myPopUp class is a class defined at lines XX
                upload_drink_popup_2 = myPopUp()
                upload_drink_popup_2.set_message('Drink Reference field empty. Please input a Drink Reference.')
                upload_drink_popup_2.set_dismiss_message('Dismiss')
                upload_drink_popup_2.set_size(1, 0.2)
                upload_drink_popup_2.set_title('Drink Reference Field Empty')
                upload_drink_popup_2.getPopUp()
        else:
            # The myPopUp class is a class defined at lines XX
            upload_drink_popup_1 = myPopUp()
            upload_drink_popup_1.set_message('Drink Reference already exists. Please give a different Drink Reference.')
            upload_drink_popup_1.set_dismiss_message('Dismiss')
            upload_drink_popup_1.set_size(1, 0.2)
            upload_drink_popup_1.set_title('Invalid Drink Reference')
            upload_drink_popup_1.getPopUp()
'''
# Create Purchase History Screen
class PurchaseHistory(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.add_widget(Label(text = 'Consumer App Management Screen'))
'''
# Since the creators footnote is to be added in multiple pages, allow it to
# be a variables that can be reused
creators_group = '18F03 1D Group 8 (10.009)'
creators_names = 'He Jiabei, Li Jiang Yan, Pung Tuck Wei, Xu Licheng'
creators_group_tag = 'Created by ' + creators_group

class myPopUp():
    def __init__(self):
        self.x_size = 1
        self.y_size = 1
        self.message = ''
        self.dismiss_message = ''
        self.popup_title = ''
    
    def set_message(self, message):
        self.message = message
    
    def set_dismiss_message(self, dismiss_message):
        self.dismiss_message = dismiss_message
    
    def set_size(self, x, y):
        self.x_size = x
        self.y_size = y
        
    def set_title(self, title):
        self.popup_title = title
    
    def getPopUp(self):
        self.content = BoxLayout()
        self.content.orientation = 'vertical'
        self.message_lbl = Label()
        self.message_lbl.text = self.message
        self.dismiss_btn = Button()
        self.dismiss_btn.text = self.dismiss_message
        for content_children in [self.message_lbl,
                                 self.dismiss_btn]:
            self.content.add_widget(content_children)
        self.popup = Popup()
        self.dismiss_btn.bind(on_press = self.popup.dismiss)
        self.popup.title = self.popup_title
        self.popup.content = self.content
        self.popup.auto_dismiss = False
        self.popup.size_hint = (self.x_size, self.y_size)
        self.popup.open()

class Drink():
    def __init__(self, name, unit_price, img_source = 'https://t6.rbxcdn.com/366352c6ff3cad3294c91c01a4209ef6'):
        self.name = name
        self.unit_price = unit_price
        self.quantity = 0
        self.subtotal = self.unit_price * self.quantity
        self.img_source = img_source
        
    def to_drink_menu(self):
        my_drink_menu = BoxLayout()
        my_drink_menu.orientation = 'horizontal'
        # Child widgets of each Drink Menu are Drink Picture,
        # Drink Details and Quantity Layout
        my_drink_pic = AsyncImage()
        my_drink_pic.source = self.img_source
        my_drink_details = BoxLayout()
        my_drink_details.orientation = 'vertical'
        # Child widgets of Drink Details are Drink Name,
        # Drink Unit Price, Drink Remarks Label,
        # Remarks Input
        my_drink_name_label = Label()
        my_drink_unit_price_label = Label()
        my_drink_remarks_label = Label()
        my_drink_name_label.text = self.name
        my_drink_unit_price_label.text = 'Unit Price: $' + format(self.unit_price, '.2f')
        my_drink_remarks_label.text = 'Remarks:'
        my_drink_remarks_input = TextInput()
        for my_drink_detail in [my_drink_name_label,
                                my_drink_unit_price_label,
                                my_drink_remarks_label,
                                my_drink_remarks_input]:
            my_drink_details.add_widget(my_drink_detail)
        my_drink_quantity_layout = BoxLayout()
        my_drink_quantity_layout.orientation = 'vertical'
        # Child widgets of Quantity Layout are Quantity Label,
        # My Quantity Label, Quantity Button Layout
        my_drink_quantity_label = Label()
        self.my_drink_my_quantity_label = Label()
        my_drink_quantity_label.text = 'Quantity'
        self.my_drink_my_quantity_label.text = '× {}'.format(self.quantity)
        my_drink_my_quantity_btn_layout = BoxLayout()
        my_drink_my_quantity_btn_layout.orientation = 'horizontal'
        # Child widgets of Quantity Button Layout are
        # Quantity Plus Button and Quantity Minus Button
        self.my_drink_my_quantity_plus_btn = Button()
        self.my_drink_my_quantity_minus_btn = Button()
        self.my_drink_my_quantity_plus_btn.text = '+'
        self.my_drink_my_quantity_minus_btn.text = '-'
        self.my_drink_my_quantity_plus_btn.bind(on_press = self.add_quantity)
        self.my_drink_my_quantity_minus_btn.bind(on_press = self.dec_quantity)
        for quantity_btn_layout_children in [self.my_drink_my_quantity_plus_btn,
                                             self.my_drink_my_quantity_minus_btn]:
            my_drink_my_quantity_btn_layout.add_widget(quantity_btn_layout_children)
        for quantity_layout_children in [my_drink_quantity_label,
                                         self.my_drink_my_quantity_label,
                                         my_drink_my_quantity_btn_layout]:
            my_drink_quantity_layout.add_widget(quantity_layout_children)
        for drink_menu_children in [my_drink_pic,
                                    my_drink_details,
                                    my_drink_quantity_layout]:
            my_drink_menu.add_widget(drink_menu_children)
        return my_drink_menu
    
    def update_quantity(self):
        self.my_drink_my_quantity_label.text = '× {}'.format(self.quantity)
    
    def add_quantity(self, instance):
        self.quantity += 1
        print('quantity: {}'.format(self.quantity))
        self.update_quantity()
    
    def dec_quantity(self, instance):
        print('quantity: {}'.format(self.quantity))
        if self.quantity > 0:
            self.quantity -= 1
        self.update_quantity()
    
    def my_subtotal(self):
        return self.quantity * self.unit_price

def is_valid_num(string):
    if string == '': # String cannot be empty
        return False
    elif string.isdigit():
        return True
    else:
        if string.count('.') == 1 and len(string) > 1:
            for char in string:
                if not(char in ['0', '1', '2', '3', '4', '5',
                                '6', '7', '8', '9', '.']):
                    return False
            if string.find('.') < len(string) - 3:
                return False
            if float(string) < 0:
                return False
            return True
        else:
            return False

def itemListUpdate():
    global db
    global drink_dict
    root = db.child("/").get()
    drink_dict = root.val()
    print(drink_dict)


# Allow continuous running of app
if __name__ == '__main__':
    Admin().run()