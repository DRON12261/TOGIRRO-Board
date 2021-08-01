from django.shortcuts import render, redirect
from django.urls import reverse
import pyodbc, os
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from .classes import Task, Inferior, UserObj
from django.contrib.auth.models import User

authorized = False

UserData = None

DBServer = 'localhost\sqlexpress'
DBName = 'TOGIRRO'
DBUser = 'DESKTOP-M7C36LJ\DRON12261'
DBPassword = '12262000'
DBDriver = '17'

if os.path.isfile('DBConfig.txt'):
    DBConfig = open('DBConfig.txt', 'r')
    DBServer = DBConfig.readline()[:-1]
    DBName = DBConfig.readline()[:-1]
    DBUser = DBConfig.readline()[:-1]
    DBPassword = DBConfig.readline()[:-1]
    DBDriver = DBConfig.readline()

conn = pyodbc.connect('DRIVER={ODBC Driver '+DBDriver+' for SQL Server};SERVER='+DBServer+';DATABASE='+DBName+';UID='+DBUser+';Trusted_connection=yes')
cursor = conn.cursor()

def main(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        return redirect('board')

@login_required
def board(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST" and 'admin' in request.POST:
        request.session['ASearch'] = ""
        request.session['ASearchType'] = -1
        request.session['ACurUserID'] = request.session['UserData']
        return redirect('adminlobby')

    if request.method == "POST" and 'weekpicker' in request.POST:
        request.session['Date'] = request.POST['weekpicker']

    if request.method == "POST" and 'logout' in request.POST:
        logout(request)
        return redirect('login')
    
    UserD = cursor.execute("SELECT * FROM Employees WHERE EmployeeID='"+str(request.session['UserData'])+"'").fetchall()[0]
    UserName = UserD.Surname+' '+UserD.Name+' '+UserD.Patronymic

    TodayDay = 0
    if str(datetime.date.today().isocalendar()[0])+'-W'+str(datetime.date.today().isocalendar()[1]) == request.session['Date']:
        TodayDay = datetime.date.today().isocalendar()[2]
    else:
        TodayDay = 0

    InferiorDB = cursor.execute("SELECT * FROM InferiorList WHERE ChiefID='"+str(request.session['UserData'])+"'").fetchall()
    InferiorList = [Inferior(0, '[ВЫ] '+UserName, UserD.EmployeeID)]
    inferI = 1
    for row in InferiorDB:
        infer = cursor.execute("SELECT * FROM Employees WHERE EmployeeID='"+str(row.InferiorID)+"'").fetchone()
        InferiorList.append(Inferior(inferI, '['+str(inferI)+'] '+infer.Surname+' '+infer.Name+' '+infer.Patronymic, row.InferiorID))
        inferI += 1
    
    if request.method == "POST" and 'inferior' in request.POST:
        request.session['CurInferior'] = int(request.POST['inferior'])
    
    Tasks = [
        [
            Task(0, "", "", "2", ""),
            Task(1, "Task1", "Task1", "4", "danger"),
            Task(0, "", "", "1", "")
        ],
        [
            Task(0, "", "", "1", ""),
            Task(1, "Task2", "Task2", "2", "info"),
            Task(0, "", "", "2", ""),
            Task(1, "Task3", "Task3", "2", "info")
        ],
        [
            Task(0, "", "", "7", "")
        ],
        [
            Task(1, "Task4", "Task4", "7", "warning")
        ]
    ]

    context = {
        'UserName' : UserName,
        'RightsLevel' : UserD.RightsLevel,
        'Date' : request.session['Date'],
        'TodayDay' : TodayDay,
        'Tasks' : Tasks,
        'InferiorList' : InferiorList,
        'CurInferior' : request.session['CurInferior']
    }

    return render(request, 'board.html', context)

def auth(request):
    try:
        a = request.session['loseLogin']
    except KeyError:
        request.session['loseLogin'] = 0
    
    try:
        b = request.session['loseCount']
    except KeyError:
        request.session['loseCount'] = 0

    if request.session['loseCount'] == 0:
        request.session['loseLogin'] = 0
    
    username = ''
    password = ''
    if request.method == "POST" and 'login' in request.POST and 'password' in request.POST:
        username = request.POST['login']
        password = request.POST['password']
        answer = cursor.execute("SELECT * FROM Employees WHERE Login='"+username+"' AND Password='"+password+"'").fetchall()
        user = authenticate(request, username=username, password=password)
        if answer and user is not None and user.is_active:
            print(answer)
            request.session['UserData'] = answer[0].EmployeeID
            request.session['Date'] = str(datetime.date.today().isocalendar()[0])+'-W'+str(datetime.date.today().isocalendar()[1])
            request.session['CurInferior'] = 0
            request.session['ACurUserID'] = answer[0].EmployeeID
            request.session['ASearch'] = ""
            request.session['ASearchType'] = -1
            login(request, user)
            request.session['loseLogin'] = 0
            request.session['loseCount'] = 0
            return redirect('board')
        else:
            request.session['loseLogin'] = 1
            request.session['loseCount'] = 1
            return redirect('login')
    
    if request.session['loseCount'] == 1:
        request.session['loseCount'] = 0

    context = {
        'loseLogin' : request.session['loseLogin']
    }
    
    return render(request, 'login.html', context)

def adminlobby(request):
    
    if not request.user.is_authenticated:
        return redirect('login')
    
    UserD = cursor.execute("SELECT * FROM Employees WHERE EmployeeID='"+str(request.session['UserData'])+"'").fetchall()[0]
    if UserD.RightsLevel < 2:
        return redirect('board')

    if request.method == "POST" and 'tasks' in request.POST:
        return redirect('board')
    
    if request.method == "POST" and 'logout' in request.POST:
        logout(request)
        return redirect('login')
    
    if request.method == "POST" and 'searchButton' in request.POST:
        request.session['ASearch'] = request.POST['search']
        request.session['ASearchType'] = int(request.POST['searchType']) - 1

    if request.method == "POST" and 'createNewUser' in request.POST:
        newSurname = request.POST['newSurname']
        newName = request.POST['newName']
        newPatronymic = request.POST['newPatronymic']
        newLogin = request.POST['newLogin']
        newPassword = request.POST['newPassword']
        newRightsLevel = int(request.POST['newRightsLevel'])

        newUser = User.objects.create_user(newLogin, password = newPassword)
        if newRightsLevel == 2:
            newUser.is_superuser = True
            newUser.is_staff = True
        newUser.save()

        cursor.execute("INSERT INTO Employees (Surname, Name, Patronymic, Login, Password, RightsLevel) VALUES('"+newSurname+"','"+newName+"', '"+newPatronymic+"', '"+newLogin+"', '"+newPassword+"', "+str(newRightsLevel)+")")
        conn.commit()

    if request.method == "POST" and 'deleteButton' in request.POST:
        delUserDB = cursor.execute("SELECT * FROM Employees WHERE EmployeeID='"+str(request.session['ACurUserID'])+"'").fetchone()
        delUser = User.objects.get(username = delUserDB.Login)
        delUser.delete()
        cursor.execute("DELETE FROM Employees WHERE EmployeeID="+str(request.session['ACurUserID']))
        conn.commit()
    
    if request.method == "POST" and 'saveButton' in request.POST:
        saveSurname = request.POST['saveSurname']
        saveName = request.POST['saveName']
        savePatronymic = request.POST['savePatronymic']
        saveLogin = request.POST['saveLogin']
        savePassword = request.POST['savePassword']
        saveRightsLevel = int(request.POST['saveRightsLevel'])

        saveUserDB = cursor.execute("SELECT * FROM Employees WHERE EmployeeID='"+str(request.session['ACurUserID'])+"'").fetchone()
        saveUser = User.objects.get(username = saveUserDB.Login)
        saveUser.username = saveLogin
        saveUser.set_password(savePassword)
        if saveRightsLevel == 2:
            saveUser.is_superuser = True
            saveUser.is_staff = True
        else:
            saveUser.is_superuser = False
            saveUser.is_staff = False
        saveUser.save()

        cursor.execute("UPDATE Employees SET Surname='"+saveSurname+"', Name='"+saveName+"', Patronymic='"+savePatronymic+"', Login='"+saveLogin+"', Password='"+savePassword+"', RightsLevel="+str(saveRightsLevel)+" WHERE EmployeeID="+str(request.session['ACurUserID']))
        conn.commit()

    if request.session['ASearch'] == "":
        if request.session['ASearchType'] == -1:
            users = cursor.execute("SELECT * FROM Employees").fetchall()
        else:
            users = cursor.execute("SELECT * FROM Employees WHERE RightsLevel="+str(request.session['ASearchType'])+"").fetchall()
    else:
        if request.session['ASearchType'] == -1:
            users = cursor.execute("WITH A AS (SELECT *, Surname+' '+Name+' '+Patronymic AS LikeName FROM Employees) SELECT * FROM A WHERE LikeName LIKE '%'+'"+request.session['ASearch']+"'+'%'").fetchall()
        else:
            users = cursor.execute("WITH A AS (SELECT *, Surname+' '+Name+' '+Patronymic AS LikeName FROM Employees) SELECT * FROM A WHERE LikeName LIKE '%'+'"+request.session['ASearch']+"'+'%' AND RightsLevel="+str(request.session['ASearchType'])+"").fetchall()
        
    userList = []
    for row in users:
        userList.append(UserObj(row.EmployeeID, row.Surname, row.Name, row.Patronymic, row.Login, row.Password, row.RightsLevel))
    
    if request.method == "POST":
        for user in userList:
            if 'User'+str(user.ID) in request.POST:
                request.session['ACurUserID'] = user.ID

    isNotSelectedUser = False
    if len(userList) < 1:
        curUser = UserObj(-1,"","","","","",0)
        isNotSelectedUser = True
    else:
        curUser = userList[0]

    for user in userList:
        if user.ID == request.session['ACurUserID']:
            curUser = user
    
    InferiorList = []
    if not isNotSelectedUser:
        InferiorDB = cursor.execute("SELECT * FROM InferiorList WHERE ChiefID='"+str(request.session['ACurUserID'])+"'").fetchall()
        for row in InferiorDB:
            infer = cursor.execute("SELECT * FROM Employees WHERE EmployeeID='"+str(row.InferiorID)+"'").fetchone()
            InferiorList.append(UserObj(infer.EmployeeID, infer.Surname, infer.Name, infer.Patronymic, infer.Login, infer.Password, infer.RightsLevel))

    NotInferiorList = []
    if not isNotSelectedUser:
        InfIDs = str(request.session['UserData'])+','
        for inf in InferiorList:
            InfIDs = InfIDs+' '+str(inf.ID)+','
        NonInferiorDB = None
        NonInferiorDB = cursor.execute("SELECT * FROM Employees WHERE EmployeeID NOT IN ("+InfIDs[:-1]+")").fetchall()
        for row in NonInferiorDB:
            NotInferiorList.append(UserObj(row.EmployeeID, row.Surname, row.Name, row.Patronymic, row.Login, row.Password, row.RightsLevel))

    if request.method == "POST" and 'deletePButton' in request.POST:
        if len(InferiorList) > 0:
            deletedInfers = []
            for infer in InferiorList:
                if 'p'+str(infer.ID) in request.POST:
                    deletedInfers.append(infer.ID)
            
            for i in deletedInfers:
                cursor.execute("DELETE FROM InferiorList WHERE ChiefID="+str(curUser.ID)+" AND InferiorID="+str(i))
            conn.commit()
            return redirect('adminlobby')
    
    if request.method == "POST" and 'addPButton' in request.POST:
        if len(NotInferiorList) > 0:
            addInfers = []
            for infer in NotInferiorList:
                if 'a'+str(infer.ID) in request.POST:
                    addInfers.append(infer.ID)
            
            print(addInfers)
            for i in addInfers:
                cursor.execute("INSERT INTO InferiorList (ChiefID, InferiorID) VALUES("+str(curUser.ID)+", "+str(i)+")")
            conn.commit()
            return redirect('adminlobby')

    context = {
        'users' : userList,
        'curUser' : curUser,
        'loggedUser' : request.session['UserData'],
        'InferiorList' : InferiorList,
        'NotInferiorList' : NotInferiorList,
        'searchControl' : request.session['ASearch'],
        'searchType' : request.session['ASearchType'],
        'isNotSelectedUser' : isNotSelectedUser
    }

    return render(request, 'adminlobby.html', context)