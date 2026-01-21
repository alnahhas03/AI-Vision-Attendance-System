import gspread

gc = gspread.service_account("facetrack-attendance.json")
sh = gc.open("CV_attendance")
ws = sh.sheet1

ws.update("A1", [["Hello ✅"]])

print("OK")