from computational_law.parser.helper_functions.clean_files import get_files, is_good_file, clean_file, make_pages

def test_get_files():
	assert get_files('fake_dir') == ['fake_dir/fake_subdir1/fake_file1.txt',
									 'fake_dir/fake_subdir2/fake_file1.txt']

def test_is_good_file():
	# Case: not a text file
	assert is_good_file('fake_dir/.DS_Store') == False
	assert is_good_file('fake_dir/fake_subdir2/fake_file1.py') == False

	# Case: good .txt
	filename = 'transcripts/2009/!A-32262.txt'
	assert is_good_file(filename) == True

	# Case: not a good .txt file
	filename = 'transcripts/2009/!B-22677 MEMO.txt'
	assert is_good_file(filename) == False

	filename = 'transcripts/2009/!Board Meeting Sept 15, 2009.txt'
	assert is_good_file(filename) == False

	filename = 'transcripts/2009/!BPHEXECUTIVEBOARDHEARING_11-17-09.txt'
	assert is_good_file(filename) == False

def test_clean_file():
	# Case: splitting 'r'
	expected_out = ['SUBSEQUENT PAROLE CONSIDERATION HEARING STATE OF CALIFORNIA',
					'BOARD OF PAROLE HEARINGS',
					'In the matter of the Life ) CDC Number: A-32262 Term Parole Consideration )',
					'Hearing of: )', 'BOOKER HILLERY ) _________ )',
					'CALIFORNIA MEDICAL FACILITY VACAVILLE, CALIFORNIA NOVEMBER 23, 2009',
					'4:00 P.M.', 'PANEL PRESENT:',
					'ARTHUR ANDERSON, Presiding Commissioner TERRI TURNER, Deputy Commissioner',
					'OTHERS PRESENT:', 'BOOKER HILLERY, Inmate',
					'KATE BROSGART, Attorney for Inmate', 'BILL ARMBRUSTER, Deputy District Attorney',
					 'CORRECTIONS TO THE DECISION HAVE BEEN MADE', 'No See Review of Hearing Yes Transcript Memorandum',
					 'CYNTHIA M. FLETCHER, WPU, Inc.', '2', 'INDEX',
					 'Page Proceedings ........................................ 3 Case Factors ....................................... 10 Pre-Commitment Factors ............................. 10 Post-Commitment Factors ............................ 11 Parole Plans ....................................... 23 Closing Statements ................................. 27 Recess ............................................. 29 Decision ........................................... 30 Adjournment ........................................ 39 Transcriber Certification .......................... 40',
					 'WPU, Inc.']
	assert clean_file('data/case_split_r.txt') == expected_out

	# Case: cleaning text
	expected_out = ['clinicians in the completion of any future clinical evaluations. Deputy Commissioner Turner, do you have any final comments?',
	 				"DEPUTY COMMISSIONER TURNER: Mr. Hillery, the next time you come to the Board, bring your documents with you just in case they don't get into the central file, your chronos and stuff that you were talking about.",
					"INMATE HILLERY: Thank you. They didn't want them in there, ma'am. They didn't want them in there and --",
					'DEPUTY COMMISSIONER TURNER: Okay.',
					"INMATE HILLERY: -- and what have been did here today, I wouldn't do it to a dog, what had been did.",
					'You know, really, what I have been through and the way I have been convicted, you know --',
					'PRESIDING COMMISSIONER ANDERSON: Mr. Hillery -- INMATE HILLERY: I just want to say --',
					"PRESIDING COMMISSIOENR ANDERSON: -- we're not", 'talking about the crime.',
					"INMATE HILLERY: I'm not talking about the crime.",
					'You, you, you want to talk about the crime.',
					"PRESIDING COMMISSIONER ANDERSON: You're not going",
					"to talk about it. You say, you say you're not going to talk about anything?",
					"INMATE HILLERY: I'm not talking about the crime. BOOKER HILLERY A-32262 DECISION PAGE 9 11/23/09"]
	assert clean_file('data/case_clean.txt') == expected_out

