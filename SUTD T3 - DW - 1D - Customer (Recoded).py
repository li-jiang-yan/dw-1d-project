from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.image import Image, AsyncImage
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.config import Config
import time
from libdw import pyrebase
from copy import deepcopy
import qrcode

"""Item List Database"""
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

def list_of_item_objects():
    my_list_of_item_objects = []
    for item in item_dict:
        my_list_of_item_objects.append(Drink(item_dict[item][0], item_dict[item][1], item_dict[item][2]))
    return my_list_of_item_objects

"""Accounts Database"""
url2 = "https://account-ff968.firebaseio.com/"
apikey2 = "AIzaSyDSdbtBma0joUojn_Q5r6x_F8Ogv8uvvOA"

config2 = {
    "apiKey": apikey2,
    "databaseURL": url2,
}

firebase2 = pyrebase.initialize_app(config2)
db2 = firebase2.database()

root2 = db2.child("/").get()
acct_dict = root2.val()

def refreshAcctData():
    global db2
    global acct_dict
    root2 = db2.child("/").get()
    acct_dict = root2.val()

def setData(wantedKey, index, newValue):
    global db2
    global acct_dict
    myDetails = deepcopy(acct_dict[wantedKey])
    myDetails[index] = newValue
    db2.child(wantedKey).set(myDetails)
    refreshAcctData()

"""Orders Database"""
url3 = "https://dw-1d-50a70.firebaseio.com/"
apikey3 = "AIzaSyBB8D0x9rp9RkdjJtn_7jagb_hYBjKSW74"

config3 = {
    "apiKey": apikey3,
    "databaseURL": url3,
}

firebase3 = pyrebase.initialize_app(config3)
db3 = firebase3.database()

"""Some global variables and functions"""
os_ls_of_item_obj = None
os_compute_total = None

def get_os_ls_of_item_obj():
    global os_ls_of_item_obj
    return os_ls_of_item_obj

def get_os_compute_total():
    global os_compute_total
    return os_compute_total

def set_os_ls_of_item_obj(newValue):
    global os_ls_of_item_obj
    os_ls_of_item_obj = newValue

def set_os_compute_total(newValue):
    global os_compute_total
    os_compute_total = newValue

cs_order_num = None

def get_cs_order_num():
    global cs_order_num
    return cs_order_num

def set_cs_order_num(newValue):
    global cs_order_num
    cs_order_num = newValue

myKey = 'empty_user'

