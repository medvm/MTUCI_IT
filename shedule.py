
import psycopg2
import sys

from PyQt5.QtWidgets import (QApplication, QWidget,
							 QTabWidget, QAbstractScrollArea,
							 QVBoxLayout, QHBoxLayout,
							 QTableWidget, QGroupBox,
						 QTableWidgetItem, QPushButton, QMessageBox, QComboBox)
class MainWindow(QWidget):
	def __init__(self):
		super(MainWindow, self).__init__()

		self._connect_to_db()

		self.setWindowTitle("Shedule")

		self.vbox = QVBoxLayout(self)

		self.tabs = QTabWidget(self)
		self.vbox.addWidget(self.tabs)

		self._create_shedule_tab()
		self._create_teacher_tab()
		self._create_subjects_tab()

	def _connect_to_db(self):
		self.conn = psycopg2.connect(database="postgres",
									 user="postgres",
									 password="passwd",
					 				 host="localhost",
					 				 port="5432")

		self.cursor = self.conn.cursor()
		self.conn.autocommit = True

# tabs

	def _create_shedule_tab(self):
		self.shedule_tab = QWidget()
		self.tabs.addTab(self.shedule_tab, "Shedule")
		self.svbox = QVBoxLayout()
		days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',  'Friday' ]
		for i in range(len(days)):
			setattr(self, f'{days[i]}_gbox', QGroupBox(days[i]))
			setattr(self, f'shbox{i}', QHBoxLayout())
			self.svbox.__getattribute__('addLayout')(getattr(self, f'shbox{i}'))
			getattr(self, f'shbox{i}').__getattribute__('addWidget')(getattr(self, f'{days[i]}_gbox'))
			self.__getattribute__('_create_day_table')(f'{days[i]}')

		self.shbox5 = QHBoxLayout()
		self.svbox.addLayout(self.shbox5)
		self.update_shedule_button = QPushButton("Update")
		self.shbox5.addWidget(self.update_shedule_button)
		self.update_shedule_button.clicked.connect(self._update_shedule)

		self.shedule_tab.setLayout(self.svbox)
 
	def _create_teacher_tab(self):
		self.teacher_tab = QWidget()
		self.tabs.addTab(self.teacher_tab, "Teachers")

		self.teacher_gbox = QGroupBox("Teachers")
		self.svbox = QVBoxLayout()
		self.shbox1 = QHBoxLayout()
		self.shbox2 = QHBoxLayout()

		self.svbox.addLayout(self.shbox1)
		self.svbox.addLayout(self.shbox2)

		self.shbox1.addWidget(self.teacher_gbox)

		self._create_teacher_table()

		self.update_shedule_button = QPushButton("Update")
		self.shbox2.addWidget(self.update_shedule_button)
		self.update_shedule_button.clicked.connect(self._update_shedule)

		self.teacher_tab.setLayout(self.svbox)

	def _create_subjects_tab(self):
		self.subjects_tab = QWidget()
		self.tabs.addTab(self.subjects_tab, "Subjects")

		self.subjects_gbox = QGroupBox("Subjects")

		self.svbox = QVBoxLayout()
		self.shbox1 = QHBoxLayout()
		self.shbox2 = QHBoxLayout()

		self.svbox.addLayout(self.shbox1)
		self.svbox.addLayout(self.shbox2)

		self.shbox1.addWidget(self.subjects_gbox)

		self._create_subjects_table()

		self.update_shedule_button = QPushButton("Update")
		self.shbox2.addWidget(self.update_shedule_button)
		self.update_shedule_button.clicked.connect(self._update_shedule)

		self.subjects_tab.setLayout(self.svbox)