def test_make_pages():
	lst_input = ['SUBSEQUENT PAROLE CONSIDERATION HEARING STATE OF CALIFORNIA',
				 'BOARD OF PAROLE HEARINGS', 'In the matter of the Life ) CDC Number: A-32262 Term Parole Consideration )',
				 'Hearing of: )', 'BOOKER HILLERY ) _________ )', 'CALIFORNIA MEDICAL FACILITY VACAVILLE, CALIFORNIA NOVEMBER 23, 2009',
				 '4:00 P.M.', 'PANEL PRESENT:', 'ARTHUR ANDERSON, Presiding Commissioner TERRI TURNER, Deputy Commissioner',
				 'OTHERS PRESENT:', 'BOOKER HILLERY, Inmate', 'KATE BROSGART, Attorney for Inmate',
				 'BILL ARMBRUSTER, Deputy District Attorney', 'CORRECTIONS TO THE DECISION HAVE BEEN MADE',
				 'No See Review of Hearing Yes Transcript Memorandum', 'CYNTHIA M. FLETCHER, WPU, Inc.', '2', 'INDEX',
				 'Page Proceedings ........................................ 3 Case Factors ....................................... 10 Pre-Commitment Factors ............................. 10 Post-Commitment Factors ............................ 11 Parole Plans ....................................... 23 Closing Statements ................................. 27 Recess ............................................. 29 Decision ........................................... 30 Adjournment ........................................ 39 Transcriber Certification .......................... 40',
				 'WPU, Inc.', '3', '1 2 3 4 5 6 7 8 9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21',
				 '22', '23', '24', '25', 'PROCEEDINGS', 'PRESIDING COMMISSIONER ANDERSON: The time is now',
				 "4:00. Today's date is 11/23/2009. We're located at California Medical Facility in Vacaville, California. This is a Subsequent Parole Hearing for Booker Hillery, CDC Number A-32262. The inmate was received in a CDCR on 11/17/1962. Life time began on the same date. The County is Kings and Kern. Offense is Murder in the First Degree, Case Number 13914-3922. The inmate received a term of life. The minimum eligible parole date is 6/15/1970. This Hearing is being recorded for the purposes of voice identification. Each of us will be required to state our first and last name, spelling our last name. When it comes to the inmate's turn, after you spell your last name, give us your CDC Number. My name is Arthur Anderson, A-N-D-E-R-S-O-N, Commissioner.",
				 'DEPUTY COMMISSIONER TURNER: Terri Turner, T-U-R-N- E-R, Deputy Commissioner.',
				 'DEPUTY DISTRICT ATTORNEY ARMBRUSTER: Bill Armbruster, Deputy District Attorney from Kings County, A-R-M-B-R-U-S-T-E-R.',
				 'ATTORNEY BROSGART: Kate Brosgart, Counsel for Mr. Hillery.', 'INMATE HILLERY: Booker T. Hillery, Jr.', 'WPU, Inc.', '4',
				 '1 2 3 4 5 6 7 8 9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25',
				 'DEPUTY COMMISSIONER TURNER: CDC Number?', 'INMATE HILLERY: My CDC Number is A-32262.',
				 'DEPUTY COMMISSIONER TURNER: Spell your last name,', 'please.', 'INMATE HILLERY: My last name is H-I-L-L-E-R-Y. DEPUTY COMMISSIONER TURNER: Thank you.',
				 "INMATE HILLERY: Yes, ma'am.", 'PRESIDING COMMISSIONER ANDERSON: Okay, Mr.',
				 "Hillery, we're going to go over some ADA, Americans with Disabilities Act issues. The ADA form of declarations is right in front of you. Take a moment, please and, can you read that without glasses? Oh, you have your glasses with you?",
				 'INMATE HILLERY: Yes.', "PRESIDING COMMISSIONER ANDERSON: Okay. Would you read that for me, to yourself, and when you're done, let me know you completed it, and then we'll have further discussion.",
				 'INMATE HILLERY: (Complied.) Okay.', 'PRESIDING COMMISSIONER ANDERSON: Do you have any questions?', 'INMATE HILLERY: No, sir.',
				 "PRESIDING COMMISSIONER ANDERSON: I've read your ADA Form, too. I have it in front of me, the BPT Form 1073, and I want to acknowledge that you have mobility",
				 'WPU, Inc.', '5']
	expected_out = [['SUBSEQUENT PAROLE CONSIDERATION HEARING STATE OF CALIFORNIA', 'BOARD OF PAROLE HEARINGS', 'In the matter of the Life ) CDC Number: A-32262 Term Parole Consideration )', 'Hearing of: )', 'BOOKER HILLERY ) _________ )', 'CALIFORNIA MEDICAL FACILITY VACAVILLE, CALIFORNIA NOVEMBER 23, 2009', '4:00 P.M.', 'PANEL PRESENT:', 'ARTHUR ANDERSON, Presiding Commissioner TERRI TURNER, Deputy Commissioner', 'OTHERS PRESENT:', 'BOOKER HILLERY, Inmate', 'KATE BROSGART, Attorney for Inmate', 'BILL ARMBRUSTER, Deputy District Attorney', 'CORRECTIONS TO THE DECISION HAVE BEEN MADE', 'No See Review of Hearing Yes Transcript Memorandum', 'CYNTHIA M. FLETCHER, WPU, Inc.'], ['INDEX', 'Page Proceedings ........................................ 3 Case Factors ....................................... 10 Pre-Commitment Factors ............................. 10 Post-Commitment Factors ............................ 11 Parole Plans ....................................... 23 Closing Statements ................................. 27 Recess ............................................. 29 Decision ........................................... 30 Adjournment ........................................ 39 Transcriber Certification .......................... 40'],
					['PROCEEDINGS', 'PRESIDING COMMISSIONER ANDERSON: The time is now', "4:00. Today's date is 11/23/2009. We're located at California Medical Facility in Vacaville, California. This is a Subsequent Parole Hearing for Booker Hillery, CDC Number A-32262. The inmate was received in a CDCR on 11/17/1962. Life time began on the same date. The County is Kings and Kern. Offense is Murder in the First Degree, Case Number 13914-3922. The inmate received a term of life. The minimum eligible parole date is 6/15/1970. This Hearing is being recorded for the purposes of voice identification. Each of us will be required to state our first and last name, spelling our last name. When it comes to the inmate's turn, after you spell your last name, give us your CDC Number. My name is Arthur Anderson, A-N-D-E-R-S-O-N, Commissioner.", 'DEPUTY COMMISSIONER TURNER: Terri Turner, T-U-R-N- E-R, Deputy Commissioner.', 'DEPUTY DISTRICT ATTORNEY ARMBRUSTER: Bill Armbruster, Deputy District Attorney from Kings County, A-R-M-B-R-U-S-T-E-R.', 'ATTORNEY BROSGART: Kate Brosgart, Counsel for Mr. Hillery.', 'INMATE HILLERY: Booker T. Hillery, Jr.'],
					['DEPUTY COMMISSIONER TURNER: CDC Number?', 'INMATE HILLERY: My CDC Number is A-32262.', 'DEPUTY COMMISSIONER TURNER: Spell your last name,', 'please.', 'INMATE HILLERY: My last name is H-I-L-L-E-R-Y. DEPUTY COMMISSIONER TURNER: Thank you.', "INMATE HILLERY: Yes, ma'am.", 'PRESIDING COMMISSIONER ANDERSON: Okay, Mr.', "Hillery, we're going to go over some ADA, Americans with Disabilities Act issues. The ADA form of declarations is right in front of you. Take a moment, please and, can you read that without glasses? Oh, you have your glasses with you?", 'INMATE HILLERY: Yes.', "PRESIDING COMMISSIONER ANDERSON: Okay. Would you read that for me, to yourself, and when you're done, let me know you completed it, and then we'll have further discussion.", 'INMATE HILLERY: (Complied.) Okay.', 'PRESIDING COMMISSIONER ANDERSON: Do you have any questions?', 'INMATE HILLERY: No, sir.', "PRESIDING COMMISSIONER ANDERSON: I've read your ADA Form, too. I have it in front of me, the BPT Form 1073, and I want to acknowledge that you have mobility"]]
	assert make_pages(lst_input) == expected_out


if __name__ == '__main__':
	test_get_files()
	test_is_good_file()
	test_clean_file()
	test_make_pages()
