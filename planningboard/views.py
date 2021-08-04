from django.shortcuts import render, redirect
from django.urls import reverse
import pyodbc, os
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from .classes import Task, Inferior, UserObj, Message, Chat
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
    
    if request.session['EditErrorCount'] == 0:
        request.session['EditError'] = 0

    if request.session['AddErrorCount'] == 0:
        request.session['AddError'] = 0

    UserD = cursor.execute("SELECT * FROM Employees WHERE EmployeeID='"+str(request.session['UserData'])+"'").fetchall()[0]
    UserName = UserD.Surname+' '+UserD.Name+' '+UserD.Patronymic

    Days = []
    TodayDay = 0
    if str(datetime.date.today().isocalendar()[0])+'-W'+str(datetime.date.today().isocalendar()[1]) == request.session['Date']:
        TodayDay = datetime.date.today().isocalendar()[2]
    else:
        TodayDay = 0
    TodayWeek = datetime.date.today().isocalendar()[1]
    WeekOnPage = int(request.session['Date'][6:])
    EndSt = 0
    if TodayDay == 0:
        EndSt = 7-TodayDay-1
    else:
        EndSt = 7-TodayDay
    for i in range(1,8):
        Days.append(datetime.date.today() + datetime.timedelta(days=EndSt, weeks=WeekOnPage-TodayWeek))
        EndSt = EndSt - 1

    InferiorDB = cursor.execute("SELECT * FROM InferiorList WHERE ChiefID='"+str(request.session['UserData'])+"'").fetchall()
    InferiorList = [Inferior(0, '[ВЫ] '+UserName, UserD.EmployeeID)]
    inferI = 1
    for row in InferiorDB:
        infer = cursor.execute("SELECT * FROM Employees WHERE EmployeeID='"+str(row.InferiorID)+"'").fetchone()
        InferiorList.append(Inferior(inferI, '['+str(inferI)+'] '+infer.Surname+' '+infer.Name+' '+infer.Patronymic, row.InferiorID))
        inferI += 1
    
    if request.method == "POST" and 'inferior' in request.POST:
        request.session['CurInferior'] = int(request.POST['inferior'])
    
    Tasks = [[],[],[],[],[]]
    TaskList = []
    taskIDs = ""

    TaskIDDB = cursor.execute("SELECT TaskID FROM TaskList WHERE EmployeeID="+str(InferiorList[int(request.session['CurInferior'])].ID)).fetchall()
    for row in TaskIDDB:
        taskIDs = taskIDs+str(row.TaskID)+','
    if taskIDs != "":
        taskIDs = taskIDs[:-1]
        TasksDB = cursor.execute("SELECT * FROM Tasks WHERE ((Start BETWEEN '"+Days[6].strftime("%Y/%m/%d")+"' AND '"+Days[0].strftime("%Y/%m/%d")+"' OR Deadline BETWEEN '"+Days[6].strftime("%Y/%m/%d")+"' AND '"+Days[0].strftime("%Y/%m/%d")+"') OR (Start < '"+Days[6].strftime("%Y/%m/%d")+"' AND Deadline > '"+Days[0].strftime("%Y/%m/%d")+"')) AND TaskID IN ("+taskIDs+")").fetchall()
        for row in TasksDB:
            desc = ""
            if row.Description != None:
                desc = cursor.execute("SELECT Text FROM Texts WHERE TextID="+str(row.Description)).fetchone().Text
            startDate = row.Start
            endDate = row.Deadline + datetime.timedelta(days=1)
            if row.Deadline + datetime.timedelta(days=1) > Days[0]:
                endDate = Days[0] + datetime.timedelta(days=1)
            if row.Start < Days[6]:
                startDate = Days[6]
            size = (endDate - startDate).days
            if size > 7:
                size = 7
            elif size < 1:
                size = 1
            pos = 1
            for i in range(0,7):
                if row.Start == Days[i]:
                    pos = 7 - i
            CheckListsDB = cursor.execute("SELECT * FROM CheckBoxList WHERE TaskID="+str(row.TaskID)).fetchone()
            CheckBoxDB = cursor.execute("SELECT * FROM CheckBoxes WHERE CheckBoxID="+str(CheckListsDB.CheckBoxID)).fetchone()
            TextDB = cursor.execute("SELECT * FROM Texts WHERE TextID="+str(CheckBoxDB.TextID)).fetchone()
            AuthorDB = cursor.execute("SELECT * FROM Employees WHERE EmployeeID="+str(row.Author)).fetchone()
            TaskList.append(Task(1, row.Title, desc, pos , size, row.TaskColor, row.Start, row.Deadline, row.Priority, row.TaskID, TextDB.Text, CheckBoxDB.Status, AuthorDB.Surname+' '+AuthorDB.Name+' '+AuthorDB.Patronymic))

    fillCounter = 0
    for i in range(0,5):
        for j in range(1,8):
            if fillCounter > 0:
                fillCounter = fillCounter - 1
                continue
            isFound = False
            isBreak = False
            for task in TaskList:
                if task.Priority == i+1:
                    if task.StartPosition == j:
                        Tasks[i].append(task)
                        fillCounter = task.Size - 1
                        isFound = True
                        isBreak = True
                        break
            if not isFound:
                Tasks[i].append(Task(0,"","",j,1,"",datetime.date.today(),datetime.date.today(),i+1,0,"",0,""))
    
    for task in TaskList:
        if request.method == "POST" and 'sendReport'+str(task.ID) in request.POST:
            checkBoxID = cursor.execute("SELECT * FROM CheckBoxList WHERE TaskID="+str(task.ID)).fetchone().CheckBoxID
            checkBoxDB = cursor.execute("SELECT * FROM CheckBoxes WHERE CheckBoxId="+str(checkBoxID)).fetchone()
            cursor.execute("UPDATE CheckBoxes SET Status=2 WHERE CheckBoxID="+str(checkBoxID))
            cursor.execute("UPDATE Texts SET Text='"+str(request.POST['Report'+str(task.ID)])+"' WHERE TextID="+str(CheckBoxDB.TextID))
            conn.commit()
            return redirect('board')

    for task in TaskList:
        if request.method == "POST" and 'sendStatus'+str(task.ID) in request.POST:
            checkBoxID = cursor.execute("SELECT * FROM CheckBoxList WHERE TaskID="+str(task.ID)).fetchone().CheckBoxID
            cursor.execute("UPDATE CheckBoxes SET Status=3 WHERE CheckBoxID="+str(checkBoxID))
            conn.commit()
            return redirect('board')

    for task in TaskList:
        if request.method == "POST" and 'sendNoStatus'+str(task.ID) in request.POST:
            checkBoxID = cursor.execute("SELECT * FROM CheckBoxList WHERE TaskID="+str(task.ID)).fetchone().CheckBoxID
            cursor.execute("UPDATE CheckBoxes SET Status=0 WHERE CheckBoxID="+str(checkBoxID))
            conn.commit()
            return redirect('board')
    
    for task in TaskList:
        if request.method == "POST" and 'saveB'+str(task.ID) in request.POST:
            stDate = request.POST['start'+str(task.ID)]
            enDate = request.POST['end'+str(task.ID)]
            sDate = datetime.date(int(stDate[:-6]), int(stDate[5:-3]), int(stDate[8:]))
            eDate = datetime.date(int(enDate[:-6]), int(enDate[5:-3]), int(enDate[8:]))
            if (sDate > eDate):
                request.session['EditError'] = 2
                request.session['EditErrorCount'] = 1
            position = request.POST['pos'+str(task.ID)]
            if taskIDs != "":
                searchDB = cursor.execute("SELECT * FROM Tasks WHERE (Start BETWEEN '"+str(sDate)+"' AND '"+str(eDate)+"' OR Deadline BETWEEN '"+str(sDate)+"' AND '"+str(eDate)+"') AND (TaskID IN ("+taskIDs+") AND NOT TaskID="+str(task.ID)+") AND Priority="+position).fetchone()
                if searchDB is not None:
                    request.session['EditError'] = 1
                    request.session['EditErrorCount'] = 1
            if request.session['EditError'] == 0:
                cursor.execute("UPDATE Tasks SET Priority="+str(position)+", Start='"+str(sDate)+"', Deadline='"+str(eDate)+"' WHERE TaskID="+str(task.ID))
            cursor.execute("UPDATE Tasks SET Title='"+request.POST['title'+str(task.ID)]+"' WHERE TaskID="+str(task.ID))
            textDB = cursor.execute("SELECT * FROM Tasks WHERE TaskID="+str(task.ID)).fetchone()
            cursor.execute("UPDATE Texts SET Text='"+str(request.POST['desc'+str(task.ID)])+"' WHERE TextID="+str(textDB.Description))
            conn.commit()
            return redirect('board')
    
    for task in TaskList:
        if request.method == "POST" and 'deleteB'+str(task.ID) in request.POST:
            cursor.execute("DELETE FROM TaskList WHERE TaskID="+str(task.ID))
            checkBoxID = cursor.execute("SELECT * FROM CheckBoxList WHERE TaskID="+str(task.ID)).fetchone().CheckBoxID
            cursor.execute("DELETE FROM CheckBoxList WHERE TaskID="+str(task.ID))
            descID = cursor.execute("SELECT * FROM Tasks WHERE TaskID="+str(task.ID)).fetchone().Description
            cursor.execute("DELETE FROM Tasks WHERE TaskID="+str(task.ID))
            textID = cursor.execute("SELECT * FROM CheckBoxes WHERE CheckBoxID="+str(checkBoxID)).fetchone().TextID
            cursor.execute("DELETE FROM CheckBoxes WHERE CheckBoxID="+str(checkBoxID))
            cursor.execute("DELETE FROM Texts WHERE TextID="+str(textID))
            cursor.execute("DELETE FROM Texts WHERE TextID="+str(descID))
            conn.commit()
            return redirect('board')
    
    if request.method == "POST" and 'addB' in request.POST:
        stDate = request.POST['addStart']
        enDate = request.POST['addEnd']
        sDate = datetime.date(int(stDate[:-6]), int(stDate[5:-3]), int(stDate[8:]))
        eDate = datetime.date(int(enDate[:-6]), int(enDate[5:-3]), int(enDate[8:]))
        if (sDate > eDate):
            request.session['AddError'] = 2
            request.session['AddErrorCount'] = 1
        position = request.POST['addPos']
        if taskIDs != "":
            searchDB = cursor.execute("SELECT * FROM Tasks WHERE (Start BETWEEN '"+str(sDate)+"' AND '"+str(eDate)+"' OR Deadline BETWEEN '"+str(sDate)+"' AND '"+str(eDate)+"') AND TaskID IN ("+taskIDs+") AND Priority="+position).fetchone()
            if searchDB is not None:
                request.session['AddError'] = 1
                request.session['AddErrorCount'] = 1
        if request.session['AddError'] == 0:
            cursor.execute("INSERT INTO Texts (Text) VALUES('"+request.POST['addDesc']+"')")
            cursor.execute("INSERT INTO Texts (Text) VALUES('')")
            textsDB = cursor.execute("SELECT * FROM Texts").fetchall()
            descText = textsDB[len(textsDB)-2].TextID
            reportText = textsDB[len(textsDB)-1].TextID
            cursor.execute("INSERT INTO CheckBoxes (TextID, Status) VALUES("+str(reportText)+", 1)")
            checkBoxDB = cursor.execute("SELECT * FROM CheckBoxes").fetchall()
            checkBoxID = checkBoxDB[len(checkBoxDB)-1].CheckBoxID
            cursor.execute("INSERT INTO Tasks (Title, Author, Description, Priority, Start, Deadline, TaskColor) VALUES('"+request.POST['addTitle']+"', "+str(request.session['UserData'])+", "+str(descText)+", "+str(position)+", '"+str(sDate)+"', '"+str(eDate)+"', 'info')")
            addTaskDB = cursor.execute("SELECT * FROM Tasks").fetchall()
            curTaskAdd = addTaskDB[len(addTaskDB)-1].TaskID
            cursor.execute("INSERT INTO CheckBoxList (TaskID, CheckBoxID) VALUES("+str(curTaskAdd)+", "+str(checkBoxID)+")")
            cursor.execute("INSERT INTO TaskList (EmployeeID, TaskID) VALUES("+str(InferiorList[int(request.session['CurInferior'])].ID)+", "+str(curTaskAdd)+")")
            conn.commit()
            request.session['AddTitle'] = ""
            request.session['AddDesc'] = ""
        return redirect('board')

    if request.session['EditErrorCount'] == 1:
        request.session['EditErrorCount'] = 0
    
    if request.session['AddErrorCount'] == 1:
        request.session['AddErrorCount'] = 0

    context = {
        'UserName' : UserName,
        'RightsLevel' : UserD.RightsLevel,
        'Date' : request.session['Date'],
        'TodayDay' : TodayDay,
        'TodayDate' : datetime.date.today().strftime("%Y-%m-%d"),
        'Tasks' : Tasks,
        'Tasks0L' : len(Tasks[0]),
        'Tasks1L' : len(Tasks[1]),
        'Tasks2L' : len(Tasks[2]),
        'Tasks3L' : len(Tasks[3]),
        'Tasks4L' : len(Tasks[4]),
        'InferiorList' : InferiorList,
        'CurInferior' : request.session['CurInferior'],
        'Monday' : Days[6].strftime("%d.%m.%Y"),
        'Tuesday' : Days[5].strftime("%d.%m.%Y"),
        'Wednesday' : Days[4].strftime("%d.%m.%Y"),
        'Thursday' : Days[3].strftime("%d.%m.%Y"),
        'Friday' : Days[2].strftime("%d.%m.%Y"),
        'Saturday' : Days[1].strftime("%d.%m.%Y"),
        'Sunday' : Days[0].strftime("%d.%m.%Y"),
        'EditError' : request.session['EditError'],
        'AddError' : request.session['AddError']
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
            login(request, user)
            request.session['UserData'] = answer[0].EmployeeID
            request.session['Date'] = str(datetime.date.today().isocalendar()[0])+'-W'+str(datetime.date.today().isocalendar()[1])
            request.session['CurInferior'] = 0
            request.session['ACurUserID'] = answer[0].EmployeeID
            request.session['ASearch'] = ""
            request.session['ASearchType'] = -1
            request.session['isEditModal'] = False
            request.session['isEditCount'] = 0
            request.session['EditError'] = 0
            request.session['EditErrorCount'] = 0
            request.session['isAddModal'] = False
            request.session['isAddCount'] = 0
            request.session['AddError'] = 0
            request.session['AddErrorCount'] = 0
            request.session['AddTitle'] = ""
            request.session['AddDesc'] = ""
            request.session['mesSearch'] = ""
            request.session['mesText'] = ""
            request.session['isChatList'] = True
            request.session['curChatID'] = 0
            request.session['loseLogin'] = 0
            request.session['loseCount'] = 0
            request.session['isSendMes'] = 0
            request.session['isSendMesCount'] = 0
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
        InfIDs = ''
        for inf in InferiorList:
            InfIDs = InfIDs+' '+str(inf.ID)+','
        NonInferiorDB = None
        if InfIDs == '':
            NonInferiorDB = cursor.execute("SELECT * FROM Employees").fetchall()
        else:
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

    UserD = cursor.execute("SELECT * FROM Employees WHERE EmployeeID='"+str(request.session['UserData'])+"'").fetchall()[0]
    UserName = UserD.Surname+' '+UserD.Name+' '+UserD.Patronymic

    context = {
        'UserName' : UserName,
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

def messenger(request):
    chats = []

    if request.session['isSendMesCount'] == 0:
        request.session['isSendMes'] = 0

    if request.method == 'POST' and 'searchButton' in request.POST:
        request.session['isChatList'] = True
        request.session['mesSearch'] = request.POST['search']
    
    if request.session['mesSearch'] == "":
        chatsDB = cursor.execute('SELECT * FROM ChatList JOIN Chats ON ChatList.ChatID = Chats.ChatID WHERE EmployeeID=' + str(request.session['UserData'])).fetchall()
        for row in chatsDB:
            textIDs = cursor.execute("SELECT * FROM TextListInChat WHERE ChatID="+str(row.ChatID)).fetchall()
            textIDsSTR = ''
            for rowt in textIDs:
                textIDsSTR = textIDsSTR + str(rowt.TextID) + ','
            if textIDsSTR != '':
                messagesDB = cursor.execute("SELECT * FROM Texts WHERE TextID IN ("+textIDsSTR[:-1]+")").fetchall()
                sender = cursor.execute("SELECT * FROM Employees WHERE EmployeeID="+str(messagesDB[len(messagesDB)-1].SenderID)).fetchone()
                chatTitle = cursor.execute("SELECT * FROM Chats WHERE ChatID="+str(row.ChatID)).fetchone().Title
                chats.append(Chat(chatTitle, row.ChatID ,messagesDB[len(messagesDB)-1].Text,messagesDB[len(messagesDB)-1].SendingDate, sender.Surname+' '+sender.Name+' '+sender.Patronymic, messagesDB[len(messagesDB)-1].SenderID))
            else:
                chatTitle = cursor.execute("SELECT * FROM Chats WHERE ChatID="+str(row.ChatID)).fetchone().Title
                chats.append(Chat(chatTitle, row.ChatID, "В этой беседе еще нет сообщений...", datetime.datetime.now(), "Система", 0))
    else:
        chatsDB = cursor.execute("SELECT * FROM ChatList JOIN Chats ON ChatList.ChatID = Chats.ChatID WHERE Title LIKE '%'+'" + request.session['mesSearch'] + "'+'%' AND EmployeeID=" + str(request.session['UserData'])).fetchall()
        for row in chatsDB:
            textIDs = cursor.execute("SELECT * FROM TextListInChat WHERE ChatID="+str(row.ChatID)).fetchall()
            textIDsSTR = ''
            for rowt in textIDs:
                textIDsSTR = textIDsSTR + str(rowt.TextID) + ','
            if textIDsSTR != '':
                messagesDB = cursor.execute("SELECT * FROM Texts WHERE TextID IN ("+textIDsSTR[:-1]+")").fetchall()
                sender = cursor.execute("SELECT * FROM Employees WHERE EmployeeID="+str(messagesDB[len(messagesDB)-1].SenderID)).fetchone()
                chatTitle = cursor.execute("SELECT * FROM Chats WHERE ChatID="+str(row.ChatID)).fetchone().Title
                chats.append(Chat(chatTitle, row.ChatID ,messagesDB[len(messagesDB)-1].Text,messagesDB[len(messagesDB)-1].SendingDate, sender.Surname+' '+sender.Name+' '+sender.Patronymic, messagesDB[len(messagesDB)-1].SenderID))
            else:
                chatTitle = cursor.execute("SELECT * FROM Chats WHERE ChatID="+str(row.ChatID)).fetchone().Title
                chats.append(Chat(chatTitle, row.ChatID, "В этой беседе еще нет сообщений...", datetime.datetime.now(), "Система", 0))

    for ch in chats:
        if request.method == 'POST' and 'chatButton' + str(ch.ChatID) in request.POST:
            request.session['isChatList'] = False
            request.session['curChatID'] = ch.ChatID

    if request.method == 'POST' and 'returnButton' in request.POST:
        request.session['isChatList'] = True
    
    employee_list = cursor.execute('SELECT * FROM Employees WHERE NOT EmployeeID=' + str(request.session['UserData'])).fetchall()
    if request.method == 'POST' and 'addChatButton' in request.POST:
        print('len(employee_list) = ' + str(len(employee_list)))
        if len(employee_list) > 0:
            add_to_chat = []
            for emps in employee_list:
                if 'a' + str(emps.EmployeeID) in request.POST:
                    add_to_chat.append(emps.EmployeeID)
            print('request.POST["title"] = ' + str(request.POST["title"]))
            chatTitle = request.POST["title"]
            if len(add_to_chat) == 1:
                empl = cursor.execute("SELECT * FROM Employees WHERE EmployeeID="+str(add_to_chat[0])).fetchone()
                chatTitle = "Диалог: "+empl.Surname+" "+empl.Name+" "+empl.Patronymic
            cursor.execute("INSERT INTO Chats (Title) VALUES ('" + chatTitle + "')")
            all_chats = cursor.execute('SELECT * FROM Chats').fetchall()
            last_record = all_chats[len(all_chats) - 1]
            print('add_to_chat: ' + str(add_to_chat))
            print('last_record_num = ' + str(last_record.ChatID))
            cursor.execute("INSERT INTO ChatList (EmployeeID, ChatID) VALUES(" + str(request.session['UserData']) + ", " + str(last_record.ChatID) + ")")
            for i in add_to_chat:
                cursor.execute(
                    "INSERT INTO ChatList (EmployeeID, ChatID) VALUES(" + str(i) + ", " + str(last_record.ChatID) + ")")
            conn.commit()
            request.session['isChatList'] = True
            return redirect('messenger')

    if request.method == "POST" and 'sendButton' in request.POST:
        if request.POST['message'] != "":
            cursor.execute("INSERT INTO Texts (Text, SendingDate, SenderID) VALUES('"+request.POST['message']+"', '"+str(datetime.datetime.now().strftime("%Y-%d-%m %H:%M:%S"))+"', '"+str(request.session['UserData'])+"')")
            TextDB = cursor.execute("SELECT * FROM Texts").fetchall()
            textID = TextDB[len(TextDB)-1].TextID
            cursor.execute("INSERT INTO TextListInChat (ChatID, TextID) VALUES("+str(request.session['curChatID'])+", "+str(textID)+")")
            conn.commit()
            request.session['mesText'] = ""
            request.session['isSendMes'] = 1
            request.session['isSendMesCount'] = 1
            return redirect('messenger')

    if request.method == "POST" and 'saveData' in request.POST:
        request.session['mesSearch'] = request.POST['saveSearch']
        request.session['mesText'] = request.POST['message']

    messages = []
    if request.session['curChatID'] != 0:
        textIDs = cursor.execute("SELECT * FROM TextListInChat WHERE ChatID="+str(request.session['curChatID'])).fetchall()
        textIDsSTR = ''
        for row in textIDs:
            textIDsSTR = textIDsSTR + str(row.TextID) + ','
        if textIDsSTR != '':
            messagesDB = cursor.execute("SELECT * FROM Texts WHERE TextID IN ("+textIDsSTR[:-1]+")").fetchall()
            for mes in messagesDB:
                sender = cursor.execute("SELECT * FROM Employees WHERE EmployeeID="+str(mes.SenderID)).fetchone()
                messages.append(Message(mes.Text, mes.SenderID, sender.Surname+' '+sender.Name+' '+sender.Patronymic, mes.SendingDate))

    if request.session['isSendMesCount'] == 1:
        request.session['isSendMesCount'] = 0

    nchats = sorted(chats, key = lambda chat : chat.LastTrueDate)
    nchats.reverse()

    print(request.session['isSendMes'])

    context = {
        'chats': nchats,
        'chat_list': request.session['isChatList'],
        'employee_list': employee_list,
        'cur_chat_title': '',
        'cur_chat_ID': 0,
        'cur_search': request.session['mesSearch'],
        'mes_text' : request.session['mesText'],
        'messages' : messages,
        'cur_user' : request.session['UserData'],
        'isSendMes' : request.session['isSendMes']
    }

    if request.session['curChatID'] != 0:
        chatDB = cursor.execute("SELECT * FROM Chats WHERE ChatID="+str(request.session['curChatID'])).fetchone()
        context['cur_chat_title'] = chatDB.Title
        context['cur_chat_ID'] = chatDB.ChatID
    
    return render(request, 'messenger.html', context)