# tables

	def _create_day_table(self, day):
		setattr(self, f'day_table_{day}', QTableWidget())
		getattr(self, f'day_table_{day}').setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

		getattr(self, f'day_table_{day}').setColumnCount(7)
		getattr(self, f'day_table_{day}').setHorizontalHeaderLabels(["id", "day", "Subject", "Room", "Time", "", ""])

		self._update_day_table(day)

		self.mvbox = QVBoxLayout()
		self.mvbox.addWidget(getattr(self, f'day_table_{day}'))
		getattr(self, f'{day}_gbox').setLayout(self.mvbox)

	def _create_teacher_table(self):
		self.teacher_table = QTableWidget()
		self.teacher_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

		self.teacher_table.setColumnCount(5)
		self.teacher_table.setHorizontalHeaderLabels(["id","full_name", "Subject", "", ""])

		self._update_teacher_table()

		self.mvbox = QVBoxLayout()
		self.mvbox.addWidget(self.teacher_table)
		self.teacher_gbox.setLayout(self.mvbox)

	def _create_subjects_table(self):
		self.subjects_table = QTableWidget()
		self.subjects_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

		self.subjects_table.setColumnCount(4)
		self.subjects_table.setHorizontalHeaderLabels(["id", "name", "", ""])

		self._update_subjects_table()

		self.mvbox = QVBoxLayout()
		self.mvbox.addWidget(self.subjects_table)
		self.subjects_gbox.setLayout(self.mvbox)		

	def _update_day_table(self, day):
		getattr(self, f'day_table_{str(day)}').setRowCount(0)	
		print(f"SELECT * FROM timetable WHERE day='{str(day)}'")
		self.cursor.execute(f"SELECT * FROM timetable WHERE day='{str(day)}'")
		records = list(self.cursor.fetchall())
		print(records)

		getattr(self, f'day_table_{day}').setRowCount(len(records)+1)

		for i, r in enumerate(records):
			r = list(r)
			joinButton    = QPushButton("Save changes")
			deleteButton  = QPushButton("Delete record")
			insertButton  = QPushButton("Insert record")
			getattr(self, f'day_table_{day}').setItem(i, 0, QTableWidgetItem(str(r[0])))
			getattr(self, f'day_table_{day}').setItem(i, 1, QTableWidgetItem(str(r[1])))
			getattr(self, f'day_table_{day}').setItem(i, 2, QTableWidgetItem(str(r[2])))
			getattr(self, f'day_table_{day}').setItem(i, 3, QTableWidgetItem(str(r[3])))
			getattr(self, f'day_table_{day}').setItem(i, 4, QTableWidgetItem(str(r[4])))
			getattr(self, f'day_table_{day}').setCellWidget(i, 5, joinButton)
			getattr(self, f'day_table_{day}').setCellWidget(i, 6, deleteButton)
			getattr(self, f'day_table_{day}').setCellWidget(len(records), 5, insertButton)

			joinButton.clicked.connect(lambda ch, num=i, day=day: self._change_day_from_table(num, day))
			deleteButton.clicked.connect(lambda ch, id_to_delete=r[0], num=i: self._delete_day_from_table(id_to_delete, num, day))
			insertButton.clicked.connect(lambda ch, num=i+1: self._insert_day_from_table(num, day))

			getattr(self, f'day_table_{day}').resizeRowsToContents()

		if len(records) == 0:
			insertButton = QPushButton("Insert 1st record")
			getattr(self, f'day_table_{day}').setCellWidget(len(records), 5, insertButton)	
			insertButton.clicked.connect(lambda ch, num=0: self._insert_day_from_table(num, day))

			getattr(self, f'day_table_{day}').resizeRowsToContents()		


	def _update_teacher_table(self):
		self.teacher_table.removeRow(0)	
		self.cursor.execute("SELECT * FROM teacher")
		records = list(self.cursor.fetchall())	
		self.teacher_table.setRowCount(len(records)+1)
		
		for i, r in enumerate(records):
			r = list(r)
			joinButton    = QPushButton("Save changes")
			deleteButton  = QPushButton("Delete record")
			insertButton  = QPushButton("Insert record")
			self.teacher_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
			self.teacher_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
			self.teacher_table.setItem(i, 2, QTableWidgetItem(str(r[2])))

			# self.cursor.execute("SELECT subject FROM subject")
			# records = list(self.cursor.fetchall())
			# CBox = QComboBox()
			# for j in range(len(records)):
			# 	records[j] = str(records[j]).replace('(', '')
			# 	records[j] = str(records[j]).replace(')', '')
			# 	records[j] = str(records[j]).replace("'", "")
			# 	records[j] = str(records[j]).replace(',', '')
			# print(records)
			# CBox.addItems(records)
			# CBox.setStyleSheet('QComboBox{}')
			# self.teacher_table.setCellWidget(len(records), 2, CBox)	
			
			self.teacher_table.setCellWidget(i, 3, joinButton)
			self.teacher_table.setCellWidget(i, 4, deleteButton)
			self.teacher_table.setCellWidget(len(records), 3, insertButton)
			joinButton.clicked.connect(lambda ch, num=i: self._change_teacher_from_table(num))
			deleteButton.clicked.connect(lambda ch, id_to_delete=r[0], num=i: self._delete_teacher_from_table(id_to_delete, num))
			insertButton.clicked.connect(lambda ch, num=i+1: self._insert_teacher_from_table(num))

			self.teacher_table.resizeRowsToContents()	

		if len(records) == 0:
			insertButton = QPushButton("Insert 1st record")
			self.teacher_table.setCellWidget(len(records), 3, insertButton)	
			insertButton.clicked.connect(lambda ch, num=0: self._insert_teacher_from_table(num))

			self.teacher_table.resizeRowsToContents()	


	def _update_subjects_table(self):		
		self.subjects_table.removeRow(0)		
		self.cursor.execute("SELECT * FROM subject")
		records = list(self.cursor.fetchall())
		self.subjects_table.setRowCount(len(records)+1)
		
		for i, r in enumerate(records):
			r = list(r)
			joinButton    = QPushButton("Save changes")
			deleteButton  = QPushButton("Delete record")
			insertButton  = QPushButton("Insert record")
			self.subjects_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
			self.subjects_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
			self.subjects_table.setCellWidget(i, 2, joinButton)
			self.subjects_table.setCellWidget(i, 3, deleteButton)
			self.subjects_table.setCellWidget(len(records), 2, insertButton)
			joinButton.clicked.connect(lambda ch, num=i: self._change_subjects_from_table(num))
			deleteButton.clicked.connect(lambda ch, id_to_delete=r[0], num=i: self._delete_subjects_from_table(id_to_delete, num))
			insertButton.clicked.connect(lambda ch, num=i+1: self._insert_subjects_from_table(num))

			self.subjects_table.resizeRowsToContents()	

		if len(records) == 0:
			insertButton = QPushButton("Insert 1st record")
			self.subjects_table.setCellWidget(len(records), 2, insertButton)	
			insertButton.clicked.connect(lambda ch, num=0: self._insert_subjects_from_table(num))

			self.subjects_table.resizeRowsToContents()

	def _change_day_from_table(self, rowNum, day):
		print(day)
		row = list()
		for i in range(getattr(self, f'day_table_{day}').columnCount()):
			try:
				row.append(getattr(self, f'day_table_{day}').item(rowNum, i).text())
			except:
				row.append(None)
		print(row)		
		try:
			self.cursor.execute(f"UPDATE timetable SET (day, subject, room_numb, start_time) = ('{row[1]}','{row[2]}','{row[3]}','{row[4]}') WHERE id={row[0]};")
			self.conn.commit()
		except:
			QMessageBox.about(self, "Error", "Fill in all the fields in the row correctly!")
			print(f"UPDATE timetable SET day='{row[1]}' subject='{row[2]}' room_numb='{row[3]}' start_time='{row[4]}' WHERE id={row[0]};")


	def _change_teacher_from_table(self, rowNum):
		row = list()
		for i in range(self.teacher_table.columnCount()):
			try:
				row.append(self.teacher_table.item(rowNum, i).text())
			except:
				row.append(None)

		# print(self.cursor.execute("UPDATE teacher SET subject='" + row[2] + "', full_name='" + row[1] +  "' where id='" + str(row[0]) + "'"))
		try:
			self.cursor.execute("UPDATE teacher SET subject='" + str(row[2]) + "', full_name='" + row[1] +  "' where id='" + str(row[0]) + "'")
			self.conn.commit()
		except:
			QMessageBox.about(self, "Error", "Fill in all the fields in the row correctly!")	

	def _change_subjects_from_table(self, rowNum):
		row = list()
		for i in range(self.subjects_table.columnCount()):
			try:
				row.append(self.subjects_table.item(rowNum, i).text())
			except:
				row.append(None)

		try:
			self.cursor.execute("UPDATE subject SET subject='" + row[1] + "' where id='" + str(row[0]) + "'")
			self.conn.commit()
		except:
			QMessageBox.about(self, "Error", "Fill in all the fields in the row correctly!")	

	def _delete_day_from_table(self, id_to_delete, rowNum, day):
		try:
			self.cursor.execute("delete from timetable where id=" + str(id_to_delete) + ";")
			self.conn.commit()
		except:
			QMessageBox.about(self, "Error", "Field doesn't exist")
		getattr(self, f'day_table_{day}').removeRow(rowNum)
		self._update_day_table(day)

	def _delete_subjects_from_table(self, id_to_delete, rowNum):
		try:
			self.cursor.execute("delete from subject where id='" + str(id_to_delete) + "';")
			self.conn.commit()
		except:
			QMessageBox.about(self, "Error", "Field doesn't exist")
		self.subjects_table.removeRow(rowNum)
		self._update_subjects_table()

	def _delete_teacher_from_table(self, id_to_delete, rowNum):
		try:
			self.cursor.execute("delete from teacher where id='" + str(id_to_delete) + "';")
			self.conn.commit()
		except:
			QMessageBox.about(self, "Error", "Field doesn't exist")
		self.teacher_table.removeRow(rowNum)
		self._update_teacher_table()						

		

	def _insert_day_from_table(self, rowNum, day):
		row = list()
		for i in range(getattr(self, f'day_table_{day}').columnCount()):
			try:
				row.append(getattr(self, f'day_table_{day}').item(rowNum, i).text())
			except:
				row.append(None)
			
		print(row)					
		try:
			self.cursor.execute(f"insert into timetable values ({str(row[0])},'{str(row[1])}','{str(row[2])}','{str(row[3])}','{str(row[4])}');")
			self.conn.commit()
			# self._update_day_table()
		except:
			QMessageBox.about(self, "Error", "Fill in all the fields in the row correctly!")
			print(f"insert into timetable values ({row[0]},'{row[1]}','{row[2]}','{row[3]}','{row[4]}');")		


	def _insert_teacher_from_table(self, rowNum):
		row = list()
		for i in range(self.teacher_table.columnCount()):
			try:
				row.append(self.teacher_table.item(rowNum, i).text())
			except:
				row.append(None)
			
		print(row)					
		try:
			self.cursor.execute("insert into teacher values ('" + str(row[0]) + "', '" + row[1] + "', '" + str(row[2]) + "');")
			self.conn.commit()
			self._update_teacher_table()
		except:
			QMessageBox.about(self, "Error", "Fill in all the fields in the row correctly!")	

	def _insert_subjects_from_table(self, rowNum):
		row = list()
		for i in range(self.subjects_table.columnCount()):
			try:
				row.append(self.subjects_table.item(rowNum, i).text())
			except:
				row.append(None)
		print(row)					
		try:
			self.cursor.execute("insert into subject values ('" + str(row[0]) + "', '" + str(row[1]) + "');")
			self.conn.commit()
			self._update_subjects_table()
		except:
			QMessageBox.about(self, "Error", "Fill in all the fields in the row correctly!")	
			print("insert into subject values ('" + str(row[0]) + "', '" + row[1] + "');")

	def _update_shedule(self):
		days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',  'Friday' ]
		for day in days: 
			self._update_day_table(day)
		self._update_teacher_table()
		self._update_subjects_table()
		

app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())


# CREATE TABLE timetable (
# 	id serial PRIMARY KEY, 
# 	day VARCHAR ( 50 ) NOT NULL, 
# 	subject VARCHAR ( 50 ) NOT NULL, 
# 	room_numb VARCHAR ( 255 ) NOT NULL, 
# 	start_time time (0) without time zone,
# 	FOREIGN KEY (subject) REFERENCES subject (name));

# CREATE TABLE teacher (
# 	id serial PRIMARY KEY, 
# 	full_name VARCHAR ( 50 ) NOT NULL, 
# 	subject VARCHAR ( 50 ) NOT NULL,
# 	FOREIGN KEY (subject) REFERENCES subject (name));


# CREATE TABLE subject (
# 	id serial PRIMARY KEY, 
# 	name VARCHAR ( 50 ) UNIQUE NOT NULL);



