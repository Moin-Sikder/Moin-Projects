(*
Personalized Client Email Dispatcher
Automates sending personalized emails to banking clients using data from Numbers spreadsheet
*)

-- Configuration
property emailSubject : "Market Update and Portfolio Review"
property emailTemplate : "Dear {{Name}},`n`nHere is your latest market update. Based on your portfolio with account ending {{Account}}, we recommend reviewing the recent performance.`n`nBest regards,`nYour Banking Team"

tell application "Numbers"
	activate
	delay 1
	
	-- Get the front document and first table
	tell document 1
		tell sheet 1
			tell table 1
				-- Get data range (assuming headers in row 1)
				set dataRange to range "A2:D100" -- Adjust range as needed
				set clientData to value of dataRange
			end tell
		end tell
	end tell
end tell

tell application "Mail"
	activate
	delay 1
	
	set emailCount to 0
	set errorCount to 0
	set errorMessages to {}
	
	repeat with i from 1 to count of clientData
		set clientRecord to item i of clientData
		
		-- Skip empty rows
		if (count of clientRecord) ≥ 3 and item 1 of clientRecord is not "" then
			try
				-- Extract client data
				set clientName to item 1 of clientRecord
				set clientEmail to item 2 of clientRecord
				set accountNumber to item 3 of clientRecord
				
				-- Personalize email template
				set personalizedBody to my replaceText(emailTemplate, "{{Name}}", clientName)
				set personalizedBody to my replaceText(personalizedBody, "{{Account}}", accountNumber)
				
				-- Create and send email
				set newMessage to make new outgoing message with properties {subject:emailSubject, content:personalizedBody, visible:true}
				tell newMessage
					make new to recipient at end of to recipients with properties {address:clientEmail}
					-- Uncomment the line below to actually send emails
					-- send
				end tell
				
				set emailCount to emailCount + 1
				delay 0.5 -- Prevent overwhelming the mail app
				
			on error errMsg
				set errorCount to errorCount + 1
				set end of errorMessages to "Error with client " & clientName & ": " & errMsg
			end try
		end if
	end repeat
	
	-- Display summary
	display dialog "Email dispatch completed:" & return & return & ¬
		"✓ Successfully processed: " & emailCount & return & ¬
		"✗ Errors encountered: " & errorCount & return & return & ¬
		"Review the draft emails in Mail before sending." buttons {"OK"} default button 1
	
	-- Show errors if any
	if errorCount > 0 then
		set errorText to ""
		repeat with msg in errorMessages
			set errorText to errorText & msg & return
		end repeat
		display dialog "Errors encountered:" & return & return & errorText buttons {"OK"} default button 1
	end if
end tell

-- Helper function to replace text in template
on replaceText(theText, searchString, replacementString)
	set AppleScript's text item delimiters to searchString
	set textItems to text items of theText
	set AppleScript's text item delimiters to replacementString
	set theText to textItems as string
	set AppleScript's text item delimiters to ""
	return theText
end replaceText