class Consumer(App):
    def build(self):
        sm = ScreenManager()
        ls = LoginScreen(name = 'login')
        ms = MenuScreen(name = 'menu')
        tus = TopUpScreen(name = 'topup')
        os = OrderScreen(name = 'order')
        ps = PaymentScreen(name = 'payment')
        cs = ConfirmScreen(name = 'confirm')
        for myScreen in [ls,
                         ms,
                         tus,
                         os,
                         ps,
                         cs]:
            sm.add_widget(myScreen)
        sm.current = 'login'
        return sm

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.layout = BoxLayout()
        self.layout.orientation = 'vertical'
        
        # Child widgets of the Login Screen are App Title, App Image,
        # Username Label, Username Input, Password Label, Password Input,
        # Login Button, Quit App Button
        self.app_title = Label()
        self.app_img = AsyncImage()
        self.username_lbl = Label()
        self.username_inp = TextInput()
        self.username_inp.multiline = False
        self.password_lbl = Label()
        self.password_inp = TextInput()
        self.password_inp.multiline = False
        self.login_btn = Button()
        self.quit_btn = Button()
        
        # Add text to the Label and Button child widgets
        self.app_title.text = 'Drink Stall Pre-order App'
        self.username_lbl.text = 'Username:'
        self.password_lbl.text = 'Password:'
        self.login_btn.text = 'Login'
        self.quit_btn.text = 'Quit App'
        
        # Add image source for the AsyncImage child widgets
        self.app_img.source = 'https://images.mentalfloss.com/sites/default/files/styles/mf_image_16x9/public/549585-istock-909106260.jpg?itok=ds7LqH1N&resize=1100x1100'
        self.app_img.allow_stretch = True
        self.app_img.keep_ratio = False
        
        # Bind Button child widgets to callback functions
        self.login_btn.bind(on_press = self.login)
        self.quit_btn.bind(on_press = App.get_running_app().stop)
        
        # Mask the characters entered into Password Input
        self.password_inp.password = True
        
        for ls_child_widget in [self.app_title,
                                self.username_lbl,
                                self.username_inp,
                                self.password_lbl,
                                self.password_inp,
                                self.login_btn,
                                self.quit_btn]:
            ls_child_widget.size_hint_y = 0.15
        
        for ls_child_widget in [self.app_title,
                                self.app_img,
                                self.username_lbl,
                                self.username_inp,
                                self.password_lbl,
                                self.password_inp,
                                self.login_btn,
                                self.quit_btn]:
            self.layout.add_widget(ls_child_widget)
        self.add_widget(self.layout)
    
    def login(self, value):
        if self.username_inp.text in acct_dict:
            if self.password_inp.text == acct_dict[self.username_inp.text][0]:
                setMyKey(self.username_inp.text)
                getMyKey()
                self.manager.get_screen('menu').updateKeyValues()
                self.manager.current = 'menu'
            else:
                # The myPopUp class is a class defined at lines XX
                login_popup = myPopUp()
                login_popup.set_message('Invalid username/password. Please try again.')
                login_popup.set_dismiss_message('Dismiss')
                login_popup.set_size(0.5, 0.2)
                login_popup.set_title('Incorrect Password')
                login_popup.getPopUp()
        else:
            # The myPopUp class is a class defined at lines XX
            login_popup = myPopUp()
            login_popup.set_message('Invalid username/password. Please try again.')
            login_popup.set_dismiss_message('Dismiss')
            login_popup.set_size(0.5, 0.2)
            login_popup.set_title('Incorrect Password')
            login_popup.getPopUp()
        
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.layout = BoxLayout()
        self.layout.orientation = 'vertical'
                
        # Child widgets of Menu Screen are Welcome Label, App Image,
        # Balance Statement, Top Up Credits Button
        # Place Order Button, Back to Login Menu Button
        self.welcome_lbl = Label()
        self.app_img = AsyncImage()
        self.balance_lbl = Label()
        self.to_tus_btn = Button()
        self.to_os_btn = Button()
        self.to_ls_btn = Button()
        
        # Add text to the Label and Button child widgets
        self.welcome_lbl.text = 'Welcome back, ' + myKey + '!'
        self.balance_lbl.text = 'You currently have ${:.2f} in your account.'.format(acct_dict[myKey][1])
        self.to_tus_btn.text = 'Top Up Credits'
        self.to_os_btn.text = 'Place Order'
        self.to_ls_btn.text = 'Back to Login Menu'
        
        # Add image source for the AsyncImage child widgets
        self.app_img.source = 'https://images.mentalfloss.com/sites/default/files/styles/mf_image_16x9/public/549585-istock-909106260.jpg?itok=ds7LqH1N&resize=1100x1100'
        self.app_img.allow_stretch = True
        self.app_img.keep_ratio = False
        
        # Bind button child widgets to callback functions
        self.to_tus_btn.bind(on_press = self.change_to_tus)
        self.to_os_btn.bind(on_press = self.change_to_os)
        self.to_ls_btn.bind(on_press = self.change_to_ls)
        
        for ms_child_widget in [self.welcome_lbl,
                                self.balance_lbl,
                                self.to_tus_btn,
                                self.to_os_btn,
                                self.to_ls_btn]:
            ms_child_widget.size_hint_y = 0.15
    
        for ms_child_widget in [self.welcome_lbl,
                                self.app_img,
                                self.balance_lbl,
                                self.to_tus_btn,
                                self.to_os_btn,
                                self.to_ls_btn]:
            self.layout.add_widget(ms_child_widget)
        
        self.add_widget(self.layout)
    
    def updateKeyValues(self):
        refreshAcctData()
        self.welcome_lbl.text = 'Welcome back, ' + getMyKey() + '!'
        self.balance_lbl.text = 'You currently have ${:.2f} in your account.'.format(acct_dict[getMyKey()][1])

    def change_to_tus(self, value):
        self.manager.get_screen('topup').update_instantiation()
        self.manager.current = 'topup'
      
    def change_to_os(self, value):
        self.manager.current = 'order'

    def change_to_ls(self, value):
        self.manager.current = 'login'

class TopUpScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.layout = BoxLayout()
        self.layout.orientation = 'vertical'
        # Child widgets of Top Up Screen are Top Up Title,
        # Top Up Image, Balance Label, Back Account Label,
        # Bank Account Input, Top Up Amount Label, Top Up Input,
        # Top Up Button, Back to Menu Button
        self.top_up_lbl = Label()
        self.top_up_img = AsyncImage()
        self.balance_lbl = Label()
        self.bank_acc_lbl = Label()
        self.bank_acc_inp = TextInput()
        self.bank_acc_inp.multiline = False
        self.top_up_amt_lbl = Label()
        self.top_up_amt_inp = TextInput()
        self.top_up_amt_inp.multiline = False
        self.top_up_btn = Button()
        self.to_ms_btn = Button()
        
        # Add text to the Label and Button child widgets
        self.top_up_lbl.text = 'Top Up Credits'
        self.balance_lbl.text = 'Current balance: ${:.2f}'.format(acct_dict[getMyKey()][1])
        self.bank_acc_lbl.text = 'Bank Account Number:'
        self.top_up_amt_lbl.text = 'Top Up Amount (in $):'
        self.top_up_btn.text = 'Top Up Credits'
        self.to_ms_btn.text = 'Back to Menu'
        
        # Add image source for the AsyncImage child widgets
        self.top_up_img.source = 'http://media.theindependent.sg/wp-content/uploads/2014/10/singapore-currency1.jpg'
        self.top_up_img.allow_stretch = True
        self.top_up_img.keep_ratio = False
        
        # Bind button child to callback functions
        self.top_up_btn.bind(on_press = self.topup)
        self.to_ms_btn.bind(on_press = self.change_to_ms)
        
        for tus_child_widget in [self.top_up_lbl,
                                 self.balance_lbl,
                                 self.bank_acc_lbl,
                                 self.bank_acc_inp,
                                 self.top_up_amt_lbl,
                                 self.top_up_amt_inp,
                                 self.top_up_btn,
                                 self.to_ms_btn]:
            tus_child_widget.size_hint_y = 0.15
        
        for tus_child_widget in [self.top_up_lbl,
                                 self.top_up_img,
                                 self.balance_lbl,
                                 self.bank_acc_lbl,
                                 self.bank_acc_inp,
                                 self.top_up_amt_lbl,
                                 self.top_up_amt_inp,
                                 self.top_up_btn,
                                 self.to_ms_btn]:
            self.layout.add_widget(tus_child_widget)
        
        self.add_widget(self.layout)
    
    def update_instantiation(self):
        refreshAcctData()
        self.balance_lbl.text = 'Current balance: ${:.2f}'.format(acct_dict[getMyKey()][1])

    def topup(self, value):
        # The is_valid_num function is a function defined at lines XX
        if is_valid_num(self.top_up_amt_inp.text):
            print(getMyKey())
            old_balance = acct_dict[getMyKey()][1]
            setData(getMyKey(), 1, float(self.top_up_amt_inp.text) + float(old_balance))
            self.update_instantiation()
            # The myPopUp class is a class defined at lines XX
            topup_popup_1 = myPopUp()
            topup_popup_1.set_message('Top Up Successful. Note that the app is in its beta version (unlinked to any bank accounts).')
            topup_popup_1.set_dismiss_message('Dismiss')
            topup_popup_1.set_size(1, 0.2)
            topup_popup_1.set_title('Successful Top Up')
            topup_popup_1.getPopUp()
        else:
            # The myPopUp class is a class defined at lines XX
            topup_popup_2 = myPopUp()
            topup_popup_2.set_message('Invalid top up amount input. Please provide only numeric inputs (decimal points up to 2 d.p. allowed.)')
            topup_popup_2.set_dismiss_message('Dismiss')
            topup_popup_2.set_size(1, 0.2)
            topup_popup_2.set_title('Invalid Top Up Amount')
            topup_popup_2.getPopUp()
    
    def change_to_ms(self, value):
        self.manager.get_screen('menu').updateKeyValues()
        self.manager.current = 'menu'

class OrderScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.my_list_of_item_objects = list_of_item_objects()
        self.my_list_of_item_add_func = []
        self.my_list_of_item_dec_func = []
        self.my_list_of_combined_func_add_item = []
        self.my_list_of_combined_func_dec_item = []
        for item in self.my_list_of_item_objects:
            # combined_function is an 
            # object defined in lines XX
            self.my_list_of_combined_func_add_item.append(combined_function(self.reset_shown_total, item.add_quantity))
            self.my_list_of_combined_func_dec_item.append(combined_function(self.reset_shown_total, item.dec_quantity))
        for func_pair in self.my_list_of_combined_func_add_item:
            self.my_list_of_item_add_func.append(func_pair.complex_function)
        for func_pair in self.my_list_of_combined_func_dec_item:
            self.my_list_of_item_dec_func.append(func_pair.complex_function)
        # Child widgets of Order Screen are
        # Drinks Scroll Layout, Checkout Button,
        # Back to Menu Button
        self.layout = BoxLayout()
        self.layout.orientation = 'vertical'
        self.item_scroll = ScrollView()
        self.item_scroll.size_hint = (1, None)
        self.item_scroll.size = (Window.width, Window.height)
        self.to_ps_btn = Button()
        self.to_ms_btn = Button()
        self.to_ps_btn.text = 'Total: ${:.2f}'.format(self.compute_total())
        self.to_ms_btn.text = 'Back to Menu'
        self.to_ps_btn.bind(on_press = self.change_to_ps)
        self.to_ms_btn.bind(on_press = self.change_to_ms)
        self.to_ps_btn.size_hint_y = 0.1
        self.to_ms_btn.size_hint_y = 0.1
        # Child widget of Drinks Scroll Layout
        # is Order Item Layout
        self.order_item_layout = BoxLayout()
        self.order_item_layout.orientation = 'vertical'
        self.order_item_layout.spacing = 10
        self.order_item_layout.size_hint_y = None
        self.order_item_layout.bind(minimum_height = self.order_item_layout.setter('height'))
        # Child widget of Order Item Layout
        # are the Object Panels
        for index in range(len(self.my_list_of_item_objects)):
            item_object_panel = (self.my_list_of_item_objects[index]).to_drink_menu()
            item_object_panel.size_hint_y = None
            item_object_panel.height = 125
            self.order_item_layout.add_widget(item_object_panel)
            (self.my_list_of_item_objects[index]).my_drink_my_quantity_plus_btn.bind(on_press = self.my_list_of_item_add_func[index])
            (self.my_list_of_item_objects[index]).my_drink_my_quantity_minus_btn.bind(on_press = self.my_list_of_item_dec_func[index])
            (self.my_list_of_item_objects[index]).my_drink_remarks_input.bind(text = (self.my_list_of_item_objects[index]).change_remarks)
        self.item_scroll.add_widget(self.order_item_layout)
        for os_children in [self.item_scroll,
                            self.to_ps_btn,
                            self.to_ms_btn]:
            self.layout.add_widget(os_children)
        self.add_widget(self.layout)
    
    def ls_of_item_obj(self):
        return self.my_list_of_item_objects
    
    def compute_total(self):
        my_total = 0
        for item in self.my_list_of_item_objects:
            my_total += item.my_subtotal()
        return my_total
    
    def reset_shown_total(self):
        self.to_ps_btn.text = 'Total: ${:.2f}'.format(self.compute_total())
        
    def change_to_ps(self, value):
        set_os_ls_of_item_obj(self.ls_of_item_obj())
        set_os_compute_total(self.compute_total())
        sum_of_quantity = 0
        for items in self.my_list_of_item_objects:
            sum_of_quantity += items.quantity
        if sum_of_quantity > 0:
            self.manager.get_screen('payment').reset_ps()
            self.manager.current = 'payment'
        else:
            change_to_ps_popup = myPopUp()
            change_to_ps_popup.set_message('Please place your order.')
            change_to_ps_popup.set_dismiss_message('Dismiss')
            change_to_ps_popup.set_size(1, 0.2)
            change_to_ps_popup.set_title('Nothing Ordered')
            change_to_ps_popup.getPopUp()

    def change_to_ms(self, value):
        self.manager.current = 'menu'

