(*
Banking Prospect Follow-Up Automator
Automates scheduling follow-up tasks after a client meeting
*)

-- Get prospect information from the user
set prospectName to text returned of (display dialog "Enter Prospect Name:" default answer "" buttons {"Cancel", "Next"} default button 2)
set companyName to text returned of (display dialog "Enter Company Name:" default answer "" buttons {"Cancel", "Next"} default button 2)
set meetingDate to text returned of (display dialog "Meeting Date (e.g., Today):" default answer "Today" buttons {"Cancel", "Next"} default button 2)

-- Calculate follow-up dates (1 day, 3 days, 1 week from now)
set today to current date
set dayOne to today + 1 * days
set dayThree to today + 3 * days
set daySeven to today + 7 * days

-- Format dates for display
set shortDateOne to (dayOne as string)
set shortDateThree to (dayThree as string)
set shortDateSeven to (daySeven as string)

-- Create follow-up tasks in Reminders
tell application "Reminders"
	-- Create a new list for this prospect if it doesn't exist
	set listName to "Prospect Follow-ups"
	try
		set followupList to list listName
	on error
		set followupList to make new list with properties {name:listName}
	end try
	
	-- Day 1 Follow-up: Send meeting summary
	make new reminder in followupList with properties {
		name:"✉️ Email " & prospectName & " (" & companyName & ") - Meeting Summary",
		body:"Send follow-up email with meeting notes and next steps",
		due date:dayOne
	}
	
	-- Day 3 Follow-up: Check if they reviewed materials
	make new reminder in followupList with properties {
		name:"📞 Call " & prospectName & " (" & companyName & ") - Check Interest",
		body:"Follow up call to answer questions and discuss next steps",
		due date:dayThree
	}
	
	-- Day 7 Follow-up: Send additional value
	make new reminder in followupList with properties {
		name:"📊 Email " & prospectName & " (" & companyName & ") - Value Add",
		body:"Send relevant case study or market insights",
		due date:daySeven
	}
end tell

-- Create calendar events for key follow-ups
tell application "Calendar"
	-- Get or create a calendar for prospect follow-ups
	set calName to "Prospect Follow-ups"
	try
		set followupCal to calendar calName
	on error
		set followupCal to make new calendar with properties {name:calName}
	end try
	
	-- Calendar event for the important call on day 3
	make new event at end of events of followupCal with properties {
		summary:"Important Follow-up Call: " & prospectName & " (" & companyName & ")",
		start date:dayThree,
		end date:dayThree + 30 * minutes,
		description:"Call to discuss next steps and address any questions",
		location:"Phone",
		allday event:false
	}
end tell

-- Confirmation message with follow-up schedule
display dialog "Follow-up sequence scheduled for " & prospectName & ":

✓ Day 1 (" & shortDateOne & "): Email meeting summary
✓ Day 3 (" & shortDateThree & "): Follow-up call  
✓ Day 7 (" & shortDateSeven & "): Send value-add content

All tasks added to Reminders and Calendar." buttons {"OK"} default button 1 with icon note