#!/usr/bin/python
"""	--- startme.py ---
	Jay Hack, 2013
	------------------

	this is a program to start a new python program, using my coding conventions.
	this includes horizontal '#' bars for seperating out sections of code and 
	the initial import statements.

	this should be called in the directory that you want to create it in.
"""
import os
import sys

FILENAME_OPTION = '-f'
IMPORT_OPTION = '-i'
SECTIONS_OPTION = '-s'
MAIN_OPTION = '-m'
ERROR_OPTION = '-e'
valid_options = [FILENAME_OPTION, IMPORT_OPTION, SECTIONS_OPTION, MAIN_OPTION, ERROR_OPTION]
valid_options_string = ', '.join(valid_options)

MAIN_OPERATION_STRING = 'if __name__ == "__main__":'
ERROR_FUNCTION_STRING = """# Function: print_error
# ---------------------
# notifies the user of an error, how to correct it, then exits
def print_error (error_message, correction_message):
	print "ERROR: 	", error_message
	print "	---"
	print "	", correction_message
	exit ()"""

#---- section parameters ----
num_of_hashtags = 120
section_name_offset = 40



# Function: print_error
# ---------------------
# notifies the user of an error, how to correct it, then exits
def print_error (error_message, correction_message):
	print "ERROR: 	", error_message
	print "	---"
	print "	", correction_message
	exit ()



########################################################################################################################
################################[ GETTING ARGS ]########################################################################
########################################################################################################################

# Function: get_arguments
# -----------------------
# given the form of the option, this function will get all arguments that follow it.
# i.e. '-i module1 module2' would return the list ['module1', 'module2']
def get_arguments (args, option):
	num_of_args = len(args)

	if option in args:
		print option
		index = args.index (option)
		return_args = []
		
		i = index + 1
		if not i < num_of_args:
			return None

		current_arg = args[i]
		while i < num_of_args and current_arg[0] != '-':
			print "	" + current_arg
			return_args.append (current_arg)
			i += 1
			if i < num_of_args:
				current_arg = args[i]

		return return_args

	return None



# Function: get_all_options
# -------------------------
# given the args, returns all options as a dict mapping the option to its args
def get_all_options (args):
	options = {}

	selected_options = []
	for arg in args:
		if arg[0] == '-':
			selected_options.append (arg)

	for option in selected_options:
		if not option in valid_options:
			print_error ("you tried an invalid option: " + option, "try one of these: " + valid_options_string)
		this_option_args = get_arguments (args, option)
		options[option] = this_option_args

	return options





########################################################################################################################
################################[ PRINTING TO FILE ]####################################################################
########################################################################################################################

# Function: insert_import_statements
# -------------------------
# prints out all of the import statements into the file
def insert_import_statements (script_file, import_modules):
	
	if not import_modules:
		return

	for module in import_modules:
		script_file.write ('import ' + module + '\n')
	script_file.write('\n\n')

# Function: insert_sections
# -------------------------
# prints out all of the section names into the file w/ hashtag bars
def insert_sections (script_file, section_names):

	if not section_names:
		return

	for section_name in section_names:

		#--- top ---
		script_file.write ('#' * num_of_hashtags + "\n")

		#--- middle ---
		left_side_hashtags = num_of_hashtags - len(section_name) - 10 - section_name_offset
		middle_line = ('#' * section_name_offset) + '[--- ' + section_name.upper () + ' ---]' + ('#' * left_side_hashtags) + "\n"
		script_file.write (middle_line)

		#--- bottom ---
		script_file.write ('#' * num_of_hashtags + "\n")
		script_file.write ('\n\n')

# Function: insert_error_function
# -------------------------------
# will insert an error function at the top of the file, after import statements
def insert_error_function (script_file):
	
	script_file.write (ERROR_FUNCTION_STRING)
	script_file.write ("\n\n")

# Function: insert_main_operation
# -------------------------------
# will insert a line at the current cursor position for the main operation of the program.
def insert_main_operation (script_file):
	
	script_file.write (MAIN_OPERATION_STRING)
	script_file.write ("\n\n\n")



if __name__ == "__main__":

	#--- get options dict ---
	options = get_all_options (sys.argv)



	#--- file name ---
	if not FILENAME_OPTION in options.keys():
		print_error ("you didn't enter a filename", "the syntax is -f filename")
	script_filename_raw = options[FILENAME_OPTION][0]
	script_filename = os.path.join(os.getcwd(), script_filename_raw)
	print "---> creating script at: ", script_filename
	script_file = open (script_filename, 'w')

	#--- import statements ---
	if IMPORT_OPTION in options.keys ():
		import_modules = options[IMPORT_OPTION]
		print "---> import modules: ", ', '.join(import_modules)
		insert_import_statements(script_file, import_modules)

	#--- error function ---
	if ERROR_OPTION in options.keys ():
		print "---> adding error function"
		insert_error_function (script_file)

	#--- sections ---
	if SECTIONS_OPTION in options.keys ():	
		section_names = options[SECTIONS_OPTION]
		print "---> sections: ", ', '.join(section_names)
		insert_sections (script_file, section_names)
		del options[SECTIONS_OPTION]

	#--- main operation ---
	if MAIN_OPTION in options.keys():
		print "---> adding main operation section"
		insert_main_operation (script_file)


	script_file.close ()












