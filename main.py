
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock
from kivymd.uix.backdrop import MDBackdrop
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

# Initialize Firebase Admin with the credentials file
cred = credentials.Certificate("assets/user-management-de483-firebase-adminsdk-otrho-2797ce9e07.json")
# เชื่อมต่อกับคอลเลกชัน "data"
firebase_admin.initialize_app(cred)
db = firestore.client()

# doc_ref = db.collection("Information").document("alovelace")
# doc_ref.set({"first": "Ada", "last": "Lovelace", "born": 1815})



LabelBase.register(name="default_font", fn_regular="assets/Poppins-Regular.ttf")

class ContentNavigationDrawer(MDBoxLayout):
    pass

class FirstScreen(MDScreenManager):
    pass

class MainApp(MDApp):
    def build(self):
        self.title = "ATC Technology"
        self.theme_cls.theme_style = "Light"

        return Builder.load_file("Sign.kv")
    def test(self):
        screen = find_Devices()
        return screen
class LoginWindow(MDScreen):
    def build(self):
        self.title = "ATC Technology"
        self.theme_cls.theme_style = "Light"

    def check_info(self):
        U_name = self.ids.Name.text
        U_passwd = self.ids.passWord.text

        try:
            if U_name != "" and U_passwd != "":
                users_ref = db.collection("Information").document(U_name)
                docs = users_ref.get()

                if docs.exists:
                    user_info = docs.to_dict()
                    if U_passwd == user_info["password"]:
                        self.manager.current = "main"
                    else:
                        raise Exception()
                else:
                    raise Exception()
            else:
                raise Exception()
        except:
            self.error_login = MDDialog(
                title="Error", text="Access Failed\nPlease check your username and password"
            )
            self.error_login.open()
    def show_pass(self, checkbox, value):
        if value:
            self.ids.passWord.password = False
        else:
            self.ids.passWord.password = True

class RegisterWindow(MDScreen):
    def check_data(self):
        name = self.ids.F_Name.text
        pasw = self.ids.F_passWord.text

        users_ref = db.collection("Information").document(name)
        docs = users_ref.get()


        if docs.exists:
            self.dialog_error_name = MDDialog(
                text="This Username already exists"
            )
            self.dialog_error_name.open()
        else:
            if name != "" and name != " " and pasw != "" and pasw != " ":
                users_ref.set({"password": pasw})

                self.success_regis = MDDialog(
                    title="Successful!",
                    text="You have been registered",
                    auto_dismiss = False,
                    buttons=[
                        MDFlatButton(
                            text="OK",
                            on_release=lambda *args: self.success_regis.dismiss()
                            )
                        ]
                    )
                self.success_regis.open()
            else:
                self.dialog_error_passw = MDDialog(text="Please fill the username and password")
                self.dialog_error_passw.open()

class MainWindow(MDScreen):
    pass
class find_Devices(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Create an MDBackdrop with menu options
        self.backdrop = MDBackdrop(left_action_items=[["menu"]], title= "Example Backdrop")
        # Create a button to toggle the backdrop
        self.toggle_button = MDFillRoundFlatIconButton(
            text="Toggle Backdrop",
            icon="menu",
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            on_release=self.toggle_backdrop
        )

        self.add_widget(self.toggle_button)

    def toggle_backdrop(self, instance):
        # Close the backdrop
        #self.backdrop.close()

        # Schedule the opening of the backdrop after 2 seconds
        Clock.schedule_once(self.open_backdrop, 2)

    def open_backdrop(self, dt):
        self.backdrop.open()

if __name__ == "__main__":
    MainApp().run()