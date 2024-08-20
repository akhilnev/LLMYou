from file_parser import parse_file_to_string

user_details = parse_file_to_string("AK_Resume.pdf")

user_details += parse_file_to_string("Akhilesh_Linkedin_Resume_2024.pdf")

prompt = "More on Akhilesh's coding skills and competencies ? "