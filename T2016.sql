USE [TOGIRRO]
GO
/****** Object:  Table [dbo].[ChatList]    Script Date: 04.08.2021 7:32:05 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[ChatList](
	[EmployeeID] [int] NOT NULL,
	[ChatID] [int] NOT NULL,
 CONSTRAINT [PK_ChatList] PRIMARY KEY CLUSTERED 
(
	[EmployeeID] ASC,
	[ChatID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Chats]    Script Date: 04.08.2021 7:32:05 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Chats](
	[ChatID] [int] IDENTITY(1,1) NOT NULL,
	[Title] [varchar](150) NOT NULL,
 CONSTRAINT [PK_Chats] PRIMARY KEY CLUSTERED 
(
	[ChatID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[CheckBoxes]    Script Date: 04.08.2021 7:32:05 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[CheckBoxes](
	[CheckBoxID] [int] IDENTITY(1,1) NOT NULL,
	[TextID] [int] NOT NULL,
	[Status] [int] NOT NULL,
	[Description] [varchar](500) NULL,
 CONSTRAINT [PK_CheckBoxes] PRIMARY KEY CLUSTERED 
(
	[CheckBoxID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[CheckBoxList]    Script Date: 04.08.2021 7:32:05 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[CheckBoxList](
	[TaskID] [int] NOT NULL,
	[CheckBoxID] [int] NOT NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[CommentList]    Script Date: 04.08.2021 7:32:05 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[CommentList](
	[CommentID] [int] NOT NULL,
	[TaskID] [int] NOT NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Comments]    Script Date: 04.08.2021 7:32:05 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Comments](
	[CommentID] [int] IDENTITY(1,1) NOT NULL,
	[TextID] [int] NOT NULL,
	[Likes] [int] NOT NULL,
	[Dislikes] [int] NOT NULL,
 CONSTRAINT [PK_Comments] PRIMARY KEY CLUSTERED 
(
	[CommentID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Employees]    Script Date: 04.08.2021 7:32:05 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Employees](
	[EmployeeID] [int] IDENTITY(1,1) NOT NULL,
	[Surname] [varchar](50) NOT NULL,
	[Name] [varchar](50) NOT NULL,
	[Patronymic] [varchar](50) NOT NULL,
	[Login] [varchar](50) NOT NULL,
	[Password] [varchar](50) NOT NULL,
	[RightsLevel] [int] NOT NULL,
	[Description] [varchar](500) NULL,
 CONSTRAINT [PK_Employees] PRIMARY KEY CLUSTERED 
(
	[EmployeeID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Files]    Script Date: 04.08.2021 7:32:05 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Files](
	[FileID] [int] IDENTITY(1,1) NOT NULL,
	[FileName] [varchar](100) NOT NULL,
 CONSTRAINT [PK_Files] PRIMARY KEY CLUSTERED 
(
	[FileID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[FilesInReportList]    Script Date: 04.08.2021 7:32:05 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[FilesInReportList](
	[ReportID] [int] NOT NULL,
	[FileID] [int] NOT NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[FilesInTextList]    Script Date: 04.08.2021 7:32:05 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[FilesInTextList](
	[TextID] [int] NOT NULL,
	[FileID] [int] NOT NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[InferiorList]    Script Date: 04.08.2021 7:32:05 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[InferiorList](
	[ChiefID] [int] NOT NULL,
	[InferiorID] [int] NOT NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[TaskList]    Script Date: 04.08.2021 7:32:05 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[TaskList](
	[EmployeeID] [int] NOT NULL,
	[TaskID] [int] NOT NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Tasks]    Script Date: 04.08.2021 7:32:05 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Tasks](
	[TaskID] [int] IDENTITY(1,1) NOT NULL,
	[Title] [varchar](150) NOT NULL,
	[Author] [int] NOT NULL,
	[Description] [int] NULL,
	[Priority] [int] NOT NULL,
	[Start] [date] NOT NULL,
	[Deadline] [date] NOT NULL,
	[TaskColor] [varchar](50) NOT NULL,
 CONSTRAINT [PK_Tasks] PRIMARY KEY CLUSTERED 
(
	[TaskID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[TextListInChat]    Script Date: 04.08.2021 7:32:05 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[TextListInChat](
	[ChatID] [int] NOT NULL,
	[TextID] [int] NOT NULL,
 CONSTRAINT [PK_TextListInChat] PRIMARY KEY CLUSTERED 
(
	[ChatID] ASC,
	[TextID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Texts]    Script Date: 04.08.2021 7:32:05 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Texts](
	[TextID] [int] IDENTITY(1,1) NOT NULL,
	[Text] [varchar](500) NOT NULL,
	[EmployeeID] [int] NULL,
	[ProjectID] [int] NULL,
	[BoardID] [int] NULL,
	[TaskID] [int] NULL,
	[MessageID] [int] NULL,
	[ChatID] [int] NULL,
	[SendingDate] [datetime] NULL,
	[SenderID] [int] NULL,
 CONSTRAINT [PK_Texts] PRIMARY KEY CLUSTERED 
(
	[TextID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[ChatList]  WITH CHECK ADD  CONSTRAINT [FK_ChatList_Chats] FOREIGN KEY([ChatID])
REFERENCES [dbo].[Chats] ([ChatID])
GO
ALTER TABLE [dbo].[ChatList] CHECK CONSTRAINT [FK_ChatList_Chats]
GO
ALTER TABLE [dbo].[ChatList]  WITH CHECK ADD  CONSTRAINT [FK_ChatList_Employees] FOREIGN KEY([EmployeeID])
REFERENCES [dbo].[Employees] ([EmployeeID])
GO
ALTER TABLE [dbo].[ChatList] CHECK CONSTRAINT [FK_ChatList_Employees]
GO
ALTER TABLE [dbo].[CheckBoxes]  WITH CHECK ADD  CONSTRAINT [FK_CheckBoxes_Texts] FOREIGN KEY([TextID])
REFERENCES [dbo].[Texts] ([TextID])
GO
ALTER TABLE [dbo].[CheckBoxes] CHECK CONSTRAINT [FK_CheckBoxes_Texts]
GO
ALTER TABLE [dbo].[CheckBoxList]  WITH CHECK ADD  CONSTRAINT [FK_CheckBoxList_CheckBoxes] FOREIGN KEY([CheckBoxID])
REFERENCES [dbo].[CheckBoxes] ([CheckBoxID])
GO
ALTER TABLE [dbo].[CheckBoxList] CHECK CONSTRAINT [FK_CheckBoxList_CheckBoxes]
GO
ALTER TABLE [dbo].[CheckBoxList]  WITH CHECK ADD  CONSTRAINT [FK_CheckBoxList_Tasks] FOREIGN KEY([TaskID])
REFERENCES [dbo].[Tasks] ([TaskID])
GO
ALTER TABLE [dbo].[CheckBoxList] CHECK CONSTRAINT [FK_CheckBoxList_Tasks]
GO
ALTER TABLE [dbo].[CommentList]  WITH CHECK ADD  CONSTRAINT [FK_CommentList_Comments] FOREIGN KEY([CommentID])
REFERENCES [dbo].[Comments] ([CommentID])
GO
ALTER TABLE [dbo].[CommentList] CHECK CONSTRAINT [FK_CommentList_Comments]
GO
ALTER TABLE [dbo].[CommentList]  WITH CHECK ADD  CONSTRAINT [FK_CommentList_Tasks] FOREIGN KEY([TaskID])
REFERENCES [dbo].[Tasks] ([TaskID])
GO
ALTER TABLE [dbo].[CommentList] CHECK CONSTRAINT [FK_CommentList_Tasks]
GO
ALTER TABLE [dbo].[Comments]  WITH CHECK ADD  CONSTRAINT [FK_Comments_Texts] FOREIGN KEY([TextID])
REFERENCES [dbo].[Texts] ([TextID])
GO
ALTER TABLE [dbo].[Comments] CHECK CONSTRAINT [FK_Comments_Texts]
GO
ALTER TABLE [dbo].[FilesInTextList]  WITH CHECK ADD  CONSTRAINT [FK_FilesInTextList_Files] FOREIGN KEY([FileID])
REFERENCES [dbo].[Files] ([FileID])
GO
ALTER TABLE [dbo].[FilesInTextList] CHECK CONSTRAINT [FK_FilesInTextList_Files]
GO
ALTER TABLE [dbo].[FilesInTextList]  WITH CHECK ADD  CONSTRAINT [FK_FilesInTextList_Texts] FOREIGN KEY([TextID])
REFERENCES [dbo].[Texts] ([TextID])
GO
ALTER TABLE [dbo].[FilesInTextList] CHECK CONSTRAINT [FK_FilesInTextList_Texts]
GO
ALTER TABLE [dbo].[InferiorList]  WITH CHECK ADD  CONSTRAINT [FK_InferiorList_Employees] FOREIGN KEY([ChiefID])
REFERENCES [dbo].[Employees] ([EmployeeID])
GO
ALTER TABLE [dbo].[InferiorList] CHECK CONSTRAINT [FK_InferiorList_Employees]
GO
ALTER TABLE [dbo].[InferiorList]  WITH CHECK ADD  CONSTRAINT [FK_InferiorList_Employees1] FOREIGN KEY([InferiorID])
REFERENCES [dbo].[Employees] ([EmployeeID])
GO
ALTER TABLE [dbo].[InferiorList] CHECK CONSTRAINT [FK_InferiorList_Employees1]
GO
ALTER TABLE [dbo].[TaskList]  WITH CHECK ADD  CONSTRAINT [FK_TaskList_Employees] FOREIGN KEY([EmployeeID])
REFERENCES [dbo].[Employees] ([EmployeeID])
GO
ALTER TABLE [dbo].[TaskList] CHECK CONSTRAINT [FK_TaskList_Employees]
GO
ALTER TABLE [dbo].[TaskList]  WITH CHECK ADD  CONSTRAINT [FK_TaskList_Tasks] FOREIGN KEY([TaskID])
REFERENCES [dbo].[Tasks] ([TaskID])
GO
ALTER TABLE [dbo].[TaskList] CHECK CONSTRAINT [FK_TaskList_Tasks]
GO
ALTER TABLE [dbo].[Tasks]  WITH CHECK ADD  CONSTRAINT [FK_Tasks_Employees] FOREIGN KEY([Author])
REFERENCES [dbo].[Employees] ([EmployeeID])
GO
ALTER TABLE [dbo].[Tasks] CHECK CONSTRAINT [FK_Tasks_Employees]
GO
ALTER TABLE [dbo].[Tasks]  WITH CHECK ADD  CONSTRAINT [FK_Tasks_Texts] FOREIGN KEY([Description])
REFERENCES [dbo].[Texts] ([TextID])
GO
ALTER TABLE [dbo].[Tasks] CHECK CONSTRAINT [FK_Tasks_Texts]
GO
ALTER TABLE [dbo].[TextListInChat]  WITH CHECK ADD  CONSTRAINT [FK_TextListInChat_Chats] FOREIGN KEY([ChatID])
REFERENCES [dbo].[Chats] ([ChatID])
GO
ALTER TABLE [dbo].[TextListInChat] CHECK CONSTRAINT [FK_TextListInChat_Chats]
GO
ALTER TABLE [dbo].[TextListInChat]  WITH CHECK ADD  CONSTRAINT [FK_TextListInChat_Texts] FOREIGN KEY([TextID])
REFERENCES [dbo].[Texts] ([TextID])
GO
ALTER TABLE [dbo].[TextListInChat] CHECK CONSTRAINT [FK_TextListInChat_Texts]
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Идентификатор сотрудника' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'ChatList', @level2type=N'COLUMN',@level2name=N'EmployeeID'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Идентификатор беседы' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'ChatList', @level2type=N'COLUMN',@level2name=N'ChatID'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Идентификатор беседы' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Chats', @level2type=N'COLUMN',@level2name=N'ChatID'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Название беседы' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Chats', @level2type=N'COLUMN',@level2name=N'Title'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Идентификатор сотрудника' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Employees', @level2type=N'COLUMN',@level2name=N'EmployeeID'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Фамилия' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Employees', @level2type=N'COLUMN',@level2name=N'Surname'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Имя' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Employees', @level2type=N'COLUMN',@level2name=N'Name'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Отчество ' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Employees', @level2type=N'COLUMN',@level2name=N'Patronymic'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Логин' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Employees', @level2type=N'COLUMN',@level2name=N'Login'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Пароль' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Employees', @level2type=N'COLUMN',@level2name=N'Password'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Описание' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Employees', @level2type=N'COLUMN',@level2name=N'Description'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Employees'
GO
