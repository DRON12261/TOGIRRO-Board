import datetime

class Task():
    IsTask = 0
    Title = ""
    Description = ""
    StartPosition = 0
    Size = 0
    Color = ""
    StartDate = None
    EndDate = None
    Priority = 0
    StartDateSTR = ""
    EndDateSTR = ""
    StartDateSTRE = ""
    EndDateSTRE = ""
    ID = 0
    ReportText =""
    Status = 0

    def __init__(self, IsTask, Title, Description, StartPosition, Size, Color, StartDate, EndDate, Priority, ID, ReportText, Status):
        self.IsTask = IsTask
        self.Title = Title
        self.Description = Description
        self.StartPosition = StartPosition
        self.Size = Size
        self.Color = Color
        self.StartDate = StartDate
        self.EndDate = EndDate
        self.StartDateSTR = StartDate.strftime("%d.%m.%Y")
        self.EndDateSTR = EndDate.strftime("%d.%m.%Y")
        self.StartDateSTRE = StartDate.strftime("%Y-%m-%d")
        self.EndDateSTRE = EndDate.strftime("%Y-%m-%d")
        self.Priority = Priority
        self.ID = ID
        self.ReportText = ReportText
        self.Status

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