class PaymentScreen(Screen):
    def __init__(self, **kwargs):
        global os_ls_of_item_obj
        global os_compute_total
        self.os_ls_of_item_obj = get_os_ls_of_item_obj()
        self.os_compute_total = get_os_compute_total()
        Screen.__init__(self, **kwargs)
        self.layout = BoxLayout()
        self.layout.orientation = 'vertical'
        # Child widgets of Payment Screen
        # are Your Order Label,
        # Order Table,
        # Make Payment Button
        # Back to Order Button
        self.order_lbl = Label()
        self.order_lbl.text = 'Your Order'
        self.order_table_obj = OrderTable()
        self.order_table = self.order_table_obj.get_table()
        self.to_cs_btn = Button()
        self.to_cs_btn.text = 'Make Payment'
        self.to_os_btn = Button()
        self.to_os_btn.bind(on_press = self.change_to_os)
        self.to_cs_btn.bind(on_press = self.change_to_cs)
        self.to_os_btn.text = 'Back to Order'
        self.order_lbl.size_hint_y = 0.1
        self.to_cs_btn.size_hint_y = 0.1
        self.to_os_btn.size_hint_y = 0.1
        for ps_child in [self.order_lbl,
                         self.order_table,
                         self.to_cs_btn,
                         self.to_os_btn]:
            self.layout.add_widget(ps_child)
        self.add_widget(self.layout)
    
    def reset_ps(self):
        global os_ls_of_item_obj
        global os_compute_total
        self.os_ls_of_item_obj = get_os_ls_of_item_obj()
        self.os_compute_total = get_os_compute_total()
        print(self.os_ls_of_item_obj)
        print(self.os_compute_total)
        for items in self.os_ls_of_item_obj:
            if items.quantity > 0:
                self.order_table_obj.add_drink(items)
        self.to_cs_btn.text = 'Make Payment (S${:.2f})'.format(os_compute_total)
    
    def change_to_os(self, value):
        self.manager.current = 'order'
    
    def change_to_cs(self, value):
        if acct_dict[getMyKey()][1] - self.os_compute_total >= 0:
            self.manager.current = 'confirm'
            old_balance = acct_dict[getMyKey()][1]
            setData(getMyKey(), 1, float(old_balance) - self.os_compute_total)
            self.order_num = int(time.time())
            set_cs_order_num(self.order_num)
            detail = {'amount': self.os_compute_total}
            for items in self.os_ls_of_item_obj:
                if items.quantity > 0:
                    detail[items.name] = [items.quantity, items.remarks_input]                    
            db3.child('new order').child(str(self.order_num)).set(detail)
            set_cs_order_num(self.order_num)
            self.manager.get_screen('confirm').reset_qr()
        else:
            change_to_cs_popup = myPopUp()
            change_to_cs_popup.set_message('Please top up your balance before proceeding.')
            change_to_cs_popup.set_dismiss_message('Dismiss')
            change_to_cs_popup.set_size(1, 0.2)
            change_to_cs_popup.set_title('Insufficient balance.')
            change_to_cs_popup.getPopUp()

class ConfirmScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.layout = BoxLayout()
        self.layout.orientation = 'vertical'
        self.cs_lbl = Label()
        self.cs_lbl.text = 'Show this QR code to the counter and enjoy your drinks!'
        self.cs_lbl.size_hint_y = 0.1
        self.to_ms_btn = Button()
        self.to_ms_btn.text = 'Back to Menu (do not press this before claiming order!)'
        self.to_ms_btn.size_hint_y = 0.01
        self.to_ms_btn.size_hint_x = 0.01
        self.to_ms_btn.pos_hint = {'x' : 0.5, 'y' : 0.5}
        self.to_ms_btn.bind(on_press = self.change_to_ms)
        
    def change_to_ms(self, value):
        self.manager.get_screen('menu').updateKeyValues()
        self.manager.current = 'menu'
    
    def reset_qr(self):
        self.qr_num = str(get_cs_order_num())
        # Acknowledgements, modified from: https://ourcodeworld.com/articles/read/554/how-to-create-a-qr-code-image-or-svg-in-python
        self.qr = qrcode.QRCode(version = 1,
                                error_correction = qrcode.constants.ERROR_CORRECT_H,
                                box_size = 10,
                                border = 4)
        self.qr.add_data(self.qr_num)
        self.qr.make(fit = True)
        self.qr_img = self.qr.make_image()
        self.qr_img.save('image.jpg')
        self.img_widget = Image()
        self.img_widget.source = 'image.jpg'
        for cs_child in [self.cs_lbl,
                         self.img_widget,
                         self.to_ms_btn]:
            self.layout.add_widget(cs_child)
        self.add_widget(self.layout)

class Drink():
    def __init__(self, name, unit_price, img_source = 'https://t6.rbxcdn.com/366352c6ff3cad3294c91c01a4209ef6'):
        self.name = name
        self.unit_price = unit_price
        self.quantity = 0
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
        my_drink_unit_price_label.text = 'Unit Price: ${:.2f}'.format(self.unit_price)
        my_drink_remarks_label.text = 'Remarks:'
        self.my_drink_remarks_input = TextInput()
        self.remarks_input = self.my_drink_remarks_input.text
        for my_drink_detail in [my_drink_name_label,
                                my_drink_unit_price_label,
                                my_drink_remarks_label,
                                self.my_drink_remarks_input]:
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
        # self.my_drink_my_quantity_plus_btn.bind(on_press = self.add_quantity)
        # self.my_drink_my_quantity_minus_btn.bind(on_press = self.dec_quantity)
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
    
    def add_quantity(self):
        self.quantity += 1
        self.reset_shown_quantity()
    
    def dec_quantity(self):
        if self.quantity > 0:
            self.quantity -= 1
        self.reset_shown_quantity()
    
    def change_remarks(self, value, text):
        self.remarks_input = self.my_drink_remarks_input.text
    
    def my_subtotal(self):
        return self.quantity * self.unit_price
    
    def reset_shown_quantity(self):
        self.my_drink_my_quantity_label.text = '× {}'.format(self.quantity)

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

class OrderTable:
    def __init__(self):
        self.myTable = GridLayout()
        self.myTable.cols = 4
        self.itemNameLabel = Label()
        self.quantityLabel = Label()
        self.remarksLabel = Label()
        self.subtotalLabel = Label()
        self.itemNameLabel.text = 'Item Name'
        self.quantityLabel.text = 'Quantity'
        self.remarksLabel.text = 'Remarks'
        self.subtotalLabel.text = 'Subtotal'
        for headers in [self.itemNameLabel,
                        self.quantityLabel,
                        self.remarksLabel,
                        self.subtotalLabel]:
            self.myTable.add_widget(headers)
    
    def add_drink(self, someDrink):
        for drink_details in [Label(text = someDrink.name),
                              Label(text = str(someDrink.quantity)),
                              Label(text = someDrink.remarks_input),
                              Label(text = format(someDrink.my_subtotal(), '.2f'))]:
            self.myTable.add_widget(drink_details)
    
    def get_table(self):
        return self.myTable

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

def setMyKey(newKey):
    global myKey
    myKey = newKey

def getMyKey():
    global myKey
    return myKey

class combined_function():
    def __init__(self, f1, f2):
        self.f1 = f1
        self.f2 = f2
    
    def complex_function(self, instance):
        self.f2()
        self.f1()

if __name__ == '__main__':
    Consumer().run()
