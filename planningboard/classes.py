class Task():
    IsTask = 0
    Title = ""
    Description = ""
    Size = ""
    Color = ""

    def __init__(self, IsTask, Title, Description, Size, Color):
        self.IsTask = IsTask
        self.Title = Title
        self.Description = Description
        self.Size = Size
        self.Color = Color

class Inferior():
    Position = 0
    Name = ""
    ID = 0

    def __init__(self, Position, Name, ID):
        self.Position = Position
        self.Name = Name
        self.ID = ID

class UserObj():
    ID = 0
    Surname = ""
    Name = ""
    Patronymic = ""
    Login = ""
    Password = ""
    RightsLevel = 0

    def __init__(self, ID, Surname, Name, Patronymic, Login, Password, RightsLevel):
        self.ID = ID
        self.Surname = Surname
        self.Name= Name
        self.Patronymic = Patronymic
        self.Login = Login
        self.Password = Password
        self.RightsLevel = RightsLevel